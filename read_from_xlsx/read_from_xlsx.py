"""
Tutorial on how to go from data in an excel spreadsheet to indico powered analyses

Setup Guide:
1. Follow the setup instructions here: https://indico.io/blog/getting-started-indico-tutorial-for-beginning-programmers/
2. Install xlrd by running `pip install xlrd`
"""

import sys, argparse
from operator import attrgetter
from pprint import pprint

import csv
import xlrd
from itertools import izip
import indicoio
indicoio.config.api_key = "YOUR_API_KEY_HERE"

def _get_sheet(book, args):
    # Both sheet and sheet number provided
    if args.sheet and args.sheet_number:
        print ("Warning: Provided both sheet name and sheet number. Ignoring sheet number.")

    if not args.sheet and not args.sheet_number:
        print("Warning: Neither sheet nor sheet number were provided. Using the first sheet by default")
        return book.sheet_by_index(0)

    # Provided sheet does not exist
    if args.sheet and args.sheet not in book.sheet_names():
        print("ERROR: {sheet_name} not found in {filename}".format(
            sheet_name=sheet_name,
            filename=args.filename
        ))
        sys.exit(1)

    # Provided sheet number is not valid
    if args.sheet_number and args.sheet_number > book.nsheets:
        print("ERROR: cannot get sheet {num}. {filename} only has {avail} sheets".format(
            num=args.sheet_number,
            avail=book.nsheets,
            filename=args.filename
        ))
        sys.exit(1)

    return book.sheet_by_name(args.sheet)

def parse_from_xlsx(args, batch_size=20):
    book = xlrd.open_workbook(args.filename)
    sheet = _get_sheet(book, args)
    data = sheet.col(args.column or 0)
    for idx in xrange(1 if args.contains_header else 0, len(data), batch_size):
        yield map(attrgetter("value"), data[idx: idx + batch_size])

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')

    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str, help="path to excel file")
    parser.add_argument("--sheet", type=str, help="sheet name")
    parser.add_argument("--sheet-number", type=int, help="sheet index from 1")
    parser.add_argument("--column", type=int, help="column index from 1")
    parser.add_argument("--contains-header", action="store_true", help="use if columns have headers")

    args = parser.parse_args()
    with open("predictions.csv", "wb") as f:
        writer = csv.writer(f, dialect="excel")
        for lines in parse_from_xlsx(args):
            not_empty, inputs = zip(*[row for row in enumerate(lines) if row[1].strip()])
            predictions = indicoio.emotion(list(inputs))
            output = [[str(predictions.pop(0))] if idx in not_empty else "" for idx in xrange(len(lines))]
            writer.writerows(izip(inputs, output))

    print "Analysis complete, CSV file generated."
