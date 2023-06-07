/* SQL file for edens_interface.py */
SELECT
	'' AS zero,
    RECEIPT_NUMBER,
    '' AS one,
    '' AS two,
    '' AS three,
    DATE_PAYMENT,
    '' AS four,
    'N' AS n,
    'Y' AS y,
	'R' AS r,  -- [R]evenue vs. [E]xpenditure
    /*
	CASE
        WHEN FEE_AMOUNT_ASSESSED < 0 THEN 'E'
        ELSE 'R'
        END AS r,  -- Revenue or Expenditure
	*/
    FEE_ACCT_CODE_1,
    RECORD_ID,
    FEE_AMOUNT_ASSESSED,
    '' AS five,
    '' AS six,
    '' AS seven,
    '' AS eight,
	'' AS nine

FROM V_FEE_PAYMENT_HISTORY

WHERE
    -- Limit the query to data from yesterday
    (DATE_PAYMENT >= '{start_date}' AND DATE_PAYMENT < '{end_date}')
    --AND RECEIPT_NUMBER = '257128'
ORDER BY
    RECEIPT_NUMBER
;
