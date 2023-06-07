# edens_interface

**Author:** Garin Wally  
**Date:** 5/1/2023

## Description

The `edens_interface` script aims to replicate the functionality of
an `.exe` file provided by TylerTechnologies (Edens) that was used before Accela was migrated to the cloud. It retrieves payment data from the Accela database and generates a report in a pipe-delimited format for importing into Edens. The script connects to the database, executes an SQL query, processes the results, exports the report to a file, and sends it via email.


## Prerequisites

- Python 3.11
- Custom Python packages:
  * `reportutils`
  * `emailer`
  * `logger`
  * `dbconnections`



## Usage

This script is primarily executed from Task Scheduler executing the `scheduled_daily.bat` script. It passes no arguments.

It can also be executed from the command-line. This method might be used for any range of dates where the script failed. Execute with:

`python edens_interface.py <start_date> <end_date>`

If no arguments are provided, the script will use yesterday's date as
the start date and today's date as the end date. The data has a less-than relationship to the end_date argument.


## Configuration

- **DEBUG Mode**: By default, email functionality is enabled (will send). Set the `DEBUG`
variable to `True` in the script to disable email functionality for debugging purposes.
