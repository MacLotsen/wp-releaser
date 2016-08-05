# WP-Releaser
Python helper script for refactoring wordpress database url's

# Installation
To install the command you need [setuptools](https://pypi.python.org/pypi/setuptools)

`python setup.py install`

<small>Note that you may need root privileges</small>

# Usage

If you installed the module using setup.py you can simply use `wp-releaser` in the console.
Else you can execute the `wp_releaser.py` with python yourself.

The following options are available:

```

(-s <filename> | --script=<filename>)

(-n <new_url> | --new-url=<new_url>)

(-o <old_url> | --old-url=<old_url>)

(--output=<output_filename>)

```

Though if you don't give any options, you will be prompted the needed information.
