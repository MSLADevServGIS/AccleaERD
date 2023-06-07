"""planning_queue.py -- Planning Queue Report
Author: Garin Wally;

This script gives Current Planning a look at what work is "in their queue".

I only made the minimal changes to get this script working on AccelaERD,
so it does not conform with my ideal practices (see edens_interface.py):
* No logging
* Does not utilize reportutils.Report and proper __file__ handling.

I have other future plans to incorporate manual efforts Charlie Ream makes to
improve the layout of the results.
"""
import datetime as dt
from pathlib import Path

import pandas as pd

from dbconnections import AccelaProd, AccelaNonProd1
# TODO: logging


path = Path(__file__).parent


class PlanningQueue(object):  # TODO: use reportutils
    def __init__(self, accela):
        self.accela = accela.connect()
        self.script = path.joinpath("sql/planning_queue_report.sql").absolute()
        #self.out_dir = Path("I:/00 Maps/Reports/Planning")
        self.out_dir = Path(r"\\CITYFILES\DEVServices\00 MAPS\Reports\Planning")
        self.out_file = self.out_dir / f"PlanningQueueReport-{dt.datetime.now().strftime('%Y-%m-%d')}.xlsx"
        self.name = "Planning Queue"
        self.description = "Weekly report of permits/licenses in the Planning Queue."

    def check_schedule(self) -> bool:
        """."""
        return True

    @property
    def required_tables(self) -> list[str]:
        return []

    def flight_checks(self) -> None:
        return

    def main(self) -> None:
        sql = self.script.open().read()
        df = pd.read_sql(sql, self.accela)
        # Sum/Total of all columns
        df = df.append(df.sum().rename('Total'))
        df.at["Total", "permittype"] = ""
        df.at["Total", "reviewtype"] = ""
        df.to_excel(self.out_file, index=False)
        return


if __name__ == "__main__":
    engine = AccelaProd.connect()
    pq = PlanningQueue(engine)
    pq.main()
