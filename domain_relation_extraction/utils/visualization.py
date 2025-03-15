import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
import io
import base64

def create_relation_graph(entities, relations, output_path=None):
    """
    Create a NetworkX graph from extracted entities and relations.
    
    Args:
        entities (list): List of entity dictionaries
        relations (list): List of relation dictionaries
        output_path (str, optional): Path to save the visualization
        
    Returns:
        networkx.Graph: The created graph
    """
    # Create a directed graph
    G = nx.DiGraph()
    
    # Add nodes for entities
    for entity in entities:
        G.add_node(entity['text'], type=entity['type'])
    
    # Add edges for relations
    for relation in relations:
        G.add_edge(relation['source'], relation['target'], 
                   label=relation['type'], relation_type=relation['type'])
    
    # Save the graph if output path is provided
    if output_path:
        plt.figure(figsize=(12, 8))
        
        # Get node positions using force-directed layout
        pos = nx.spring_layout(G, seed=42)
        
        # Draw nodes
        node_colors = {'DISEASE': 'red', 'MEDICATION': 'blue', 'PROCEDURE': 'purple', 
                      'SYMPTOM': 'orange', 'COMPANY': 'green', 'PRODUCT': 'cyan',
                      'METRIC': 'gray', 'EVENT': 'lightgreen'}
        
        # Get node types and colors
        node_color = [node_colors.get(G.nodes[node]['type'], 'black') for node in G.nodes()]
        
        nx.draw_networkx_nodes(G, pos, node_color=node_color, alpha=0.8, node_size=500)
        
        # Draw edges
        edge_colors = {'treats': 'blue', 'causes': 'red', 'prevents': 'green', 
                      'indicates': 'orange', 'acquired': 'purple', 'launched': 'teal',
                      'increased': 'green', 'decreased': 'red'}
        
        edge_color = [edge_colors.get(G.edges[edge]['relation_type'], 'black') for edge in G.edges()]
        
        nx.draw_networkx_edges(G, pos, edge_color=edge_color, width=2, 
                              arrowsize=15, arrowstyle='->')
        
        # Draw labels
        nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')
        
        # Draw edge labels
        edge_labels = {(u, v): G.edges[u, v]['label'] for u, v in G.edges()}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
        
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(output_path, format='png', bbox_inches='tight')
        plt.close()
    
    return G

def create_interactive_graph(entities, relations):
    """
    Create an interactive HTML visualization using pyvis.
    
    Args:
        entities (list): List of entity dictionaries
        relations (list): List of relation dictionaries
        
    Returns:
        str: HTML string of the visualization
    """
    # Create a pyvis network
    net = Network(height="500px", width="100%", directed=True)
    
    # Define node colors by type
    node_colors = {
        'DISEASE': '#dc3545',     # red
        'MEDICATION': '#0d6efd',  # blue
        'PROCEDURE': '#6f42c1',   # purple
        'SYMPTOM': '#fd7e14',     # orange
        'COMPANY': '#20c997',     # teal
        'PRODUCT': '#0dcaf0',     # cyan
        'METRIC': '#6c757d',      # gray
        'EVENT': '#198754'        # green
    }
    
    # Add nodes
    for entity in entities:
        node_color = node_colors.get(entity['type'], '#000000')
        net.add_node(entity['text'], label=entity['text'], title=entity['type'], 
                    color=node_color, shape='box')
    
    # Add edges
    for relation in relations:
        net.add_edge(relation['source'], relation['target'], 
                    title=relation['type'], label=relation['type'])
    
    # Generate HTML
    html = net.generate_html()
    
    return html

def get_graph_image_base64(entities, relations):
    """
    Create a graph image and return as base64 encoded string.
    
    Args:
        entities (list): List of entity dictionaries
        relations (list): List of relation dictionaries
        
    Returns:
        str: Base64 encoded PNG image
    """
    # Create a graph
    G = nx.DiGraph()
    
    # Add nodes for entities
    for entity in entities:
        G.add_node(entity['text'], type=entity['type'])
    
    # Add edges for relations
    for relation in relations:
        G.add_edge(relation['source'], relation['target'], 
                   label=relation['type'], relation_type=relation['type'])
    
    # Create figure
    plt.figure(figsize=(10, 6))
    
    # Get node positions using force-directed layout
    pos = nx.spring_layout(G, seed=42)
    
    # Draw nodes
    node_colors = {'DISEASE': 'red', 'MEDICATION': 'blue', 'PROCEDURE': 'purple', 
                  'SYMPTOM': 'orange', 'COMPANY': 'green', 'PRODUCT': 'cyan',
                  'METRIC': 'gray', 'EVENT': 'lightgreen'}
    
    # Get node types and colors
    node_color = [node_colors.get(G.nodes[node]['type'], 'black') for node in G.nodes()]
    
    nx.draw_networkx_nodes(G, pos, node_color=node_color, alpha=0.8, node_size=500)
    
    # Draw edges
    edge_colors = {'treats': 'blue', 'causes': 'red', 'prevents': 'green', 
                  'indicates': 'orange', 'acquired': 'purple', 'launched': 'teal',
                  'increased': 'green', 'decreased': 'red'}
    
    edge_color = [edge_colors.get(G.edges[edge]['relation_type'], 'black') for edge in G.edges()]
    
    nx.draw_networkx_edges(G, pos, edge_color=edge_color, width=2, 
                          arrowsize=15, arrowstyle='->')
    
    # Draw labels
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')
    
    # Draw edge labels
    edge_labels = {(u, v): G.edges[u, v]['label'] for u, v in G.edges()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
    
    plt.axis('off')
    plt.tight_layout()
    
    # Convert to base64
    img_data = io.BytesIO()
    plt.savefig(img_data, format='png', bbox_inches='tight')
    img_data.seek(0)
    plt.close()
    
    encoded = base64.b64encode(img_data.read()).decode('utf-8')
    return encoded