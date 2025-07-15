````markdown
# VoidTrace - Advanced Recon Tool

VoidTrace is a powerful and easy-to-use Python recon tool designed for subdomain enumeration, port scanning, WHOIS lookups, and more. It supports multi-threading, customizable port ranges, and outputs results in JSON or text formats.

---

## Features

- Subdomain enumeration with customizable wordlist  
- Multi-threaded port scanning with port range or list  
- WHOIS lookup for domain information  
- Save reports as JSON or text  
- Interactive CLI prompts for missing arguments  
- Color-coded terminal output for easy reading  

---

## Table of Contents

- [Installation](#installation)  
- [Cloning the Repository](#cloning-the-repository)  
- [Generating a Wordlist](#generating-a-wordlist)  
- [Usage](#usage)  
- [Command Line Arguments](#command-line-arguments)  
- [Requirements](#requirements)  
- [License](#license)  

---

## Installation

### 1. Clone the Repository

Open your terminal or command prompt and run:

```bash
git clone https://github.com/yourusername/VoidTrace.git
cd VoidTrace
````

### 2. Create and Activate a Virtual Environment (Recommended)

```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

---

### 3. Install Dependencies

VoidTrace requires several Python packages listed in `requirements.txt`. Install them with:

```bash
pip install -r requirements.txt
```

---

## Generating a Wordlist for Subdomain Enumeration

VoidTrace uses a wordlist file to brute-force subdomains of the target domain.

### Option 1: Use Provided Sample

A sample wordlist `subdomains.txt` is included in the repository, which contains common subdomain prefixes.

### Option 2: Create Your Own Wordlist

You can create a custom wordlist using any text editor or by downloading publicly available lists, e.g.:

* [SecLists Subdomain Wordlist](https://github.com/danielmiessler/SecLists/blob/master/Discovery/DNS/subdomains-top1million-5000.txt)

Save the wordlist file in the project folder or specify the full path when running VoidTrace.

---

## Usage

Run the recon tool using the following command:

```bash
python void.py <target> [options]
```

### Example

```bash
python void.py example.com -p 80,443,8080 -t 50 -w subdomains.txt --json
```

This will scan ports 80, 443, and 8080 with 50 threads, enumerate subdomains from `subdomains.txt`, perform WHOIS lookup, and save the report as a JSON file.

---

## Command Line Arguments

| Argument          | Description                                | Default          |
| ----------------- | ------------------------------------------ | ---------------- |
| `<target>`        | Target domain or IP (required)             | -                |
| `-p, --ports`     | Ports to scan (e.g. `1-1000` or `80,443`)  | `1-1000`         |
| `-t, --threads`   | Number of concurrent threads               | `100`            |
| `-w, --wordlist`  | Path to subdomain wordlist                 | `subdomains.txt` |
| `--json`          | Save output report as JSON instead of text | False            |
| `--no-whois`      | Skip WHOIS lookup                          | False            |
| `--no-subdomains` | Skip subdomain enumeration                 | False            |

---

## Requirements

VoidTrace requires Python 3.6 or higher and the following packages:

* `argparse`
* `socket`
* `whois`
* `requests`
* `threading`
* `tqdm`
* `colorama`

These are all included in the `requirements.txt`. Install them using:

```bash
pip install -r requirements.txt
```

## 💰 Donations

Support the project with Bitcoin donations:

```
bc1qlpw590fkykfdd9v92g9snfmx8hc8vwxvkz5npm

```

## Support

If you find any issues or want to contribute, please open an issue or submit a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Disclaimer

Use this tool responsibly and only on systems you own or have explicit permission to test.

---

**Happy Recon!** 👾
