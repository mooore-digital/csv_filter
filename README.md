# CSV Filter (alpha)
Written in python, this program is a command-line interface, providing the ability to mutate data in a CSV file when spreadsheet applications lack functionality.

## Usage
For now, calling the program looks a bit rough, but it gets the job done.

You can call the program this way:
`python csv_filter/__init__.py`

- **--file/-f**: Specify file to filter
- **--deduplicate/-d** (optional): Specify deduplication column
- **--filter** (optional): Specify filter column and regex pattern
- **--filter_inverse** (optional): Inverse filter matches
- **--ignore_case/-i** (optional): Enable case insensitivity
- **--verbose/-v** (optional): Enable verbose output

## Examples

#### Deduplicating rows based on a column uniqueness
`python csv_filter/__init__.py --file export.csv --deduplicate=email -i -v`

#### Filter rows based on a regex
`python csv_filter/__init__.py --file export.csv --filter "_address_country_id=(NL|BE)" -i -v`

## Issue reporting/contributing
This program is in it's very early stages. If you encounter problems or have suggestions, please create a ticket or a pull request.
