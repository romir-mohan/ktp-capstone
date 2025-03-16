import json
from itertools import combinations  # Import combinations for pairwise comparisons

# Function to read the data from 'data.txt'
def read_data_from_file():
    with open('data.txt', 'r') as file:
        data = json.load(file)
    return data

# Function to calculate the score and generate edges
def calculate_edge_score(user_info1, user_info2):
    score = 0
    categories = []

    # Compare year
    if user_info1.get('year') == user_info2.get('year'):
        score += 1
        categories.append('year')

    # Compare major
    if user_info1.get('major') == user_info2.get('major'):
        score += 2
        categories.append('major')

    # Check if both users are exec
    if user_info1.get('role') == 'Pledge' and user_info2.get('role') == 'Pledge':
        score += 3
        categories.append('pledge')

    # Check if both users are exec (not Member and not Pledge)
    if (user_info1.get('role') not in ['Member', 'Pledge']) and (user_info2.get('role') not in ['Member', 'Pledge']):
        score += 3
        categories.append('exec')

    internships1 = set(map(str.strip, user_info1.get('internships', '').split(','))) if user_info1.get('internships') else set()
    internships2 = set(map(str.strip, user_info2.get('internships', '').split(','))) if user_info2.get('internships') else set()

    if internships1 & internships2:  # Check for common internships
        score += 4
        categories.append('internship')

    return score, categories

# Function to generate all possible user connections and compute scores
def generate_edges():
    data = read_data_from_file()
    users = list(data.keys())  # Extract user IDs
    edges = []

    # Iterate over all possible pairs of users
    for user1_id, user2_id in combinations(users, 2):
        user1_info = data[user1_id]
        user2_info = data[user2_id]

        # Ensure both users have names
        if 'name' in user1_info and 'name' in user2_info:
            score, categories = calculate_edge_score(user1_info, user2_info)

            # Only store meaningful edges (score > 0)
            if score > 0:
                edges.append({
                    'member1': user1_info['name'],
                    'member2': user2_info['name'],
                    'score': score,
                    'categories': categories
                })

    return edges

# Function to write edges to a JSON file
def write_edges_to_file(edges, filename="graph_edges.json"):
    with open(filename, 'w') as file:
        json.dump(edges, file, indent=4)

if __name__ == '__main__':
    edges = generate_edges()  # Generate edges
    write_edges_to_file(edges)  # Write edges to file
