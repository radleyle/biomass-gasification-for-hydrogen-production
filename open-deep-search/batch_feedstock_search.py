import subprocess
import signal
import time

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

def run_with_timeout(command, timeout=900):  # 15 minutes timeout
    """Run command with timeout to prevent hanging."""
    try:
        print(f"⏰ Running with {timeout//60}min timeout: {' '.join(command)}")
        result = subprocess.run(command, cwd=".", timeout=timeout)
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print(f"⚠️ Query timed out after {timeout//60} minutes - skipping to next query")
        return False
    except Exception as e:
        print(f"❌ Error running query: {e}")
        return False

# Batch 1: Hydrogen yield (explicit units)
base_query_h2 = "experimental hydrogen yield data (mol/kg OR mmol/g) from {} of {} including tables or quantitative results if available"

print("\n=== Running batch search for H2 yield (20 queries, with units) ===\n")
for tech in technologies:
    for feedstock in feedstocks:
        query = base_query_h2.format(tech, feedstock)
        print(f"\n=== Running research for: {tech} of {feedstock} (H2 yield, units) ===\n")
        
        success = run_with_timeout(["python", "main.py", query])
        if not success:
            print(f"⚠️ Skipping failed query: {tech} + {feedstock} (H2)")
            continue
            
        time.sleep(2)  # Small delay between queries

# Batch 2: CO yield (explicit units) 
base_query_co = "experimental carbon monoxide yield data (mol/kg OR mmol/g) from {} of {} including tables or quantitative results if available"

print("\n=== Running batch search for CO yield (20 queries, with units) ===\n")
for tech in technologies:
    for feedstock in feedstocks:
        query = base_query_co.format(tech, feedstock)
        print(f"\n=== Running research for: {tech} of {feedstock} (CO yield, units) ===\n")
        
        success = run_with_timeout(["python", "main.py", query])
        if not success:
            print(f"⚠️ Skipping failed query: {tech} + {feedstock} (CO)")
            continue
            
        time.sleep(2)  # Small delay between queries

print("\n✅ Batch search completed!")

if __name__ == "__main__":
    pass   