import subprocess

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

base_query = "experimental hydrogen yield data from {} of {} including tables or quantitative results if available"

for tech in technologies:
    for feedstock in feedstocks:
        query = base_query.format(tech, feedstock)
        print(f"\n=== Running research for: {tech} of {feedstock} ===\n")
        subprocess.run(["python", "main.py", query], cwd=".") 