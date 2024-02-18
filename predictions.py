import gradio as gr
import csv

# Function to retrieve prediction data by identifier
def retrieve_prediction(identifier):
    file_path = 'predictions.csv'
    try:
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['Identifier'] == identifier:
                    # Return only the predicted total CO2 emissions for the given identifier
                    predicted_emissions = row.get('Predicted CO2 Emissions', 'Data not found.')
                    return predicted_emissions
    except FileNotFoundError:
        return "Prediction file not found."
    
    return "Identifier not found."

# Gradio interface to retrieve and display prediction data
iface_retrieve = gr.Interface(
    fn=retrieve_prediction,
    inputs=gr.inputs.Textbox(label="Enter Prediction Identifier"),
    outputs=gr.outputs.Textbox(label="Predicted Total CO2 Emissions (kgCO2e)"),
    title="Retrieve Predicted CO2 Emissions",
    description="Enter the prediction identifier to retrieve the stored total predicted CO2 emissions."
)

iface_retrieve.launch()
