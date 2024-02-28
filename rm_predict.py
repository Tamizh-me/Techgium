import gradio as gr
import joblib
import numpy as np
import csv

model = joblib.load('models/gradient_boosting_regressor_model.joblib')

emission_factors = {
    'Synthetic Rubber': 2.4,
    'Natural Rubber': 0.639,
    'Carbon Black': 3.2,
    'Steel Cord': 2.46,
    'Silica': 2.06,
    'Process Oil': 1.61,
    'Bead Wire': 2.46,
    'Zinc Oxide': 2.01,
    'Sulfur': 0.008
}

fuel_emission_factors = {
    'Benzene': 2.81,
    'Kerosene': 2.76,
    'Diesel fuel': 2.89,
    'A heavy oil': 3.08,
    'B • C heavy oil': 3.34,
    'Liquefied petroleum gas (LPG)': 3.78,
    'Liquefied natural gas (LNG)': 4.23,
    'Fuel coal': 2.37
}

def get_next_identifier():
    file_path = 'predictions.csv'
    try:
        with open(file_path, 'r') as file:
            last_line = None
            for last_line in csv.reader(file): pass
            if last_line and last_line[0].startswith('tire'):
                last_num = int(last_line[0][4:])
                return f"tire{last_num + 1}"
    except FileNotFoundError:
        pass
    return "tire1"

def save_prediction_results(identifier, tire_weight, predicted_emission, transport_emission, fuel_emission, plant_emission):
    file_path = 'predictions.csv'
    # Attempt to write the header only if the file is being created (i.e., doesn't exist)
    try:
        with open(file_path, 'x', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Identifier', 'Tire Weight', 'Predicted Material CO2 Emissions', 'Raw Material Transportation CO2 Emissions', 'Fuel CO2 Emissions', 'Plant Energy Consumption CO2 Emissions'])
    except FileExistsError:
        pass  # File already exists, proceed to append data without writing the header
    
    with open(file_path, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([identifier, tire_weight, predicted_emission, transport_emission, fuel_emission, plant_emission])

def predict_and_calculate_emissions(average_distance, fuel_type, fuel_quantity, energy_consumption, tire_weight, synthetic_rubber_weight, natural_rubber_weight, carbon_black_weight, steel_cord_weight, silica_weight, process_oil_weight, bead_wire_weight, zinc_oxide_weight, sulfur_weight):
    weights = np.array([synthetic_rubber_weight, natural_rubber_weight, carbon_black_weight, steel_cord_weight, silica_weight, process_oil_weight, bead_wire_weight, zinc_oxide_weight, sulfur_weight])
    emissions = weights * np.array([emission_factors[mat] for mat in emission_factors])
    features = np.concatenate(([tire_weight], weights, emissions)).reshape(1, -1)
    predicted_emission = model.predict(features)[0]
    
    # Additional Calculations
    transport_emission = tire_weight * 0.000547 * average_distance
    fuel_emission = fuel_quantity * fuel_emission_factors[fuel_type]
    plant_emission = energy_consumption * 0.82
    
    # Save results
    identifier = get_next_identifier()
    save_prediction_results(identifier, tire_weight, predicted_emission, transport_emission, fuel_emission, plant_emission)
    
    return predicted_emission, transport_emission, fuel_emission, plant_emission

# Assuming the predict_and_calculate_emissions function is defined correctly as per your previous code snippet

with gr.Blocks() as demo:
    gr.Markdown("### Predict Total CO2 Emissions")
    gr.Markdown("Enter the details to predict emissions and calculate additional environmental impacts.")
    
    # Tire and raw material weights
    with gr.Row():
        tire_weight = gr.Number(label="Tyre Weight (kg)")
    with gr.Row():
        synthetic_rubber_weight = gr.Number(label="Synthetic Rubber Weight (kg)", value=0)
        natural_rubber_weight = gr.Number(label="Natural Rubber Weight (kg)", value=0)
        carbon_black_weight = gr.Number(label="Carbon Black Weight (kg)", value=0)
    with gr.Row():
        steel_cord_weight = gr.Number(label="Steel Cord Weight (kg)", value=0)
        silica_weight = gr.Number(label="Silica Weight (kg)", value=0)
        process_oil_weight = gr.Number(label="Process Oil Weight (kg)", value=0)
    with gr.Row():
        bead_wire_weight = gr.Number(label="Bead Wire Weight (kg)", value=0)
        zinc_oxide_weight = gr.Number(label="Zinc Oxide Weight (kg)", value=0)
        sulfur_weight = gr.Number(label="Sulfur Weight (kg)", value=0)

    # Fuel type selection in its own row
    with gr.Row():
        fuel_type = gr.Radio(['Benzene', 'Kerosene', 'Diesel fuel', 'A heavy oil', 'B • C heavy oil', 'Liquefied petroleum gas (LPG)', 'Liquefied natural gas (LNG)', 'Fuel coal'], label="Fuel Type (*for steam and heating)")

    # Additional parameters in a compact 3-box layout
    with gr.Row():
        average_distance = gr.Number(label="Average Distance Provider-Manufacture (km)", value=0)
        fuel_quantity = gr.Number(label="Fuel Quantity per tyre (liters/kg)", value=0)
        energy_consumption = gr.Number(label="Plant Energy Consumption (kWh/tyre)", value=0)
    
    btn_predict = gr.Button("Predict", align="right")  
    
      # Outputs
    predicted_material_emission = gr.Textbox(label="Predicted RawbMaterial CO2 Emissions (kgCO2e/tyre)")
    raw_material_transportation_emission = gr.Textbox(label="Transportation CO2 Emissions (kgCO2e/tyre)")
    fuel_emission = gr.Textbox(label="Heating/Steam Fuel CO2 Emissions (kgCO2e/tyre)")
    plant_energy_consumption_emission = gr.Textbox(label="Plant Energy CO2 Emissions (kgCO2e/tyre)")

    # Button to execute the function
    

    btn_predict.click(
        fn=predict_and_calculate_emissions,
        inputs=[
            average_distance, fuel_type, fuel_quantity, energy_consumption,
            tire_weight, synthetic_rubber_weight, natural_rubber_weight, carbon_black_weight,
            steel_cord_weight, silica_weight, process_oil_weight, bead_wire_weight,
            zinc_oxide_weight, sulfur_weight
        ],
        outputs=[
            predicted_material_emission, raw_material_transportation_emission,
            fuel_emission, plant_energy_consumption_emission
        ]
    )

demo.launch()
