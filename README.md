## extract\_params.py

`extract_params.py` is a lightweight Python CLI tool for extracting and analyzing parameter names from a list of URLs.

### Features

* **Customizable separators**: supports parameters separated by `&`, `;`, `,`, and `|`, and can be easily extended to include more.
* **URL normalization & decoding**: detects missing schemes, adds `http://` if needed, and decodes percent-encoded parameter names.
* **Unique output**: writes only one instance of each parameter name to the output file.
* **Usage statistics**: prints a beautiful table (via [`beautifultable`](https://pypi.org/project/beautifultable/)) showing the occurrence count of each parameter.

### Installation

```bash
pip install beautifultable
```

### Usage

```bash
python extract_params.py -f urls.txt -o params.txt
```

* `-f, --file` — input file containing one URL per line.
* `-o, --output` — output file where unique parameter names will be saved (one per line).

After running, the script will:

1. Write all unique parameter names (alphabetically sorted) into `params.txt`.
2. Display a table in the console:

   ```
   +-------------+-------+
   |  Parameter  | Count |
   +-------------+-------+
   | id          | 42    |
   | session     | 17    |
   | utm_source  | 10    |
   +-------------+-------+
   ```

### Advantages

* **Simplicity**: single script, minimal setup.
* **Reliability**: manual parsing avoids false positives.
* **Flexibility**: easy to extend the set of separators and URL formats.
* **Decoding**: automatically decodes percent-encoded parameter names for readability.
* **Visualization**: immediate insight into parameter frequency.
