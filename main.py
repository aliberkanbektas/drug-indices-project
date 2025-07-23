from drug_indices.edges import save_edge_relations_to_json
from drug_indices.indices import load_edge_relations_from_json, calculate_and_return_all_drugs, save_results_to_dataframe


drug_list = [
    "afatinib", "alpelisib", "anastrozole", "busulfan", "dasatinib",
    "daunorubicin", "erdafitinib", "melphalan", "mitomycin c",
    "nilotinib", "olaparib", "orgovyx", "plerixafor", "prednisone",
    "zanubrutinib", "belinostat", "bortezomib", "carmustine", "flutamide",
    "futibatinib", "granisetron", "ibrutinib", "lenalidomide",
    "lomustine", "midostaurin", "olutasidenib", "pomalidomide",
    "pralatrexate", "repotrectinib", "ribociclib"
]

json_path = "edge_relations.json"
xlsx_path = "drug_indices.xlsx"

save_edge_relations_to_json(drug_list, json_path)
data = load_edge_relations_from_json(json_path)
results = calculate_and_return_all_drugs(drug_list, data)
df = save_results_to_dataframe(results, xlsx_path)
