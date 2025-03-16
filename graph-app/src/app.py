from flask import Flask, jsonify
import json

app = Flask(__name__)

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
    if (user_info1.get('role') != 'Member') and (user_info2.get('role') != 'Member'):
        score += 3
        categories.append('exec')

    # Compare internship status
    if user_info1.get('internships') == user_info2.get('internships') and user_info1.get('internships') and user_info2.get('internships'):
        score += 4
        categories.append('internship')

    return score, categories

# Function to parse the data and generate nodes and edges
def parse_data():
    data = read_data_from_file()

    nodes = []
    edges = []

    for user_id, user_info in data.items():
        if 'name' in user_info:
            # Add node data
            node = {
                'id': user_info['name'],  # Node ID will be the user's name
                'label': user_info['name'],
                'title': user_info.get('about', 'No description available'),
                'image': user_info.get('pfp_thumb_link', ''),
                'shape': 'image',  # Node uses an image as the shape
                'size': 25
            }
            nodes.append(node)

            # Add edges for each connection
            if 'connections' in user_info:
                for connected_user in user_info['connections']:
                    connected_user_info = data.get(connected_user, {})
                    if connected_user_info:
                        score, categories = calculate_edge_score(user_info, connected_user_info)

                        # Only add edge if score is greater than 0
                        if score > 0:
                            edge = {
                                'from': user_info['name'],
                                'to': connected_user,
                                'score': score,
                                'categories': categories,
                                'label': f"{user_info['name']} - {connected_user} - {score} - " + ', '.join(categories),
                                'arrows': ''  # No arrows for undirected edges
                            }
                            edges.append(edge)

    return {'nodes': nodes, 'edges': edges}

# Function to write data to a JSON file
def write_data_to_file(data, filename="graph_data.json"):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

if __name__ == '__main__':
    app.run(debug=True)
