import gradio as gr
import json
import numpy as np
import joblib

# Load the model
model_path = 'Support_Vector_Regression.joblib'  # Update the path to your model file
svr_model = joblib.load(model_path)

# Function to make prediction and save input and output to JSON
def predict_and_save(vehicle_range, vehicle_weight, recycled_materials, battery_capacity, energy_efficiency, model_name):
    # Creating input array for the model
    input_features = np.array([vehicle_range, vehicle_weight, recycled_materials, battery_capacity, energy_efficiency]).reshape(1, -1)
    
    # Making prediction
    predicted_emission = svr_model.predict(input_features)[0]

    # Data to be saved
    data_to_save = {
        "vehicle_range": vehicle_range,
        "vehicle_weight": vehicle_weight,
        "recycled_materials": recycled_materials,
        "battery_capacity": battery_capacity,
        "energy_efficiency": energy_efficiency,
        "model_name": model_name,
        "predicted_emission": predicted_emission
    }

    # Save to JSON file
    with open("predictions.json", "a") as file:
        json.dump(data_to_save, file)
        file.write("\n")  # For newline separation between entries

    return predicted_emission

# Creating Gradio interface
iface = gr.Interface(
    fn=predict_and_save,
    inputs=[
        gr.inputs.Number(label="Vehicle Range (km)"),
        gr.inputs.Number(label="Vehicle Weight (kg)"),
        gr.inputs.Number(label="Recycled Materials Used (%)"),
        gr.inputs.Number(label="Battery Capacity (kWh)"),
        gr.inputs.Number(label="Factory Energy Efficiency (%)"),
        gr.inputs.Textbox(label="Model Name")
    ],
    outputs="number",
    title="CO2 Emissions Prediction",
    description="Predict CO2 Emissions in Manufacturing (kg) for Electric Vehicles"
)

# Launch the Gradio interface
iface.launch()
