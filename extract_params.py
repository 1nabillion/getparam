import argparse
import sys
from urllib.parse import urlparse, unquote
from collections import Counter
from beautifultable import BeautifulTable

SEPARATORS = ['&', ';', ',', '|']

def normalize_url(url):
    url = url.strip()
    if not url:
        return None
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    return url


def extract_params_from_url(url):
    parsed = urlparse(url)
    raw_query = parsed.query or ''
    for sep in SEPARATORS:
        raw_query = raw_query.replace(sep, '&')

    params = []
    for segment in raw_query.split('&'):
        if not segment:
            continue
        parts = segment.split('=', 1)
        key = unquote(parts[0])
        if key:
            params.append(key)
    return params


def main():
    parser = argparse.ArgumentParser(description='Extract URL parameter names from a list of URLs')
    parser.add_argument('-f', '--file', required=True, help='Input file with one URL per line')
    parser.add_argument('-o', '--output', required=True, help='Output file to save unique parameter names')
    args = parser.parse_args()

    counter = Counter()
    unique_params = set()

    try:
        with open(args.file, 'r', encoding='utf-8') as f:
            for line in f:
                url = normalize_url(line)
                if not url:
                    continue
                try:
                    params = extract_params_from_url(url)
                except Exception as e:
                    print(f"Warning: could not parse URL '{line.strip()}': {e}", file=sys.stderr)
                    continue
                for p in params:
                    unique_params.add(p)
                    counter[p] += 1
    except FileNotFoundError:
        print(f"Error: input file '{args.file}' not found.", file=sys.stderr)
        sys.exit(1)
    with open(args.output, 'w', encoding='utf-8') as out:
        for param in sorted(unique_params):
            out.write(param + '\n')
    if counter:
        table = BeautifulTable()
        table.columns.header = ["Parameter", "Count"]
        for param, cnt in counter.most_common():
            table.rows.append([param, cnt])
        print(table)
    else:
        print("No parameters found.")

if __name__ == '__main__':
    main()
