# VoidTrace.py
import re
import argparse
import socket
import whois
import json
import requests
import threading
import time
from tqdm import tqdm
from colorama import Fore, init
time.sleep(1)  # Small delay to ensure colorama initializes properly
# Color definitions
WHITE = '\033[1;37m'   # Regular white (not bright)
BLUE = '\033[34m'      # Standard blue
GREEN = '\033[32m'     # Standard green
RESET = '\033[0m'

print(f"{BLUE} _   _       _     _ ___________  ___  _____  _____ ")
print("| | | |     (_)   | |_   _| ___ \/ _ \/  __ \|  ___|" + RESET)
print(" | | | | ___  _  __| | | | | |_/ / /_\ \ /  \/| |__  ")
print(" | | | |/ _ \| |/ _` | | | |    /|  _  | |    |  __| ")
print(f"\ \_/ / (_) | | (_| | | | | |\ \| | | | \__/\| |___ {GREEN}")
print(f" \___/ \___/|_|\__,_| \_/ \_| \_\_| |_/\____/\____/{RESET}")

print(f"{WHITE}VoidTrace - A Recon Tool for Subdomain Enumeration and More BY VECTER61{RESET}")
time.sleep(1)  # Small delay to ensure the banner is displayed properly
init(autoreset=True)
lock = threading.Lock()

def scan_port(host, port, results):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex((host, port))
            if result == 0:
                banner = "No banner"
                try:
                    http_request = f"HEAD / HTTP/1.1\r\nHost: {host}\r\n\r\n"
                    s.send(http_request.encode())
                    banner = s.recv(1024).decode(errors="ignore").strip()
                except:
                    pass
                with lock:
                    results.append({"port": port, "banner": banner})
    except Exception:
        pass

def port_scanner(host, ports, threads):
    results = []
    port_list = parse_ports(ports)
    with tqdm(total=len(port_list), desc="Scanning Ports", ncols=70) as pbar:
        def thread_task(port):
            scan_port(host, port, results)
            pbar.update(1)

        thread_list = []
        for port in port_list:
            t = threading.Thread(target=thread_task, args=(port,))
            t.start()
            thread_list.append(t)

        for t in thread_list:
            t.join()
    return sorted(results, key=lambda x: x["port"])

def parse_ports(ports):
    ports = ports.strip()
    if "-" in ports:
        try:
            start, end = map(int, ports.split("-"))
            return list(range(start, end + 1))
        except ValueError:
            print(f"{Fore.RED}Invalid port range format. Using default 1-1000.")
            return list(range(1, 1001))
    else:
        try:
            return [int(p.strip()) for p in ports.split(",") if p.strip().isdigit()]
        except Exception:
            print(f"{Fore.RED}Invalid ports list format. Using default 1-1000.")
            return list(range(1, 1001))

def resolve_subdomains(domain, wordlist):
    found = []
    print(f"{Fore.CYAN}[+] Enumerating subdomains...")
    try:
        total_lines = sum(1 for _ in open(wordlist))
    except FileNotFoundError:
        print(f"{Fore.RED}Wordlist file '{wordlist}' not found.")
        return found

    with open(wordlist, 'r') as f:
        for line in tqdm(f, total=total_lines, desc="DNS Enum", ncols=70):
            sub = line.strip() + "." + domain
            try:
                ip = socket.gethostbyname(sub)
                found.append({"subdomain": sub, "ip": ip})
            except socket.gaierror:
                continue
    return found

def whois_lookup(domain):
    try:
        return whois.whois(domain)
    except Exception as e:
        return f"WHOIS lookup failed: {e}"

def is_domain(target):
    return any(c.isalpha() for c in target)

def sanitize_filename(name):
    # Remove any character not allowed in filenames (windows/mac/linux safe)
    return re.sub(r'[^A-Za-z0-9_\-\.]', '_', name)

def save_output(target, port_results, subdomains, whois_data, args):
    safe_target = sanitize_filename(target)
    if args.json:
        filename = f"{safe_target}report.json"
        data = {
            "target": target,
            "ports": port_results,
            "subdomains": subdomains,
            "whois": str(whois_data) if whois_data else "Skipped"
        }
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        print(f"{Fore.GREEN}[+] Report saved to {filename}")
    else:
        filename = f"{safe_target}report.txt"
        with open(filename, "w") as f:
            f.write(f"Target: {target}\n\nPorts:\n")
            for p in port_results:
                f.write(f"{p['port']}: {p['banner']}\n")
            if subdomains:
                f.write("\nSubdomains:\n")
                for s in subdomains:
                    f.write(f"{s['subdomain']} -> {s['ip']}\n")
            if whois_data:
                f.write("\nWHOIS:\n")
                f.write(str(whois_data))
        print(f"{Fore.GREEN}[+] Report saved to {filename}")

def run_recon():
    parser = argparse.ArgumentParser(description="Advanced Python Recon Tool")
    parser.add_argument("target", nargs='?', help="Target IP or domain")
    parser.add_argument("-p", "--ports", help="Ports to scan (e.g. 1-65535 or 80,443)", default=None)
    parser.add_argument("-t", "--threads", type=int, help="Number of threads", default=None)
    parser.add_argument("-w", "--wordlist", help="Path to subdomain wordlist", default=None)
    parser.add_argument("--json", action="store_true", help="Save report as JSON")
    parser.add_argument("--no-whois", action="store_true", help="Skip WHOIS lookup")
    parser.add_argument("--no-subdomains", action="store_true", help="Skip subdomain enumeration")

    args = parser.parse_args()

    # Prompt if target not provided via CLI
    if not args.target:
        args.target = input("🔹 Enter target domain or IP: ").strip()

    # Check if target is still empty after prompt
    if not args.target:
        print(f"{Fore.RED}Error: No target domain or IP provided. Exiting.{RESET}")
        exit(1)

    # Proceed with other args input if missing
    if not args.ports:
        port_input = input("🔹 Port range [default: 1-1000]: ").strip()
        args.ports = port_input if port_input else "1-1000"
    if args.threads is None:
        thread_input = input("🔹 Number of threads [default: 100]: ").strip()
        args.threads = int(thread_input) if thread_input.isdigit() else 100
    if not args.wordlist:
        wordlist_input = input("🔹 Subdomain wordlist path [default: subdomains.txt]: ").strip()
        args.wordlist = wordlist_input if wordlist_input else "WORDLISTS/subdomains.txt"

    print(f"{Fore.YELLOW}[+] Starting Recon on {args.target}")

    port_results = port_scanner(args.target, args.ports, args.threads)

    subdomains = []
    if is_domain(args.target) and not args.no_subdomains:
        subdomains = resolve_subdomains(args.target, args.wordlist)

    whois_data = None
    if is_domain(args.target) and not args.no_whois:
        print(f"{Fore.CYAN}[+] Running WHOIS lookup...")
        whois_data = whois_lookup(args.target)

    save_output(args.target, port_results, subdomains, whois_data, args)
    print(f"{Fore.GREEN}[+] Recon complete for {args.target}")
