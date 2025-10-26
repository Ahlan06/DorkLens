#!/usr/bin/env python3
# DorkLens - Advanced Google Dork Scanner
# By Ahlan06 - Enhanced version

import requests
import time
import argparse
import json
import os
import sys
from urllib.parse import quote_plus
from datetime import datetime
import random

# List of Google API Keys (rotate to bypass query limits)
API_KEYS = [
    "AIzaSyDSYmpwpwmf79fnkjsfa_yx3Y997547PkE", 
    "AIzfkl8981asbf-OWzXvy4DdfdklkadacU4lB7pe-A"
]
CX = "c29125701aqfkBRacd897492"  # Google Custom Search Engine ID

# Default domains to exclude (false positives)
DEFAULT_EXCLUDE_DOMAINS = [
    "bugs.mysql.com", "forum.glpi-project.org", "piwigo.org",
    "stackoverflow.com", "github.com", "pastebin.com", "w3schools.com",
    "mozilla.org", "php.net", "python.org", "apache.org"
]

# Common file extensions for sensitive files
SENSITIVE_EXTENSIONS = [
    "sql", "db", "backup", "bak", "log", "conf", "config", 
    "env", "ini", "xml", "json", "csv", "txt", "doc", "pdf"
]

class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_banner():
    """Print tool banner"""
    banner = f"""
{Colors.HEADER}
██████╗  ██████╗ ██████╗ ██╗  ██╗██╗     ███████╗███╗   ██╗███████╗
██╔══██╗██╔═══██╗██╔══██╗██║ ██╔╝██║     ██╔════╝████╗  ██║██╔════╝
██║  ██║██║   ██║██████╔╝█████╔╝ ██║     █████╗  ██╔██╗ ██║███████╗
██║  ██║██║   ██║██╔══██╗██╔═██╗ ██║     ██╔══╝  ██║╚██╗██║╚════██║
██████╔╝╚██████╔╝██║  ██║██║  ██╗███████╗███████╗██║ ╚████║███████║
╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═══╝╚══════╝
{Colors.ENDC}
{Colors.OKCYAN}Advanced Google Dork Scanner v2.0{Colors.ENDC}
{Colors.WARNING}By Ahlan06 - Use responsibly and legally only{Colors.ENDC}
"""
    print(banner)

def validate_api_keys():
    """Validate that API keys are not default/fake"""
    if not API_KEYS or len(API_KEYS[0]) < 30:
        print(f"{Colors.FAIL}Warning: API keys seem to be fake or invalid.{Colors.ENDC}")
        print(f"{Colors.WARNING}Please replace with valid Google Custom Search API keys.{Colors.ENDC}")
        return False
    return True

def read_domains_from_file(file_path):
    """Read domains to exclude from a file."""
    try:
        with open(file_path, "r", encoding='utf-8') as f:
            domains = [line.strip() for line in f.readlines() 
                      if line.strip() and not line.startswith('#')]
        print(f"{Colors.OKGREEN}Loaded {len(domains)} exclude domains from {file_path}{Colors.ENDC}")
        return domains
    except FileNotFoundError:
        print(f"{Colors.WARNING}Warning: Exclude domains file '{file_path}' not found. Using default exclusions.{Colors.ENDC}")
        return DEFAULT_EXCLUDE_DOMAINS
    except Exception as e:
        print(f"{Colors.FAIL}Error reading exclude domains file: {e}. Using default exclusions.{Colors.ENDC}")
        return DEFAULT_EXCLUDE_DOMAINS

