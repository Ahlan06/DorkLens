# DorkLens - Advanced Google Dork Scanner

**Advanced Google Dork Scanner v2.0**

*By Ahlan06 - Use responsibly and legally only*

[![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20|%20Linux%20|%20macOS-lightgrey.svg)](https://github.com/Ahlan06/DorkLens)

---

## Table of Contents

- [About](#about)
- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Output Formats](#output-formats)
- [Security and Ethics](#security-and-ethics)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## About

**DorkLens** is an advanced Google Dork scanner designed to automate the search for sensitive information and potential vulnerabilities using the Google Custom Search API. This tool is intended for cybersecurity professionals, security researchers, and penetration testers for legal and authorized activities.

### Legitimate Use Cases:
- **Bug Bounty** authorized programs
- **Penetration testing** with written authorization
- **Security audits** on your own domains
- **Academic research** in cybersecurity
- **Security training** and education

---

## Features

### Core Features:
- **Automatic rotation** of Google API keys
- **Intelligent filtering** of false positives
- **Multiple output formats** (TXT, JSON, CSV)
- **Automatic retry** with exponential backoff
- **Robust error handling**
- **Parallelized query processing**
- **Real-time progress tracking**
- **Automatic duplicate removal**
- **Enriched metadata** (title, snippet, query)

### Advanced Features:
- **Sample generation** of Google Dorks
- **Configurable delays** between requests
- **Graceful interruption** (Ctrl+C) with save
- **Automatic validation** of API keys
- **Detailed logging** of operations

---

## Installation

### Prerequisites
- Python 3.6 or higher
- Valid Google Custom Search API keys
- Stable Internet connection

### 1. Clone the project
```bash
git clone https://github.com/Ahlan06/DorkLens.git
cd DorkLens
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. API Keys Configuration
Edit the `dorklens.py` file and replace the API keys with yours:

```python
API_KEYS = [
    "YOUR_FIRST_GOOGLE_API_KEY",
    "YOUR_SECOND_GOOGLE_API_KEY"
]
CX = "YOUR_CUSTOM_SEARCH_ENGINE_ID"
```

---

## Configuration

### Getting Google API Keys

#### 1. **Google Custom Search API Key**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the "Custom Search API"
4. Generate an API key in "Credentials"

#### 2. **Custom Search Engine ID (CX)**
1. Visit [Google Custom Search Engine](https://cse.google.com/cse/)
2. Create a new search engine
3. Configure to search "The entire web"
4. Copy the search engine ID (CX)

### File Structure

```
DorkLens/
├── dorklens.py              # Main script
├── README.md                # Documentation
├── requirements.txt         # Python dependencies
├── sample_dorks.txt         # Google Dorks examples
├── exclude_domains.txt      # Domains to exclude (optional)
└── results/                 # Results folder (auto-created)
    ├── dork_results.txt
    ├── dork_results.json
    └── dork_results.csv
```

---

## Usage

### Basic Usage

```bash
# Generate a sample Google Dorks file
python dorklens.py --generate-sample

# Basic scan with dorks file
python dorklens.py --dorks sample_dorks.txt --output results.txt

# Scan with JSON format
python dorklens.py --dorks sample_dorks.txt --format json --output results.json
```

### Advanced Options

```bash
# Scan with custom parameters
python dorklens.py \
    --dorks my_dorks.txt \
    --output custom_results.csv \
    --format csv \
    --max-results 100 \
    --delay 2.0 \
    --exclude exclude_domains.txt
```

### Available Arguments

| Argument | Description | Default | Example |
|----------|-------------|---------|---------|
| `--dorks` | File containing Google Dorks | Required | `queries.txt` |
| `--output` | Output file | `dork_results.txt` | `results.json` |
| `--format` | Output format (txt/json/csv) | `txt` | `json` |
| `--max-results` | Max results per query | `50` | `100` |
| `--delay` | Delay between requests (seconds) | `1.0` | `2.5` |
| `--exclude` | File with domains to exclude | Optional | `exclude.txt` |
| `--generate-sample` | Generate a sample file | - | - |

---

## Output Formats

### TXT Format (Default)
```
# DorkLens Results - Generated on 2025-10-26 14:30:45
# Total results: 25

URL: https://example.com/admin/config.php
Title: Configuration File - Admin Panel  
Query: filetype:php "config" "password"
Snippet: Configuration file containing database credentials...
--------------------------------------------------------------------------------
```

### JSON Format
```json
{
  "timestamp": "2025-10-26 14:30:45",
  "total_results": 25,
  "results": [
    {
      "url": "https://example.com/admin/config.php",
      "title": "Configuration File - Admin Panel",
      "snippet": "Configuration file containing...",
      "query": "filetype:php \"config\" \"password\""
    }
  ]
}
```

### CSV Format
```csv
URL,Title,Snippet,Query
https://example.com/admin/config.php,Configuration File,Configuration file...,filetype:php "config"
```

---

## Security and Ethics

### Important Warnings

> **CAUTION**: This tool should only be used within a legal and ethical framework. Unauthorized use may violate cybersecurity and data protection laws.

### Best Practices
- **Always obtain written authorization** before scanning third-party domains
- **Respect the Terms of Service** of Google and target sites
- **Use appropriate delays** to avoid server overload
- **Report vulnerabilities** responsibly
- **Document your activities** for legal justification

### Built-in Limitations
- Automatic filtering of sensitive domains
- Mandatory delays between requests
- Result count limitations
- API key rotation to prevent abuse

---

## Examples

### Common Google Dorks

```bash
# Exposed configuration files
filetype:env "DB_PASSWORD"
filetype:conf "password" | "passwd"
filetype:sql "INSERT INTO" "password"

# Administration pages
inurl:admin intitle:login
inurl:wp-admin "dashboard"
intitle:"phpMyAdmin" "Welcome to phpMyAdmin"

# Exposed directories
intitle:"index of /" "parent directory"
intitle:"Apache2 Ubuntu Default Page"

# Revealing error messages
intext:"sql syntax near" | intext:"syntax error"
intext:"Warning: mysql_connect()"
intext:"Fatal error" "Call to undefined function"

# Sensitive documents
filetype:pdf "confidential" | "internal use only"
filetype:doc "password" | "credential"
```

### Domain-targeted Searches

```bash
# Scan a specific domain
site:example.com filetype:sql
site:example.com intitle:"index of"
site:example.com "password" filetype:txt

# Exclude certain subdomains
site:example.com -site:blog.example.com filetype:log
```

---

## Troubleshooting

### Common Errors

#### **"API key quota exceeded"**
- **Solution**: Add more API keys or wait for quota reset
- **Prevention**: Use longer delays (`--delay 2.0`)

#### **"No results found"**
- **Cause**: Queries too specific or domains filtered
- **Solution**: Check your Google Dorks and exclusion list

#### **"Request timeout"**
- **Cause**: Unstable Internet connection
- **Solution**: Check your connection and increase delay

### Performance Optimization

```bash
# Fast mode (risk of rate limiting)
python dorklens.py --dorks queries.txt --delay 0.5 --max-results 30

# Stealth mode (slower but safer)
python dorklens.py --dorks queries.txt --delay 3.0 --max-results 20
```

---

## Contributing

### How to Contribute

1. **Fork** the project
2. Create a **feature branch** (`git checkout -b feature/enhancement`)
3. **Commit** your changes (`git commit -m 'Add new features'`)
4. **Push** to the branch (`git push origin feature/enhancement`)
5. Open a **Pull Request**

### Reporting Bugs

Use [GitHub Issues](https://github.com/Ahlan06/DorkLens/issues) with:
- Detailed problem description
- Steps to reproduce
- Environment (OS, Python version)
- Error logs

### Enhancement Suggestions

- Web interface (Flask/FastAPI)
- Database support
- Integration with other security tools
- Advanced stealth mode with proxies
- HTML/PDF report generation

---

## Changelog

### v2.0.0 (2025-10-26)
- Automatic retry with exponential backoff
- JSON and CSV support
- Duplicate removal
- Sample dorks generation
- API keys validation
- Graceful interruption handling

### v1.0.0 (Initial)
- Basic Google Dork scanner
- API keys rotation
- Domain filtering
- Simple TXT output

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- **Google Custom Search API** for the search API
- **Cybersecurity community** for Google Dorks
- **Testers and contributors** for their feedback

---

## Contact

- **Author**: Ahlan Mira
- **GitHub**: [@Ahlan06](https://github.com/Ahlan06)
- **Project**: [DorkLens Repository](https://github.com/Ahlan06/DorkLens)

---

**Disclaimer: This tool is intended solely for educational purposes and authorized testing. The author is not responsible for malicious use of this tool.**

**Always use responsibly and comply with applicable laws.**
