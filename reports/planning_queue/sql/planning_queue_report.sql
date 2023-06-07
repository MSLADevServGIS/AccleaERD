/*
Report for Emily Gluckin (P&LUSE) that counts permits by status in order to understand
what Planning's queue looks like.

Author: Garin Wally, 2020-07-29
Credit: Missy Kern
*/

--/*
SELECT
	reviewtype,
	permittype,

    -- Count the permits by workflow status
	SUM(CASE
		WHEN wfstatus = 'In Process'
		THEN 1 ELSE 0 END) AS InProcess,

	SUM(CASE
		WHEN wfstatus LIKE 'Additional%'
		THEN 1 ELSE 0 END) AS AdditionalRequired,

	SUM(CASE
		WHEN wfstatus LIKE '%received%'
		THEN 1 ELSE 0 END) AS ResubmittalReceived,

	SUM(CASE
		WHEN wfstatus = ''
		THEN 1 ELSE 0 END) AS InQueue,

    -- Number of the permits counted above which were submitted within 7 days
	-- This column breaks out permits already counted by status
	SUM(CASE
		WHEN submit_date > (GetDate() - 7)
		THEN 1 ELSE 0 END) AS New,

	-- Anything else (e.g. 'County Review Required')
	SUM(CASE
		WHEN wfstatus NOT IN ('', 'In Process') AND wfstatus NOT LIKE 'Additional%' AND wfstatus NOT LIKE '%received%'
		THEN 1 ELSE 0 END) AS Misc,

	-- The sum of all columns except New
	COUNT(permitid) AS Total,

	MIN(CASE
		WHEN wfstatus = ''
		THEN submit_date
		END) AS OldestNotStarted

FROM (
--*/
	SELECT
        a1.B1_ALT_ID AS permitid,
        a1.B1_PER_GROUP AS permitgroup,
        CASE
            WHEN b1.B1_CHECKLIST_COMMENT IS NULL AND a1.B1_PER_GROUP = 'Licenses'
            THEN 'EDR'
            WHEN b1.B1_CHECKLIST_COMMENT IS NULL AND a1.B1_PER_GROUP IN ('Planning', 'Building')
            THEN 'Paper' 
            ELSE b1.B1_CHECKLIST_COMMENT
            END AS reviewtype,
        CASE
            WHEN a1.B1_PER_TYPE LIKE '%Revision'
            THEN a1.B1_PER_TYPE + ' (' + SUBSTRING(a1.B1_ALT_ID, 10, 3) + ')'
            ELSE a1.B1_PER_TYPE END AS permittype,

        a1.B1_FILE_DD AS submit_date,
        w1.SD_APP_DES AS wfstatus

	FROM B1PERMIT a1

	JOIN GPROCESS w1
		ON a1.SERV_PROV_CODE=w1.SERV_PROV_CODE
			AND a1.B1_PER_ID1=w1.B1_PER_ID1
			AND a1.B1_PER_ID2=w1.B1_PER_ID2
			AND a1.B1_PER_ID3=w1.B1_PER_ID3
			AND w1.SD_PRO_DES IN ('Planning', 'Planning Review')
			AND w1.SD_CHK_LV1 = 'Y'

	LEFT OUTER JOIN BCHCKBOX b1
		ON a1.SERV_PROV_CODE=b1.SERV_PROV_CODE
			AND a1.B1_PER_ID1=b1.B1_PER_ID1
			AND a1.B1_PER_ID2=b1.B1_PER_ID2
			AND a1.B1_PER_ID3=b1.B1_PER_ID3
			AND b1.B1_CHECKBOX_DESC = 'Plan Review Type'

	WHERE
		(
			((a1.B1_PER_TYPE IN ('Residential Construction', 'Commercial Construction') OR a1.B1_PER_TYPE LIKE '%revision') AND a1.B1_PER_GROUP = 'Building')
			OR (a1.B1_PER_GROUP = 'Planning' AND a1.B1_PER_TYPE IN ('Sign', 'Zoning Compliance'))
			OR a1.B1_PER_GROUP = 'Licenses'
		)
		AND a1.B1_APPL_STATUS = 'Open'
		--AND a1.B1_ALT_ID IN ('2020-MSS-COM-00147', '2020-mss-com-00171')
--/*
	) i
GROUP BY permitgroup, reviewtype, permittype
--*/
;
