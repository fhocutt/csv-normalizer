# csv-normalizer

## Summary
This program normalizes CSVs and writes the result to stdout.

## Quickstart
It is recommended to install this in a virtualenv. Make and activate your
virtualenv, then:
```
$ git clone <name>
$ pip install .
```
To run the program, you will currently need to paste in your CSV on the command
line as the first argument. Enclose in single quotes (`'`) to avoid problems
with the double quotes in the files. For example:
```
$ python normalizer/cli.py 'Timestamp,Address,ZIP,FullName,FooDuration,BarDuration,TotalDuration,Notes
4/1/11 11:00:00 AM,"123 4th St, Anywhere, AA",94121,Monkey Alberto,1:23:32.123,1:32:33.123,zzsasdfa,I am the very model of a modern major general
3/12/14 12:00:00 AM,"Somewhere Else, In Another Time, BB",1,Superman übertan,111:23:32.123,1:32:33.123,zzsasdfa,This is some Unicode right here. ü ¡! 😀
2/29/16 12:11:11 PM,111 Ste. #123123123,1101,Résumé Ron,31:23:32.123,1:32:33.123,zzsasdfa,🏳️🏴🏳️🏴''
```

For help on running the program,
```
$ python normalizer/normalizer.py --help
usage: normalizer.py [-h] [--version] csv_input

positional arguments:
  csv_input   UTF-8 CSV-formatted input string

  optional arguments:
    -h, --help  show this help message and exit
      --version   show program's version number and exit

```

To run the automated tests and linter,
```
$ tox
```

## Known Issues

* This currently reads the CSV from sys.argv[1], not sys.stdin.
* This probably does not handle Unicode decode errors with the `'replace'`
  strategy as it should (replacing unreadable characters with the Unicode
  Replacement Character). I'm not sure whether it's possible to tell argparse
  to handle it that way or whether something else will be needed.
* This does not handle time zones properly, and the normalized timestamp string
  is not actually ISO-8601 because it lacks time zone information.
* The tests and documentation are badly lacking. Most of the individual field
  normalization methods have unit tests; the rest doesn't. Docstrings should
  look roughly like the ones for the field normalization functions.
* The error handling is overly broad but I'm blanking on the right exception
  categories and I'm way past time.
* It would be nice to have the script entry point defined so that we don't need
  to call this with the full path.
* It would be nice to add type annotations with mypy for type checking.
