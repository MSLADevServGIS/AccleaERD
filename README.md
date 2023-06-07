# AccelaERD
This project holds all important reports and supporting libraries/modules for the AccelaERD server and can be found in `C:/workspace/`.  

## Explanation of folder contents:
* README.md -- If you're reading this document, than you are already familiar with this MarkDown file!
* .gitignore -- This file tells git to ignore certain files such as the .env and .log files
* /Lib -- This directory contains custom libraries/modules that support Report/Model functionality
  * Set this directory to the PYTHONPATH environment variable so it's contents can be imported by Python scripts
* /reports -- This directory contains reports and execution scripts (.bat files) for them (more below)


## Reports
This 'reports' folder is intended to manage reports that:  
* Are not needed "within reach" such as those reports executed by buttons in the Accela user interface
* May or may not email their outputs to specific users
* Are scheduled for automatic execution to produce refreshed data on intervals

### Scheduling reports
Use Microsoft Task Scheduler to execute the .bat files for the appropriate interval.  
Each .bat file should contain a command-line script that controls the execution of Python scripts.  
