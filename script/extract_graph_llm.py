import os
import openai
import networkx as nx
import matplotlib.pyplot as plt

# Set your OpenAI API key
openai.api_key = 'key_api_key_goes_here'

def extract_calls_from_cobol(file_path):
    with open(file_path, 'r') as file:
        cobol_code = file.read()

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Extract all COBOL program calls from the following COBOL code and format them as JSON with source and target fields:\n\n{cobol_code}\n\nOutput:"}
        ],
        max_tokens=150
    )

    return response.choices[0].message['content'].strip().replace("```json\n", "").replace("```", "")

def generate_neo4j_input(calls):
    neo4j_input = []
    for call in calls:
        neo4j_input.append({
            "source": call["source"],
            "target": call["target"],
            "type": "CALLS"
        })
    return neo4j_input

def main():
    src_folder = 'd:\\personal_projects\\cobol-project\\src'
    cobol_files = [f for f in os.listdir(src_folder) if f.endswith('.cbl')]

    all_calls = []
    for cobol_file in cobol_files:
        file_path = os.path.join(src_folder, cobol_file)
        calls = extract_calls_from_cobol(file_path)
        # print(calls)
        all_calls.extend(eval(calls))  # Assuming the response is a JSON string
        #all_calls.extend(calls)  # Assuming the response is a JSON string


    # neo4j_input = generate_neo4j_input(all_calls)
    # print(neo4j_input)

    # Generate graphical representation
    G = nx.DiGraph()
    for call in all_calls:
        G.add_edge(call['source'], call['target'], relationship='CALLS')

    pos = nx.spring_layout(G)
    plt.figure(figsize=(10, 8))
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color='skyblue', font_size=10, font_weight='bold', arrows=True)
    edge_labels = nx.get_edge_attributes(G, 'relationship')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')
    plt.title('COBOL Program Calls Graph')
    plt.show()

if __name__ == "__main__":
    main()