def google_dork(query, exclude_domains, max_results=100, delay=1):
    """Execute Google Dork query with enhanced error handling"""
    results = []
    api_index = 0
    retry_count = 0
    max_retries = 3
    
    # URL encode the query
    encoded_query = quote_plus(query)
    
    for start in range(1, min(max_results, 100) + 1, 10):
        while retry_count < max_retries:
            api_key = API_KEYS[api_index]
            url = f"https://www.googleapis.com/customsearch/v1?q={encoded_query}&key={api_key}&cx={CX}&start={start}"
            
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                response = requests.get(url, timeout=15, headers=headers)
                
                if response.status_code == 200:
                    data = response.json()
                    items = data.get("items", [])
                    
                    if not items:
                        print(f"{Colors.WARNING}No more results found for query.{Colors.ENDC}")
                        return results
                    
                    for item in items:
                        link = item['link']
                        title = item.get('title', 'No title')
                        snippet = item.get('snippet', 'No snippet')
                        
                        # Enhanced filtering
                        if not any(domain.lower() in link.lower() for domain in exclude_domains):
                            result_entry = {
                                'url': link,
                                'title': title,
                                'snippet': snippet,
                                'query': query
                            }
                            results.append(result_entry)
                    
                    retry_count = 0  # Reset retry count on success
                    break
                
                elif response.status_code in [403, 429]:
                    print(f"{Colors.WARNING}API key {api_index + 1} quota exceeded or rate limited. Rotating...{Colors.ENDC}")
                    api_index = (api_index + 1) % len(API_KEYS)
                    if api_index == 0:
                        wait_time = 60 + random.randint(10, 30)
                        print(f"{Colors.WARNING}All API keys exhausted. Waiting {wait_time} seconds...{Colors.ENDC}")
                        time.sleep(wait_time)
                    continue
                
                else:
                    print(f"{Colors.FAIL}Error {response.status_code}: {response.text}{Colors.ENDC}")
                    retry_count += 1
                    if retry_count < max_retries:
                        print(f"{Colors.WARNING}Retrying... ({retry_count}/{max_retries}){Colors.ENDC}")
                        time.sleep(2 ** retry_count)  # Exponential backoff
                    else:
                        break
                        
            except requests.RequestException as e:
                print(f"{Colors.FAIL}Request failed: {e}{Colors.ENDC}")
                retry_count += 1
                if retry_count < max_retries:
                    print(f"{Colors.WARNING}Retrying... ({retry_count}/{max_retries}){Colors.ENDC}")
                    time.sleep(2 ** retry_count)
                else:
                    break
        
        if retry_count >= max_retries:
            print(f"{Colors.FAIL}Max retries reached, skipping to next batch.{Colors.ENDC}")
            retry_count = 0
        
        # Add randomized delay to avoid rate limiting
        delay_time = delay + random.uniform(0.5, 1.5)
        time.sleep(delay_time)
        
        if len(results) >= max_results:
            break
    
    return results

def read_dorks_from_file(file_path):
    """Read Google Dork queries from a file with enhanced validation"""
    try:
        with open(file_path, "r", encoding='utf-8') as f:
            lines = f.readlines()
        
        dorks = []
        for i, line in enumerate(lines, 1):
            line = line.strip()
            if line and not line.startswith('#'):
                if len(line) > 5:  # Basic validation
                    dorks.append(line)
                else:
                    print(f"{Colors.WARNING}Skipping invalid dork on line {i}: {line}{Colors.ENDC}")
        
        print(f"{Colors.OKGREEN}Loaded {len(dorks)} valid dork queries from {file_path}{Colors.ENDC}")
        return dorks
        
    except FileNotFoundError:
        raise FileNotFoundError(f"File '{file_path}' not found")
    except Exception as e:
        print(f"{Colors.FAIL}Error reading file: {e}{Colors.ENDC}")
        return []

def save_results(results, output_file, format_type='txt'):
    """Save results in different formats"""
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if format_type == 'json':
            output_data = {
                'timestamp': timestamp,
                'total_results': len(results),
                'results': results
            }
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        elif format_type == 'csv':
            import csv
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['URL', 'Title', 'Snippet', 'Query'])
                for result in results:
                    if isinstance(result, dict):
                        writer.writerow([
                            result.get('url', ''),
                            result.get('title', ''),
                            result.get('snippet', ''),
                            result.get('query', '')
                        ])
                    else:
                        writer.writerow([result, '', '', ''])
        
        else:  # Default txt format
            with open(output_file, "w", encoding='utf-8') as f:
                f.write(f"# DorkLens Results - Generated on {timestamp}\n")
                f.write(f"# Total results: {len(results)}\n\n")
                
                for result in results:
                    if isinstance(result, dict):
                        f.write(f"URL: {result.get('url', '')}\n")
                        f.write(f"Title: {result.get('title', '')}\n")
                        f.write(f"Query: {result.get('query', '')}\n")
                        f.write(f"Snippet: {result.get('snippet', '')}\n")
                        f.write("-" * 80 + "\n\n")
                    else:
                        f.write(f"{result}\n")
        
        print(f"{Colors.OKGREEN}Successfully saved {len(results)} results to {output_file}{Colors.ENDC}")
        
    except Exception as e:
        print(f"{Colors.FAIL}Error saving results: {e}{Colors.ENDC}")

