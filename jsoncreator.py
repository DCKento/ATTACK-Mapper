import requests
import json

#This script will take the full enterprise-attack file and then create a JSON file that only includes the techniques and excludes subtechniques
# URL for MITRE ATT&CK Enterprise framework in STIX format
url = "https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json"

# Fetch the data
response = requests.get(url)
attack_data = response.json()

# Extract tactics and top-level techniques
tactics = {}
for obj in attack_data["objects"]:
    if obj["type"] == "x-mitre-tactic":
        tactics[obj["id"]] = {
            "id": obj["id"],
            "name": obj["name"],
            "techniques": []
        }
    elif obj["type"] == "attack-pattern" and not obj.get("x_mitre_is_subtechnique", False):
        for phase in obj.get("kill_chain_phases", []):
            if phase["kill_chain_name"] == "mitre-attack":
                phase_name = phase["phase_name"]
                if phase_name not in tactics:
                    tactics[phase_name] = {
                        "id": phase_name,
                        "name": phase_name,
                        "techniques": []
                    }
                tactics[phase_name]["techniques"].append({
                    "id": obj["id"],
                    "name": obj["name"]
                })
# Convert to the desired JSON structure
enterprise_attack = {
    "enterprise-attack": {
        "tactics": list(tactics.values())
    }
}

# Save to a JSON file
with open("enterprise_attack_top_level_techniques.json", "w") as file:
    json.dump(enterprise_attack, file, indent=4)

print("JSON file created successfully.")
