import requests
import json

# This script takes the framework and formats it so it's just the Tactics and top level techniques, then sorts them alphabetically
# URL for MITRE ATT&CK Enterprise framework in STIX format
url = "https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json"

# Fetch the data
response = requests.get(url)
attack_data = response.json()

# Define the correct order of tactics based on the MITRE ATT&CK framework
tactic_order = [
    "Reconnaissance",
    "Resource Development",
    "Initial Access",
    "Execution",
    "Persistence",
    "Privilege Escalation",
    "Defense Evasion",
    "Credential Access",
    "Discovery",
    "Lateral Movement",
    "Collection",
    "Command and Control",
    "Exfiltration",
    "Impact"
]

# Create a mapping using the exact names from MITRE ATT&CK
tactic_mapping = {tactic: tactic for tactic in tactic_order}

# Extract tactics and top-level techniques
tactics = {tactic: {"id": None, "name": tactic, "techniques": []} for tactic in tactic_order}

# First pass: extract tactic IDs
for obj in attack_data["objects"]:
    if obj["type"] == "x-mitre-tactic":
        tactic_name = obj["name"]
        if tactic_name in tactic_mapping:
            our_tactic_name = tactic_mapping[tactic_name]
            tactics[our_tactic_name]["id"] = obj["external_references"][0]["external_id"]
            print(f"Mapped tactic: {tactic_name} -> {our_tactic_name} with ID: {tactics[our_tactic_name]['id']}")

# Second pass: extract techniques
technique_count = 0
for obj in attack_data["objects"]:
    if obj["type"] == "attack-pattern":
        technique_id = obj["external_references"][0]["external_id"]
        # Check if it's a top-level technique (not a sub-technique)
        if '.' not in technique_id:
            technique_count += 1
            if "kill_chain_phases" in obj:
                for phase in obj["kill_chain_phases"]:
                    if phase["kill_chain_name"] == "mitre-attack":
                        tactic_name = phase["phase_name"].replace("-", " ").title()
                        if tactic_name in tactics:
                            tactics[tactic_name]["techniques"].append({
                                "id": technique_id,
                                "name": obj["name"]
                            })
                            print(f"Added technique {technique_id}: {obj['name']} to {tactic_name}")
                        else:
                            print(f"Warning: Tactic {tactic_name} not found for technique {technique_id}")
            else:
                print(f"Warning: No kill_chain_phases for technique {technique_id}")

# Alphabetically sort techniques within each tactic
for tactic in tactics.values():
    tactic["techniques"].sort(key=lambda x: x["name"])

# Print debug information for tactics
print("\nTactics:")
for tactic, data in tactics.items():
    print(f"{tactic}: ID={data['id']}, Techniques={len(data['techniques'])}")

# Convert to the desired JSON structure
enterprise_attack = {
    "enterprise-attack": {
        "tactics": [tactics[tactic] for tactic in tactic_order if tactics[tactic]["id"] is not None]
    }
}

# Print debug information
print(f"\nTotal techniques processed: {technique_count}")
for tactic in tactic_order:
    if tactics[tactic]["id"] is not None:
        print(f"{tactic}: {len(tactics[tactic]['techniques'])} techniques")

# Save to a JSON file
output_file_path = "enterprise_attack_top_level_techniques.json"
with open(output_file_path, "w") as file:
    json.dump(enterprise_attack, file, indent=4)

print(f"\nJSON file created successfully at {output_file_path}")

# Print the final structure
print("\nFinal structure:")
print(json.dumps(enterprise_attack, indent=2))
