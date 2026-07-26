import argparse
import csv
import locale
import typing
from concurrent.futures import ThreadPoolExecutor, as_completed


def check_csv(filename: str, encoding: str, delimiter: str) -> tuple[str, bool, str]:
    try:
        with open(filename, encoding=encoding, newline='') as f:
            reader = csv.reader(f, delimiter=delimiter)
            first_len = None
            for line_no, row in enumerate(reader, start=1):
                if first_len is None:
                    first_len = len(row)
                elif len(row) != first_len:
                    message = f'line {line_no}: contains inconsistent columns (expected {first_len}, got {len(row)})'
                    return filename, False, message
    except UnicodeDecodeError:
        return filename, False, f'failed to decode csv text file using {encoding!r}'

    return filename, True, ''


def main(argv: typing.Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--encoding', dest='encoding', default=locale.getpreferredencoding())
    parser.add_argument('-d', '--delimiter', dest='delimiter', default=',')
    parser.add_argument('-j', '--jobs', dest='jobs', type=int, default=8)
    parser.add_argument('filenames', nargs='*', help='Filenames to check.')
    args = parser.parse_args(argv)

    print(f'Checking CSV files using encoding {args.encoding!r} and delimiter {args.delimiter!r}...')
    print(f'Checking {len(args.filenames)} files with {args.jobs} workers...')

    retval = 0
    with ThreadPoolExecutor(max_workers=args.jobs) as executor:
        futures = {
            executor.submit(check_csv, filename, args.encoding, args.delimiter): filename
            for filename in args.filenames
        }
        for future in as_completed(futures):
            filename, ok, msg = future.result()
            if not ok:
                print(f'{filename}: {msg}')
                retval = 1
    return retval


if __name__ == '__main__':
    raise SystemExit(main())
