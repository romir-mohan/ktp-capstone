import json

# Function to read the data from 'data.txt'
def read_data_from_file():
    with open('data_short.txt', 'r') as file:
        data = json.load(file)
    return data

# Function to parse the data and generate nodes and edges
def parse_data():
    data = read_data_from_file()

    nodes = []

    for user_id, user_info in data.items():
        if 'name' in user_info:
            # Add node data
            node = {
                'name': user_info['name'],
                'profile': user_info.get('pfp_thumb_link', ''),
            }
            nodes.append(node)

    return nodes

# Function to write data to a JSON file
def write_nodes_to_file(data, filename="graph_nodes.json"):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

if __name__ == '__main__':
    graph_data = parse_data()  # Parse the data
    write_nodes_to_file(graph_data)  # Write to file

