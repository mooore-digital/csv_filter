#!/usr/bin/env python
import argparse
import csv
import logging
import os
import re
import sys

DELIMITER = ','


class CsvFilter:
    def __init__(
            self, file=None, deduplicate=False, filter=None, case_insensitive=False, verbose=False,
            delimiter=DELIMITER
    ):
        self.file = file
        self.deduplicate = deduplicate
        self.filter = filter
        self.case_insensitive = case_insensitive
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

        if self.case_insensitive:
            re_flags = re.IGNORECASE

        if self.verbose:
            print '* Filtering file', file_path

        with open(file_path, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=self.delimiter)
            for row in reader:
                if counter == 0:
                    if self.deduplicate:
                        deduplicate_column_index = row.index(self.deduplicate)
                    if self.filter:
                        filter_match = re.match('^(.+)=(.+)$', self.filter)
                        if filter_match:
                            filter_column = filter_match.group(1)
                            filter_pattern = filter_match.group(2)
                            filter_column_index = row.index(filter_column)
                    counter += 1
                    result.append(row)
                    continue

                valid = True

                if self.deduplicate and deduplicate_column_index is not False:
                    value = row[deduplicate_column_index]
                    if self.case_insensitive:
                        value = value.lower()
                    if value in deduplicate_key_values:
                        valid = False
                    else:
                        deduplicate_key_values.append(value)

                if self.filter and filter_column_index:
                    value = row[filter_column_index]
                    if not re.match(filter_pattern, value, re_flags):
                        valid = False

                if valid:
                    result.append(row)

                counter += 1

        if self.verbose:
            print '* Filtered', counter, 'items to', len(result)

        return result

    def store_items(self, file_path, items):
        if self.verbose:
            print '* Storing items to', file_path

        with open(file_path, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter=self.delimiter)
            for row in items:
                writer.writerow(row)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', '-f', help='File to filter')
    parser.add_argument('--deduplicate', help='Deduplication column to be applied', default=False)
    parser.add_argument('--filter', help='Filter to be applied', default=False)
    parser.add_argument('--ignore_case', '-i', action='store_true', help='Match values case insensitive', default=False)
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose')
    return parser.parse_args()


def main():
    args = parse_arguments()
    CsvFilter(
        file=args.file,
        deduplicate=args.deduplicate,
        filter=args.filter,
        case_insensitive=args.case_insensitive,
        verbose=args.verbose
    ).apply()
    return 0


if __name__ == '__main__':
    sys.exit(main())
