from bs4 import BeautifulSoup
import pandas as pd
from rdflib import OWL, RDF, Graph

def load_graphml_nodes(file_path):
    """Load node values from a GraphML file."""
    with open(file_path, 'r', encoding='utf-8-sig') as file:
        # Using "xml" parser for handling XML files
        soup = BeautifulSoup(file, "xml")  

    nodes = soup.find_all("node")
    node_values = set()
    for node in nodes:
        data_element = node.find("data", key="d4")
        if data_element:
            label_text = data_element.find("y:Label").find("y:Label.Text").text.strip()
            label_soup = BeautifulSoup(label_text, "html.parser")
            node_name = label_soup.get_text().strip().replace("\n", "")
            node_name = node_name.replace("\ufeff", "").replace("\ufeff", "").replace("\u200b", "")    
            node_values.add(node_name)

    return node_values

def load_graphml_edges(file_path):
    """Load edge values from a GraphML file."""
    with open(file_path, 'r', encoding='utf-8-sig') as file:
        soup = BeautifulSoup(file, "xml")  

    edges = soup.find_all("edge")
    edge_values = set()
    for edge in edges:
        data_element = edge.find("data", key="d11")
        if data_element:
            label_text = data_element.find("y:Label").find("y:Label.Text").text.strip()
            label_soup = BeautifulSoup(label_text, "html.parser")
            edge_name = label_soup.get_text().strip().replace("\n", "")
            edge_name = edge_name.replace("\ufeff", "").replace("\ufeff", "").replace("\u200b", "")      
            edge_values.add(edge_name)

    return edge_values

# Retrives the entities from OWL file 
def retrieve_entities_from_owl(file_path):
    g = Graph()
    g.parse(file_path)
    individuals = set(g.subjects(predicate=RDF.type, object=OWL.NamedIndividual))
    return individuals, g

# Get sub elements for an individual/node
def get_sub_elements(individual, graph):
    sub_elements = {}
    for sub, pred, obj in graph.triples((individual, None, None)):
        if str(obj) != "http://www.w3.org/2002/07/owl#NamedIndividual":
            if str(pred) in sub_elements:            
                if isinstance(sub_elements[str(pred)], list):
                    sub_elements[str(pred)].append(str(obj))
                else:                    
                    sub_elements[str(pred)] = [sub_elements[str(pred)]] + [str(obj)]
            else:
                sub_elements[str(pred)] = [str(obj)]
    
    return sub_elements


def get_all_properties(file_path, platform):
    g = Graph()
    g.parse(file_path)
    prefix = f"http://www.example.com/ontologies/{platform.lower()}-mlops#"
    properties = set()
    for prop in g.subjects(RDF.type, OWL.ObjectProperty):
        prop_str = str(prop).replace(prefix, '').replace('_', ' ')  # Remove prefix and underscores
        properties.add(prop_str)
    for prop in g.subjects(RDF.type, OWL.DatatypeProperty):
        prop_str = str(prop).replace(prefix, '').replace('_', ' ')  # Remove prefix and underscores
        properties.add(prop_str)
    
    return properties

def get_all_nodes(file_path, platform):
    g = Graph()
    g.parse(file_path)
    prefix = f"http://www.example.com/ontologies/{platform.lower()}-mlops#"
    nodes = set()
    for node in g.subjects(RDF.type, OWL.NamedIndividual):
        node_str = str(node)
        if node_str.startswith(prefix):
            node_str = node_str[len(prefix):].replace('_', ' ')  # Remove prefix and underscores
        nodes.add(node_str)
    return nodes

def compare_nodes(graphml_nodes, owl_nodes):
    """Compare nodes between GraphML and OWL files."""
    missing_nodes = [node for node in graphml_nodes if node not in owl_nodes]
    if missing_nodes:
        print("Nodes present in GraphML but not in OWL:")
        print(missing_nodes)
    else:
        print("All nodes from GraphML are present in OWL.")

def compare_properties(graphml_properties, owl_properties):
    """Compare properties between GraphML and OWL files."""
    missing_properties = [prop for prop in graphml_properties if prop not in owl_properties]
    if missing_properties:
        print("Properties present in GraphML but not in OWL:")
        print(missing_properties)
    else:
        print("All properties from GraphML are present in OWL.")


# AWS
print("\n")
print("AWS")
aws_graphml_file = "AWS/AWS.graphml"
aws_graphml_nodes = load_graphml_nodes(aws_graphml_file)
aws_graphml_edges = load_graphml_edges(aws_graphml_file)

print("AWS Nodes from GraphML")
print(aws_graphml_nodes)
print("\n")
print("AWS Edges from GraphML")
print(aws_graphml_edges)


print("\n")
aws_owl_file = "AWS/AWS-MLOps.owl"
aws_OWL_Nodes = get_all_nodes(aws_owl_file, "AWS")
print("AWS Nodes from OWL")
print(aws_OWL_Nodes)

aws_OWL_properties = get_all_properties(aws_owl_file, "AWS")
print("\n")
print("AWS Edges from OWL")
print(aws_OWL_properties)

print("\n")
print("Verifying AWS Abstract GraphML elements against AWS Abstract OWL elements")
compare_nodes(aws_graphml_nodes, aws_OWL_Nodes)
compare_properties(aws_graphml_edges, aws_OWL_properties)


# Azure
print("\n")
print("Azure")
azure_graphml_file = "Azure/Azure.graphml"
azure_graphml_nodes = load_graphml_nodes(azure_graphml_file)
azure_graphml_edges = load_graphml_edges(azure_graphml_file)

print("Azure Nodes from GraphML")
print(azure_graphml_nodes)
print("\n")
print("Azure Edges from GraphML")
print(azure_graphml_edges)


print("\n")
azure_owl_file = "Azure/Azure-MLOps.owl"
azure_OWL_Nodes = get_all_nodes(azure_owl_file, "Azure")
print("Azure Nodes from OWL")
print(azure_OWL_Nodes)

azure_OWL_properties = get_all_properties(azure_owl_file, "Azure")
print("\n")
print("Azure Edges from OWL")
print(azure_OWL_properties)

print("\n")
print("Verifying Azure Abstract GraphML elements against Azure Abstract OWL elements")
compare_nodes(azure_graphml_nodes, azure_OWL_Nodes)
compare_properties(azure_graphml_edges, azure_OWL_properties)
        

# Google
print("\n")
print("Google")
google_graphml_file = "Google/Google.graphml"
google_graphml_nodes = load_graphml_nodes(google_graphml_file)
google_graphml_edges = load_graphml_edges(google_graphml_file)

print("Google Nodes from GraphML")
print(google_graphml_nodes)
print("\n")
print("Google Edges from GraphML")
print(google_graphml_edges)


print("\n")
google_owl_file = "Google/Google-MLOps.owl"
google_OWL_Nodes = get_all_nodes(google_owl_file, "Google")
print("Google Nodes from OWL")
print(google_OWL_Nodes)

google_OWL_properties = get_all_properties(google_owl_file, "Google")
print("\n")
print("Google Edges from OWL")
print(google_OWL_properties)

print("\n")
print("Verifying Google Abstract GraphML elements against Google Abstract OWL elements")
compare_nodes(google_graphml_nodes, google_OWL_Nodes)
compare_properties(google_graphml_edges, google_OWL_properties)