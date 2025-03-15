from flask import Flask, jsonify
import json

app = Flask(__name__)

def read_data_from_file():
    with open('data.txt', 'r') as file:
        data = json.load(file)
    return data

def parse_data(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)

    nodes = []
    edges = []

    for user_id, user_info in data.items():
        if 'name' in user_info:
            node = {
                'id': user_info['name'],
                'label': user_info['name'],
                'title': user_info.get('about', 'No description available'),
                'image': user_info.get('pfp_thumb_link', ''),
                'shape': 'image',
                'size': 25
            }
            nodes.append(node)

            if 'connections' in user_info:
                for connected_user in user_info['connections']:
                    edges.append({
                        'from': user_info['name'],
                        'to': connected_user,
                        'arrows': 'to'
                    })

    return {'nodes': nodes, 'edges': edges}

@app.route('/graph')
def get_graph_data():
    file_path = 'data.txt'
    graph_data = parse_data(file_path)
    return jsonify(graph_data)

if __name__ == '__main__':
    app.run(debug=True)
