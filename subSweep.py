import argparse
import os
import time
import subprocess
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


API_KEY = "-2N5V4p3saPZaUUC_Q03bpSOftcwqklU"

# ================== SecurityTrails ===================
def get_subdomains_securitytrails(domain):
    url = f"https://api.securitytrails.com/v1/domain/{domain}/subdomains"
    headers = {
        "Accept": "application/json",
        "APIKEY": API_KEY
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            subdomains = data.get("subdomains", [])
            return [f"{sub}.{domain}" for sub in subdomains]
        else:
            print(f"[!] ST Error {response.status_code} for {domain}")
            return []
    except Exception as e:
        print(f"[!] ST Exception for {domain}: {e}")
        return []

# ================== ShrewdEye ===================
def get_subdomains_shrewdeye(domain):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=options)
    subdomains = set()
    page = 1

    while True:
        url = f"https://shrewdeye.app/domain/{domain}?page={page}"
        try:
            driver.get(url)
            time.sleep(3)

            rows = driver.find_elements(By.CSS_SELECTOR, "a[href^='http']")
            found = 0

            for row in rows:
                text = row.text.strip()
                if text.endswith(domain):
                    subdomains.add(text)
                    found += 1

            if found == 0:
                break

            page += 1
        except Exception as e:
            print(f"[!] SE Error on {domain} page {page}: {e}")
            break

    driver.quit()
    return list(subdomains)

# ================== Subfinder ===================
def get_subdomains_subfinder(domain):
    try:
        result = subprocess.run(
            ["subfinder", "-d", domain, "-silent"],
            capture_output=True,
            text=True,
            timeout=30
        )
        subdomains = result.stdout.strip().split('\n')
        return [sub.strip() for sub in subdomains if sub.strip()]
    except Exception as e:
        print(f"[!] Subfinder error for {domain}: {e}")
        return []

# ================== Main Processing ===================
def process_domains(input_file, output_file):
    if not os.path.exists(input_file):
        print(f"[✘] Input file not found: {input_file}")
        return

    all_subdomains = set()

    with open(input_file, 'r') as f:
        domains = [line.strip() for line in f if line.strip()]

    for domain in domains:
        print(f"\n[===] Processing: {domain}")

        st_subs = get_subdomains_securitytrails(domain)
        print(f"[ST] {len(st_subs)} subdomains")

        se_subs = get_subdomains_shrewdeye(domain)
        print(f"[SE] {len(se_subs)} subdomains")

        sf_subs = get_subdomains_subfinder(domain)
        print(f"[SF] {len(sf_subs)} subdomains")

        all_subdomains.update(st_subs)
        all_subdomains.update(se_subs)
        all_subdomains.update(sf_subs)

    with open(output_file, 'w') as f:
        for sub in sorted(all_subdomains):
            f.write(sub + '\n')

    print(f"\n[✔] Done. Total unique subdomains: {len(all_subdomains)}")
    print(f"[➤] Saved to: {output_file}")

# ================== Argument Parsing ===================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Subdomain Finder (SecurityTrails + Shrewdeye + Subfinder)")
    parser.add_argument("-p", "--path", required=True, help="Path to domains list file")
    parser.add_argument("-o", "--output", required=True, help="Path to output file")
    args = parser.parse_args()

    process_domains(args.path, args.output)

