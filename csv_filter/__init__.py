#!/usr/bin/env python3
import argparse
import csv
import logging
import os
import re
import sys

DELIMITER = ','


class CsvFilter:
    def __init__(
            self, 
            file=None, 
            deduplicate=False, 
            filter=None, 
            filter_inverse=False,
            ignore_case=False, 
            verbose=False,
            delimiter=DELIMITER
    ):
        self.file = file
        self.deduplicate = deduplicate
        self.filter = filter
        self.filter_inverse = filter_inverse
        self.ignore_case = ignore_case
        self.verbose = verbose
        self.delimiter = delimiter
        self.logger = logging.getLogger('deduplicate')
        if self.verbose:
            self.logger.setLevel(logging.DEBUG)

    def apply(self):
        base_path = os.getcwd()
        src_path = base_path + '/' + self.file
        dest_path = src_path.replace('.csv', '.filtered.csv')
        filtered_items = self.filter_items(src_path)
        self.store_items(dest_path, filtered_items)

    def filter_items(self, file_path):
        result = []
        deduplicate_column_index = False
        deduplicate_key_values = []
        filter_column = False
        filter_column_index = False
        filter_pattern = False
        counter = 0
        re_flags = 0

        if self.ignore_case:
            re_flags = re.IGNORECASE

        if self.verbose:
            print('* Filtering file', file_path)

        if self.filter:
            filter_match = re.match('^(.+)=(.+)$', self.filter)
            if filter_match:
                filter_column = filter_match.group(1)
                filter_pattern = filter_match.group(2)

        with open(file_path, 'rt') as csv_file:
            for row in csv.reader(csv_file, delimiter=self.delimiter):
                if counter == 0:
                    if self.deduplicate:
                        deduplicate_column_index = row.index(self.deduplicate)

                    if filter_column:
                        filter_column_index = row.index(filter_column)

                    counter += 1
                    result.append(row)
                    continue

                valid = False

                if self.deduplicate and deduplicate_column_index is not False:
                    value = row[deduplicate_column_index]
                    if self.ignore_case:
                        value = value.lower()
                    if value in deduplicate_key_values:
                        valid = False
                    else:
                        deduplicate_key_values.append(value)

                if filter_column_index is not False:
                    value = row[filter_column_index]
                    if bool(re.match(filter_pattern, value, re_flags)) is not self.filter_inverse:
                        valid = True

                if valid:
                    result.append(row)

                counter += 1

        if self.verbose:
            print('* Filtered', counter, 'items to', len(result))

        return result

    def store_items(self, file_path, items):
        if self.verbose:
            print('* Storing items to', file_path)

        with open(file_path, 'wt') as csvfile:
            writer = csv.writer(csvfile, delimiter=self.delimiter)
            for row in items:
                writer.writerow(row)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', '-f', help='File to filter')
    parser.add_argument('--deduplicate', help='Deduplication column to be applied', default=False)
    parser.add_argument('--filter', help='Filter to be applied', default=False)
    parser.add_argument('--filter_inverse', action='store_true', help='Inverse filter matches', default=False)
    parser.add_argument('--ignore_case', '-i', action='store_true', help='Match values case insensitive', default=False)
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose')
    return parser.parse_args()


def main():
    args = parse_arguments()
    CsvFilter(
        file=args.file,
        deduplicate=args.deduplicate,
        filter=args.filter,
        filter_inverse=args.filter_inverse,
        ignore_case=args.ignore_case,
        verbose=args.verbose
    ).apply()
    return 0


if __name__ == '__main__':
    sys.exit(main())
