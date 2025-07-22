import re
import sys
import os

def extract_tables_from_markdown(md_text):
    # Regex for markdown tables (rows with | and ---)
    table_regex = r'((?:\|.*\|\n)+\|[ ]*[-:]+.*\n(?:\|.*\|\n)+)'
    tables = []
    for match in re.finditer(table_regex, md_text):
        tables.append(match.group(0).strip())
    return tables

def save_table_as_csv(table_md, out_path):
    lines = [line.strip() for line in table_md.strip().split('\n') if line.strip()]
    # Remove markdown table separator (---) line
    if len(lines) > 2 and set(lines[1].replace('|','').replace('-','').replace(':','').strip()) == set():
        lines.pop(1)
    rows = [ [cell.strip() for cell in line.strip('|').split('|')] for line in lines ]
    with open(out_path, 'w', encoding='utf-8') as f:
        for row in rows:
            f.write(','.join(row) + '\n')

def main():
    # By default, use the latest report file in the current directory
    report_file = sys.argv[1] if len(sys.argv) > 1 else 'gpt_report.md'
    if not os.path.exists(report_file):
        print(f"File {report_file} not found. Please specify the markdown report file.")
        return
    with open(report_file, 'r', encoding='utf-8') as f:
        md_text = f.read()
    tables = extract_tables_from_markdown(md_text)
    if not tables:
        print("No tables found in the report.")
        return
    for i, table in enumerate(tables, 1):
        print(f"\n--- Table {i} ---\n{table}\n")
        csv_name = f"table_{i}.csv"
        save_table_as_csv(table, csv_name)
        print(f"Saved as {csv_name}")

if __name__ == '__main__':
    main()