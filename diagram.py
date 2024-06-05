import matplotlib.pyplot as plt
import networkx as nx

G = nx.DiGraph()

nodes = { "Users": "Users\n---------------\nuser_id (VARCHAR(24) PRIMARY KEY)\nstate (VARCHAR(2))\ncreated_date (DATETIME)\nlast_login (DATETIME)\nrole (VARCHAR(255))\nactive (BOOLEAN)", 
         "Brands": "Brands\n---------------\nbrand_id (VARCHAR(24) PRIMARY KEY)\nbarcode (VARCHAR(255))\nbrand_code (VARCHAR(255))\ncategory (VARCHAR(255))\ncategory_code (VARCHAR(255))\ncpg (VARCHAR(24))\ntop_brand (BOOLEAN)\nname (VARCHAR(255))", 
         "Receipts": "Receipts\n---------------\nreceipt_id (VARCHAR(24) PRIMARY KEY)\nuser_id (VARCHAR(24) FOREIGN KEY)\nbonus_points_earned (INT)\nbonus_points_earned_reason (VARCHAR(255))\ncreate_date (DATETIME)\ndate_scanned (DATETIME)\nfinished_date (DATETIME)\nmodify_date (DATETIME)\npoints_awarded_date (DATETIME)\npoints_earned (FLOAT)\npurchase_date (DATETIME)\npurchased_item_count (INT)\nrewards_receipt_status (VARCHAR(255))\ntotal_spent (FLOAT)", 
         "Receipt_Items": "Receipt_Items\n---------------\nreceipt_item_id (INT AUTO_INCREMENT PRIMARY KEY)\nreceipt_id (VARCHAR(24) FOREIGN KEY)\nbrand_id (VARCHAR(24) FOREIGN KEY)\nitem_description (VARCHAR(255))\nitem_price (FLOAT)\nquantity (INT)" 
         }
node_sizes = {k: len(v.split("\n")) * 100 for k, v in nodes.items()}  # Scale node sizes

for node, label in nodes.items():
    G.add_node(node, label=label, size=node_sizes[node])

G.add_edge("Users", "Receipts", label="user_id")
G.add_edge("Receipts", "Receipt_Items", label="receipt_id")
G.add_edge("Receipt_Items", "Brands", label="brand_id")

pos = nx.spring_layout(G, seed=42)

sizes = [nx.get_node_attributes(G, 'size')[node] for node in G.nodes()]

nx.draw_networkx_nodes(G, pos, node_shape='s', node_size=sizes, node_color='lightblue', edgecolors='black')

nx.draw_networkx_edges(G, pos, arrowstyle='-|>', arrowsize=6, edge_color='grey')

node_labels = nx.get_node_attributes(G, 'label')
for key, val in node_labels.items():
    x, y = pos[key]
    plt.text(x, y, s=val, bbox=dict(facecolor='lightblue', edgecolor='black', boxstyle='round,pad=0.3'), verticalalignment='center', horizontalalignment='center', fontsize=6)

edge_labels = nx.get_edge_attributes(G, 'label')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=6)

plt.margins(0.1)

plt.subplots_adjust(left=0.01, right=0.99, top=0.95, bottom=0.05, wspace=0.4, hspace=0.4)

# Show plot
plt.title("ER Diagram")
plt.show()
