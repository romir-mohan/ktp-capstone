import json
from itertools import combinations
import os

# Defining the path to data.txt
data_file_path = os.path.join("src/backend/data.txt", "data.txt")

def load_firebase_data(file_path):

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)
    
def identify_similarities(firebase_data):
    similarities = []
    members = list(firebase_data.items())

    for (id1, data1), (id2, data2) in combinations(members, 2):
        common_attrs = []

        # Check major similarity
        if data1.get("major") == data2.get("major"):
            common_attrs.append(f"Same major: {data1.get('major')}")

        # Check year similarity
        if data1.get("year") == data2.get("year"):
            common_attrs.append(f"Same year: {data1.get('year')}")

        # Check role differences (exec)
        if data1.get("role") != "Member" and data2.get("role") != "Member":
            common_attrs.append(f"Role-based connection: {data1.get('role')} ↔ {data2.get('role')}")

        # Check internship similarity, split strings by comma and space
        internships1 = set(data1.get("internships", "").split(", "))
        internships2 = set(data2.get("internships", "").split(", "))
        common_internships = internships1.intersection(internships2)

        if common_internships:
            common_attrs.append(f"Same internships: {', '.join(common_internships)}")

        if common_attrs:
            similarities.append({
                "member1": data1.get("name", "Unknown"),
                "member2": data2.get("name", "Unknown"),
                "connections": common_attrs
            })

    return similarities

firebase_data = load_firebase_data(data_file_path)

similarity_results = identify_similarities(firebase_data)

print(json.dumps(similarity_results, indent=4))
