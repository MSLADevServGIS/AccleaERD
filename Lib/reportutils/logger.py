"""logger.py
Author: Garin Wally; May 9, 2023

This file provides a utility for creating logger objects for logging messages to a file.
"""
import datetime as dt
import logging
from pathlib import Path


def make_logger(filepath, debug=False):
    """Builds a logger object for logging messages to a .log file."""
    # Absolute path of the Python script creating the object
    pth = Path(filepath)
    # The name of the callings script
    script_name = pth.name.split(".")[0]
    # Create a name for the log file, and the full path
    log_file = dt.datetime.now().strftime(f"{script_name}-%Y%m%d%H")
    # If debug mode, name ends with '-debug'
    if debug:
        log_file = log_file + "-debug"
    # Slap '.log' onto the end of the filename
    log_file = log_file + ".log"
    log_path = pth.parent.joinpath("logs").joinpath(log_file)
    # Create the logger object for writing log files
    logger = logging.getLogger(str(filepath))

    # Configure the logger to write to the target log file
    fh = logging.FileHandler(log_path)
    # Set the level(s) -- don't touch! Cause um, ...buggy software? idk...
    if debug:
        logger.setLevel(logging.DEBUG)
        fh.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
        fh.setLevel(logging.INFO)
    # Format handler - this sets the formatting of log messages
    fh.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s"))
    logger.addHandler(fh)
    # Add a non-standard 'logfile' attribute onto the object for accessing output log files
    setattr(logger, "logfile", log_path)
    logger.info("Logger initialized.")
    logger.debug("Debug Mode")  # Will only print if level is DEBUG
    return logger
