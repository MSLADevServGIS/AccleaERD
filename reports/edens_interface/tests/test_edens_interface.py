"""Tests for Edens-Interface."""

from sys import argv, path

path.append(r"I:\Automation\ApplicationSpecialist_Projects\SoftwarePlan\server\Lib")
from ..report import edens_rpt, Engine


def test_dataframe():
    engine = Engine.connect()
    edens_rpt.inputs = {
        "start_date": "4/28/2023",
        "end_date": "4/29/2023"
    }
    print(edens_rpt.sql)
    edens_rpt.run(engine)
    assert not edens_rpt.result.empty, "Empty dataframe"
    edens_rpt.save()
    assert edens_rpt.output.exists()
