import os
import re

REPORTS_DIR = "gpt-researcher/reports"
OUTPUT_FILE = "reference_links.txt"

def extract_links_from_report(report_path):
    with open(report_path, "r", encoding="utf-8") as f:
        content = f.read()
    # Find the References section
    refs = re.split(r"(?i)## References", content)
    if len(refs) < 2:
        return []
    refs_section = refs[1]
    # Extract all URLs
    urls = re.findall(r"https?://[^\s\)\]]+", refs_section)
    return urls

all_links = set()
for fname in os.listdir(REPORTS_DIR):
    if fname.endswith(".md"):
        links = extract_links_from_report(os.path.join(REPORTS_DIR, fname))
        all_links.update(links)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for url in sorted(all_links):
        f.write(url + "\n")

print(f"Extracted {len(all_links)} unique reference links to {OUTPUT_FILE}")
