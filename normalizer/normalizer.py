#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Frances Hocutt"
__version__ = "0.0.1dev"
__license__ = "GNU GPL v3.0"

import argparse
import csv
from datetime import datetime, timedelta
from io import StringIO
import sys


# TODO: how does argparse handle unicode/bytestrings? Do we need to set
#       PYTHONIOENCODING before running the script or is it ok?
# TODO: replace invalid unicode with unicode replacement char; I think this
#       will just error on loading if it can't figure UTF-8 as it stands?


def pad_zip_code(zipcode):
    """Pad a string to 5 digits by adding zeros to the left.

    Parameters:
        zipcode (str)   string to be padded out

    Returns:
        string padded with up to 5 zeroes
    """
    return zipcode.zfill(5)


def convert_to_seconds(duration_string):
    """Given a string in the form (HH)H:MM:S.MS, convert it to seconds.

    Parameters:
        duration_string (str)   stuff

    Returns:
        string with duration converted to floating-point seconds
    """
    (hours, minutes, seconds) = [float(x) for x in duration_string.split(':')]
    total_seconds = (60 * 60 * hours) + (60 * minutes) + seconds

    # I am not sure about keeping this as a string; makes sense for zip code,
    # may be inconsistent here?
    return str(total_seconds)


def calculate_total_duration(foo_duration_str, bar_duration_str):
    """Calculate TotalDuration from FooDuration and BarDuration.

    Parameters:
        foo_duration (str)  String with FooDuration (a float)
        bar_duration (str)  String with BarDuration (a float)

    Returns:
        str     String with TotalDuration (the sum of FooDuration and
                BarDuration)
    """
    foo_duration = float(foo_duration_str)
    bar_duration = float(bar_duration_str)

    # Again this is a little weird to be doing as strings but I have not
    # checked how the csv writer handles floats - FIXME?
    return str(foo_duration + bar_duration)


def timestamp_to_iso_8601(timestamp_str):
    """Given a timestamp like '4/1/11 11:11:11 AM', format it in ISO 8601.

    Currently missing timezone information.
    """
    pac_datetime = datetime.strptime(timestamp_str, '%m/%d/%y %I:%M:%S %p')

    # This is a hack and I wouldn't be surprised if there is some horrible
    # corner case it fails on - probably daylight savings
    atl_datetime = pac_datetime + timedelta(hours=3)

    # FIXME: this is not actually the correct format because it is missing the
    # UTC offset. Use pytz or maybe arrow to handle time zone properly.
    return atl_datetime.isoformat()


def uppercase_name(name):
    """Convert a given string to uppercase."""
    return name.upper()  # should handle anything with upper defined in unicode


def normalize_csv_row(row):
    # TODO: Docstring, tests

    normalized_row = {}

    normalized_bar_duration = convert_to_seconds(row['BarDuration'])
    normalized_foo_duration = convert_to_seconds(row['FooDuration'])
    normalized_total_duration = calculate_total_duration(
        normalized_foo_duration, normalized_bar_duration)
    normalized_zip = pad_zip_code(row['ZIP'])
    normalized_full_name = uppercase_name(row['FullName'])
    normalized_timestamp = timestamp_to_iso_8601(row['Timestamp'])

    normalized_row = {'Notes': row['Notes'],
                      'Address': row['Address'],
                      'BarDuration': normalized_bar_duration,
                      'FooDuration': normalized_foo_duration,
                      'TotalDuration': normalized_total_duration,
                      'ZIP': normalized_zip,
                      'FullName': normalized_full_name,
                      'Timestamp': normalized_timestamp}

    return normalized_row


def normalize_csv_fields(rows_to_normalize):
    # TODO: Docstring, tests

    normalized_csv_data = []
    for row in rows_to_normalize:
        try:
            new_row = normalize_csv_row(row)
            normalized_csv_data.append(new_row)
        except Exception as e:  # FIXME: overly broad, bad idea
            print(e, file=sys.stderr)
    return normalized_csv_data


def write_csv(csv_dicts):
    # TODO: docstring, tests

    fieldnames = ['Timestamp', 'Address', 'ZIP', 'FullName', 'FooDuration',
                  'BarDuration', 'TotalDuration', 'Notes']
    with sys.stdout as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in csv_dicts:
            writer.writerow(row)


def read_csv(input_string):
    # TODO: docstring, tests
    buff = StringIO(input_string)
    rows = []
    reader = csv.DictReader(buff)
    for row in reader:
        rows.append(row)
    return rows


def main(args):
    # TODO: docstring, tests
    # TODO: make able to read from stdin, not argv[1]

    csv_input = args.csv_input

    # read CSV
    loaded_csv = read_csv(csv_input)

    # normalize CSV
    normalized_csv = normalize_csv_fields(loaded_csv)

    # write CSV
    write_csv(normalized_csv)


if __name__ == "__main__":
    # TODO: document this better
    parser = argparse.ArgumentParser()

    parser.add_argument("csv_input", help="UTF-8 CSV-formatted input string")

    # Specify output of "--version"
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__))

    # TODO: what happens when this gets bad unicode input?
    args = parser.parse_args()
    main(args)