def generate_sample_dorks():
    """Generate sample Google Dorks file"""
    sample_dorks = [
        # File exposure dorks
        'filetype:sql "password"',
        'filetype:env "DB_PASSWORD"',
        'filetype:log "password" | "username"',
        'filetype:conf "password" | "passwd"',
        'intitle:"index of" "backup"',
        'intitle:"index of" "config"',
        
        # Directory listing dorks
        'intitle:"index of /" "parent directory"',
        'intitle:"Apache2 Ubuntu Default Page"',
        
        # Login page dorks
        'inurl:admin intitle:login',
        'inurl:wp-admin',
        'inurl:phpmyadmin',
        
        # Error message dorks
        'intext:"sql syntax near" | intext:"syntax error has occurred"',
        'intext:"Warning: mysql_connect()"',
        'intext:"Fatal error" "Call to undefined function"'
    ]
    
    with open('sample_dorks.txt', 'w', encoding='utf-8') as f:
        f.write("# Sample Google Dorks for DorkLens\n")
        f.write("# Use responsibly and only on authorized targets\n\n")
        for dork in sample_dorks:
            f.write(f"{dork}\n")
    
    print(f"{Colors.OKGREEN}Generated sample_dorks.txt with common Google Dorks{Colors.ENDC}")

def main():
    print_banner()
    
    # Validate API keys
    if not validate_api_keys():
        response = input(f"{Colors.WARNING}Continue anyway? (y/N): {Colors.ENDC}")
        if response.lower() != 'y':
            sys.exit(1)
    
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="DorkLens - Advanced Google Dork Scanner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python dorklens.py --dorks queries.txt --output results.txt
  python dorklens.py --dorks queries.txt --format json --max-results 100
  python dorklens.py --generate-sample
        """
    )
    
    parser.add_argument(
        "--dorks",
        help="Path to a file containing Google Dork queries (one per line)"
    )
    parser.add_argument(
        "--output",
        default="dork_results.txt",
        help="Output file to save results (default: dork_results.txt)"
    )
    parser.add_argument(
        "--format",
        choices=['txt', 'json', 'csv'],
        default='txt',
        help="Output format: txt, json, or csv (default: txt)"
    )
    parser.add_argument(
        "--max-results",
        type=int,
        default=50,
        help="Maximum results per query (default: 50, max: 100)"
    )
    parser.add_argument(
        "--exclude",
        help="Path to a file containing domains to exclude (one per line)"
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=1.0,
        help="Delay between requests in seconds (default: 1.0)"
    )
    parser.add_argument(
        "--generate-sample",
        action="store_true",
        help="Generate a sample dorks file and exit"
    )
    
    args = parser.parse_args()
    
    # Generate sample dorks if requested
    if args.generate_sample:
        generate_sample_dorks()
        return
    
    # Validate required arguments
    if not args.dorks:
        print(f"{Colors.FAIL}Error: --dorks argument is required{Colors.ENDC}")
        parser.print_help()
        return
    
    # Validate max_results
    if args.max_results > 100:
        print(f"{Colors.WARNING}Warning: Max results limited to 100 due to Google API restrictions{Colors.ENDC}")
        args.max_results = 100

    # Read Google Dork queries from the specified file
    try:
        dork_queries = read_dorks_from_file(args.dorks)
        if not dork_queries:
            print(f"{Colors.FAIL}No valid dorks found in the file.{Colors.ENDC}")
            return
    except FileNotFoundError as e:
        print(f"{Colors.FAIL}{e}{Colors.ENDC}")
        return

    # Read exclude domains from file or use defaults
    if args.exclude:
        exclude_domains = read_domains_from_file(args.exclude)
    else:
        exclude_domains = DEFAULT_EXCLUDE_DOMAINS
        print(f"{Colors.OKBLUE}Using {len(exclude_domains)} default exclude domains{Colors.ENDC}")

    print(f"{Colors.OKBLUE}Configuration:{Colors.ENDC}")
    print(f"  - Queries: {len(dork_queries)}")
    print(f"  - API Keys: {len(API_KEYS)}")
    print(f"  - Max results per query: {args.max_results}")
    print(f"  - Output format: {args.format}")
    print(f"  - Delay between requests: {args.delay}s")
    print()
    
    # Run multiple queries and save results
    all_results = []
    
    try:
        for i, query in enumerate(dork_queries, 1):
            print(f"{Colors.OKBLUE}[{i}/{len(dork_queries)}] Running query: {Colors.BOLD}{query}{Colors.ENDC}")
            
            results = google_dork(query, exclude_domains, 
                                max_results=args.max_results, 
                                delay=args.delay)
            
            all_results.extend(results)
            print(f"{Colors.OKGREEN}Found {len(results)} results for this query{Colors.ENDC}")
            print()

    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}Scan interrupted by user. Saving partial results...{Colors.ENDC}")

    # Remove duplicates while preserving order
    seen_urls = set()
    unique_results = []
    for result in all_results:
        url = result['url'] if isinstance(result, dict) else result
        if url not in seen_urls:
            seen_urls.add(url)
            unique_results.append(result)

    print(f"{Colors.OKGREEN}Total unique results found: {len(unique_results)}{Colors.ENDC}")

    # Save results to file
    save_results(unique_results, args.output, args.format)

if __name__ == "__main__":
    main()