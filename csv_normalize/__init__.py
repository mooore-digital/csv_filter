#!/usr/bin/env python
import argparse
import csv
import os
import re
import sys

DELIMITER = ','


class CsvNormalize:
    def __init__(self, file=None, verbose=False, delimiter=DELIMITER):
        self.file = file
        self.verbose = verbose
        self.delimiter = delimiter

    def apply(self):
        base_path = os.getcwd()
        src_path = base_path + '/' + self.file
        dest_path = src_path.replace('.csv', '.normalized.csv')
        normalized_items = self.normalize_items(src_path)
        self.store_items(dest_path, normalized_items)

    def normalize_items(self, file_path):
        result = []
        counter = 0
        with open(file_path, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=self.delimiter)
            for row in reader:
                if counter == 0:
                    normalize_header_columns(row, self.verbose)
                else:
                    normalize_row(row)

                result.append(row)
                counter += 1
        return result

    def store_items(self, file_path, items):
        if self.verbose:
            print '* Storing items to', file_path

        with open(file_path, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter=self.delimiter)
            for row in items:
                writer.writerow(row)


def normalize_header_columns(row, debug=False):
    for i in range(0, len(row)):
        column = row[i].decode('UTF-8')
        column = column.lower()
        column = re.sub('[\W]', '_', column, flags=re.IGNORECASE | re.UNICODE)
        column = re.sub('[_]{2,}', '_', column, flags=re.UNICODE)
        column = column.strip('_')
        if debug:
            print column, '\t', row[i]
        row[i] = column.encode('UTF-8')
    return row


def normalize_row(row):
    return row


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', '-f', help='File to filter')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose')
    parser.add_argument('--delimiter', '-d', help='CSV delimiter', default=DELIMITER)
    return parser.parse_args()


def main():
    args = parse_arguments()
    CsvNormalize(file=args.file, verbose=args.verbose, delimiter=args.delimiter).apply()


if __name__ == '__main__':
    sys.exit(main())
