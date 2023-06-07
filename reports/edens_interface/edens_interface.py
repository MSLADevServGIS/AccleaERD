"""edens_interface: Accela Payments for Edens
Author: Garin Wally; 5/1/2023

This report is my best approximation to reproduce the results of an
.exe file probably made by TylerTechnologies (Edens).
It runs daily to produce a pipe-delimited file used to import the
previous day's payment data from Accela into Edens.
"""
import datetime as dt
from dateutil.parser import parse as parse_date
from pathlib import Path

from dbconnections import AccelaProd, AccelaNonProd1
from reportutils import Emailer, ErrorEmail, Report, make_arg_parser, make_logger


# The master switch for turning email-sending on (False, default) or off (True)
# True will override any value passed to args.debug
DEBUG = False

today = dt.date.today()
yesterday = (today - dt.timedelta(days=1))
dt_fmt = "%m/%d/%Y"


# Setup command-line arguments
parser = make_arg_parser()

# Example using all args: `python myscript --start "01/01/20X6" --end "01/02/20X6" --debug`
parser.add_argument(
    "--start",
    default=yesterday.strftime(dt_fmt),
    help="Start date for data range"
    )

parser.add_argument(
    "--end",
    default=today.strftime(dt_fmt),
    help="Start date for data range"
    )

args = parser.parse_args()
# Override whatever value was passed to args.debug if DEBUG is True
if DEBUG and args.debug is not DEBUG:
    args.debug = DEBUG


# Setup logger
logger = make_logger(__file__, args.debug)


# Setup email
logger.info("Initializing emailer...")
emailer = Emailer(__file__, "email.toml")
emailer.set_debug(args.debug)  # Only send emails if the DEBUG variable is False
logger.info("  Done.")


# Setup Report
logger.info("Initializing Report...")


# Customize the .process() method to format date dd/mm/yyyy
class EdenReport(Report):
    def process(self):
        df = self.result.copy()
        df["DATE_PAYMENT"] = df["DATE_PAYMENT"].apply(
            # Format the datetime correctly
            lambda x: x.strftime(dt_fmt)
        )
        df["FEE_AMOUNT_ASSESSED"] = df["FEE_AMOUNT_ASSESSED"].apply(
            # Ensure float(x), format with 2 decimals, indent 12 spaces
            lambda x: f"{x:.2f}".format(float(x)).rjust(12)
        )
        self.result = df
        return


# Instantiate the report
edens_rpt = EdenReport(
    __file__,
    "accela_payments.sql",
    logger,
    ext=".txt",
    sep="|",
    header=False
    )

logger.info("  Done.")


def main():
    """Controls the execution of the report."""
    try:
        # ===== Report Inputs =====
        logger.info("Setting inputs...")
        # The 'argv' allows for arguments passed in by the command line
        # This feature is clutch for running this script for specific dates
        edens_rpt.set_input(
            "start_date",
            args.start
            )
        edens_rpt.set_input(
            "end_date",
            args.end
        )
        logger.info(f"  Inputs: {edens_rpt.inputs}")

        # ===== DB Connection =====
        logger.info("Establishing database connection...")
        # Comment/Uncomment the line for the desired database (default is AccelaProd)
        edens_rpt.connect(AccelaProd)  # Production database
        #edens_rpt.connect(AccelaNonProd1)  # Development/NonProduction database
        logger.info(f"  Connected to {edens_rpt.engine.url}")

        # ===== Execute Report =====
        logger.info("Running report...")
        edens_rpt.execute()
        edens_rpt.process()
        logger.info("  Done.")

        # ===== Export Results =====
        logger.info("Exporting results...")
        edens_rpt.save()
        logger.info(f"  Rows exported: {len(edens_rpt.result)}")

        # ===== Email Results =====
        logger.info("Emailing results...")
        emailer.body = emailer.body.format(
            date=edens_rpt._inputs["start_date"]
            )
        emailer.build()
        emailer.attach(str(edens_rpt.output))
        logger.info(f"  To: {emailer.to}")
        # TODO: support cc and bcc
        sent = emailer.send()
        if sent:
            logger.info("  Sent.")
        else:
            logger.info("  Not sent.")

        logger.info(f"Completed {edens_rpt.name}\n")

    except Exception as e:  # TODO: Untested
        # If an error occurs, log it first
        logger.error(e)
        # Then email the log file to the author/programmer
        error_email = ErrorEmail(__file__, str(logger.logfile))
        error_email.send()
        raise e


if __name__ == "__main__":
    main()
