import subprocess

# Define feedstocks and technologies
feedstocks = [
    "agricultural residues",
    "sewage sludge",
    "municipal solid waste",
    "algae",
    "woody forest energy crops"
]

technologies = [
    "steam gasification",
    "supercritical water gasification",
    "plasma gasification",
    "CO2 gasification"
]

# Batch 1: Hydrogen yield (explicit units)
base_query_h2 = "experimental hydrogen yield data (mol/kg OR mmol/g) from {} of {} including tables or quantitative results if available"

print("\n=== Running batch search for H2 yield (20 queries, with units) ===\n")
for tech in technologies:
    for feedstock in feedstocks:
        query = base_query_h2.format(tech, feedstock)
        print(f"\n=== Running research for: {tech} of {feedstock} (H2 yield, units) ===\n")
        subprocess.run(["python", "main.py", query], cwd=".")

# Batch 2: CO yield (explicit units)
base_query_co = "experimental carbon monoxide yield data (mol/kg OR mmol/g) from {} of {} including tables or quantitative results if available"

print("\n=== Running batch search for CO yield (20 queries, with units) ===\n")
for tech in technologies:
    for feedstock in feedstocks:
        query = base_query_co.format(tech, feedstock)
        print(f"\n=== Running research for: {tech} of {feedstock} (CO yield, units) ===\n")
        subprocess.run(["python", "main.py", query], cwd=".")

if __name__ == "__main__":
    pass  # The script runs on import, so nothing needed here 