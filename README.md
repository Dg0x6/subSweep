# SubSweep

SubSweep is a Python tool for discovering subdomains using three powerful sources:

- [SecurityTrails](https://securitytrails.com/)
- [ShrewdEye](https://shrewdeye.app/)
- [Subfinder](https://github.com/projectdiscovery/subfinder)

## 🚀 Features

- Gathers subdomains from multiple sources
- Merges and deduplicates results
- Supports input file with multiple domains
- Saves all results in a single output file

## 🛠 Requirements

- Python 3.6+
- Google Chrome (for Selenium)
- `subfinder` installed and available in your PATH

Install dependencies:

```bash
pip install -r requirements.txt
```

## ⚙️ Usage

```bash
python3 subsweep.py -p domains.txt -o output.txt
```

| Option | Description |
|--------|-------------|
| `-p` or `--path`   | Path to file containing list of domains |
| `-o` or `--output` | Output file to save subdomains |

## 📌 Example

```bash
python3 subsweep.py -p input_domains.txt -o found_subdomains.txt
```

## 🔐 API Key

SecurityTrails API key is hardcoded in the script. You can change it manually in the `subsweep.py` file.

You need to visit this website:
👉 https://securitytrails.com/app/account/credentials
and create an account.
After logging in, go to that page and you will find your API key.
Then, open the script and go to line 11:
```
API_KEY = "api_key_from_securitytrails"
```
Replace "api_key_from_securitytrails" with your actual API key.

## 📄 License

This project is licensed under the MIT License.
