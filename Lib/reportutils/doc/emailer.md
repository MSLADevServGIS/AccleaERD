# `emailer.py`

The `emailer.py` module provides a convenient way to incorporate email notifications into projects, making it easy to send notifications, reports, and other relevant information via email.

## Usage
Import the utility near the top of the script, like so:
```python
from reportutils import Emailer
```

Then initialize an Emailer object by providing the `__file__` global variable to pass the absolute path of the calling script, and a TOML (`.toml`) config file containing the email settings:

```python
emailer = Emailer(__file__, "email.toml")
```

If a `.toml` file isn't supplied, attributes can be set from within the script like so:

```python
emailer.to = "recipient@example.com"
emailer.subject = "Email Subject"
emailer.body = "Email body content"
```

Optionally, attach files to the email:

```python
emailer.attach("/path/to/file1.txt")
emailer.attach("/path/to/file2.csv")
```

Build the email message:

```python
emailer.build()
```

Send the email:

```python
emailer.send()
```
