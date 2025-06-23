#!/usr/bin/env python3
import argparse
import re
from urllib.parse import urlparse, unquote_plus
from collections import Counter
from beautifultable import BeautifulTable

def normalize_url(url: str) -> str:
    if not re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*://', url):
        return 'http://' + url
    return url

def extract_keys_from_url(url: str, sep_pattern: str) -> list[str]:
    query = urlparse(url).query
    query = re.sub(sep_pattern, '&', query)
    keys = []
    for segment in query.split('&'):
        if not segment:
            continue
        key, *_ = segment.split('=', 1)
        key = unquote_plus(key)
        if re.fullmatch(r'[A-Za-z0-9_-]+', key):
            keys.append(key)
    return keys

def main():
    parser = argparse.ArgumentParser(description="Extract unique URL parameter names and their counts.")
    parser.add_argument('-f', '--file', required=True, help="Input file with one URL per line")
    parser.add_argument('-o', '--output', required=True, help="Output file for unique parameter names")
    args = parser.parse_args()
    counter = Counter()
    sep_pattern = r'[;,|]'  

    with open(args.file, 'r', encoding='utf-8') as fin:
        for line in fin:
            url = line.strip()
            if not url:
                continue
            url = normalize_url(url)
            keys = extract_keys_from_url(url, sep_pattern)
            counter.update(keys)

    with open(args.output, 'w', encoding='utf-8') as fout:
        for key in sorted(counter):
            fout.write(f"{key}\n")

    table = BeautifulTable()
    table.column_headers = ["Parameter", "Count"]
    for key, cnt in counter.most_common():
        table.append_row([key, str(cnt)])
    print(table)

if __name__ == "__main__":
    main()
