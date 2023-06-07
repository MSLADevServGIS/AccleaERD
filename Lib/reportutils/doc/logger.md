# `logger.py`

The `logger.py` module provides a convenient way to log messages to a file. It is configured to write `.log` messages to a `log` folder within your project folder structure. Also pre-configured for your convienence is the formatting and file naming.

## Usage
Import the utility near the top of the script, like so:
```python
from reportutils import make_logger
```

Then use the function to create a logging object by providing the `__file__` global variable to pass the absolute path of the calling script.

```python
logger = make_logger(__file__)
```

Then, anytime you wish to log a message, simply use a method of that "severity" to log the message. There are a handful to choose from:
* DEBUG
* INFO
* WARN
* ERROR
* CRITICAL

 For instance:

```python
# Debug
logger.debug("This message won't get written to the file...")
logger.debug("...unless it is set to log this low of a level.")

# Info
logger.info("This is a message of severity: INFO")
logger.info("This is the most common method for logging messages")

# Warning
logger.warn("This is a message of severity: WARN")

# Error
logger.error("This is a message of severity: ERROR")

# Critical
logger.critical("This is a message of severity: CRITICAL")
```