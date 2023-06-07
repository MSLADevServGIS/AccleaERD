"""argparser.py - Command-line Argument Parsing Utilities.
Author: Garin Wally; 5/26/2023

Indended to handle boilerplating for supporting arguments.
The `make_arg_parser` function provides a way for pre-configured argparse parsers
between all projects.

Use:
```
from reportutils import make_arg_parser

# Initialize the parser object
parser = make_arg_parser()

# Add script-specific arguments as needed
parser.add_argument(...)

# Create an object that stores the arguments
args = parser.parse_args()

# Use the arguments
print(args.debug)
```
"""
import argparse


def make_arg_parser(debug_help="Enable debug mode"):
    """Provides a convenience function for making a pre-configured command-line argument parser."""
    # Initialize a parser object
    parser = argparse.ArgumentParser()
    
    # Default arguments
    # --debug: enables a flag that is False by default (and when not used), or True when set
    parser.add_argument("--debug", action="store_true", default=False, help=debug_help)
    # Use: `python myscript --debug` -> sets args.debug to True
    
    return parser
