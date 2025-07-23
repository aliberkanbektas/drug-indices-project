from drug_indices.edges import get_edge_list_from_pubchem
import networkx as nx
import matplotlib.pyplot as plt

def draw_graph(drug_name: str) -> None:
    """
    It draws a graph for a given drug using its PubChem edge list.

    This function retrieves the molecular structure of the drug in question from PubChem.
    It then constructs an undirected graph based on atom connectivity and visualises it.
    using Matplotlib and NetworkX.

    You can also run the containing script directly via:

        python -m visualization.graph

    Parameters:
        drug_name (str): The name of the drug to visualise.

    Returns:
        None. Displays the graph using a layout-based visualisation.
    """

    edges = get_edge_list_from_pubchem(drug_name)
    if isinstance(edges, list):
        G = nx.Graph()
        G.add_edges_from(edges)
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_size=700, node_color='lightblue', font_size=10, font_color='black')
        plt.title(f"Graph for {drug_name}")
        plt.show()
    else:
        print(f"Error retrieving edges for {drug_name}: {edges}")

# === Usage ===

if __name__ == "__main__":
    drug_name = "afatinib"  # Example drug name
    draw_graph(drug_name)
