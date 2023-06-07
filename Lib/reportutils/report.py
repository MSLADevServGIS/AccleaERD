"""Report Utils / report.py: Report object
Author: Garin Wally; 5/1/2023

Defines the Report object for executing SQL queries against a database,
handling the query execution, result processing and saving.

The Report object encapsulates the following functionalities:
- Execution of SQL queries and retrieval of results as a Pandas DataFrame.
- Parsing of SQL queries for input parameters and mapping them to keyword
    arguments.
- Dynamic generation of output file paths based on the current timestamp.
- Connection establishment to the database using a provided ConnectionInfo
    object.
- Saving the query results to output files in CSV or Excel format.
- Customizable processing methods for additional data manipulations.

Other report-related projects can import and utilize this object to
streamline SQL query execution and result handling.
"""

import datetime as dt
import re
from io import StringIO
from pathlib import Path

import pandas as pd


class Report:
    """A Report handles the SQL execution and post-processing."""
    def __init__(self, filepath, sqlfile, logger=None, **kwargs):
        # The Abspath for the Python file; use __file__
        self.file = Path(filepath)
        # The folder that contains the Python file
        self.basepath = self.file.parent
        # The Python script's formatted name, used for naming outputs
        self.name = self.file.name.split(".")[0].replace("_", " ").title()
        # The path to the SQL file
        self.sqlpath = self.basepath.joinpath("sql", sqlfile)
        # The path to the output folder
        self.outpath = self.basepath.joinpath("outputs")

        # A dict that will store input parameters used by the SQL script
        self._inputs: dict = {}
        self.engine = None
        self.logger = logger
        self.kwargs: dict = kwargs
        self.result: pd.DataFrame|None = None

    @property
    def sql(self) -> str:
        """Read and return the contents of the SQL file."""
        # This as a property might duplicate some processes, but is
        #  convient for changing out the SQL file content after the
        #  object has been initialized.
        with self.sqlpath.open() as f:
            q = f.read()
        return q

    @property
    def inputs(self) -> dict:
        """Parse SQL for input parameters and map to kwargs."""
        inpts = {i: self._inputs[i] for i
                 in re.findall("\{(.*?)\}", self.sql)}
        return inpts

    @property
    def output(self) -> Path:
        """Dynamically produces the output file path."""
        outname = dt.datetime.now().strftime(
            f"{self.name}-%Y%m%d%H%M" + self.kwargs.get("ext", ".xlsx")
            )
        return self.outpath.joinpath(outname)

    def connect(self, ConnectionInfo) -> None:
        """Connect to the db using info from the ConnectionInfo object."""
        self.engine = ConnectionInfo.connect()
        return

    def execute(self) -> pd.DataFrame:
        """Executes the SQL file with (optional) inputs."""
        self.result = pd.read_sql(
            # Format the SQL script with optional inputs
            self.sql.format(**self.inputs),
            # The database connection to use to run the SQL
            self.engine
            )
        return self.result

    def process(self) -> None:
        """Placeholder for a more customizable method."""
        # Can be overridden as needed to provide post-processing functionality
        return

    def save(self) -> None:
        """Saves the results to the output path."""
        # Set the default export function to to_csv, unless the 'ext' kwarg is .xlsx
        if self.kwargs.get("ext") != ".xlsx":
            self.result.to_csv(
                self.output,
                # Set the [sep]erator character
                sep=self.kwargs.get("sep", ","),
                # Turn on/off column names
                header=self.kwargs.get("header", True),
                # Don't include pandas-provided row numbers
                index=False
            )
        else:
            self.result.to_excel(
                self.output,
                index=False
                )
        return

    def save_to_sheet(self, excel_thing, sheet_name: str) -> None:
        """Save the data to a specific sheet in an Excel file."""
        pass  # TODO: will allow saving outputs to individual sheets in a shared Excel file

    def set_input(self, key, value) -> None:
        self._inputs[key] = value
        return
