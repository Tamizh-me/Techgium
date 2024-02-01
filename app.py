import pandas as pd
from joblib import load
import gradio as gr

rf_model = load('random_forest_model.joblib')

default_input = {
    'Factory Size': 67868.006042283,
    'Production Volume': 67,
    'Battery Chemistry_Li-ion': 1,
    'Battery Chemistry_Lead-Acid': 0,
    'Battery Chemistry_NiMH': 0,
    'Material Composition_Aluminum': 0,
    'Material Composition_Plastic': 1,
    'Material Composition_Steel': 0,
    'Logistics Distance': 78.78
}
def predict_emissions(production_year, equipment_efficiency, renewable_energy_share, battery_capacity, vehicle_weight):
    user_input = {
        'Production Year': production_year,
        'Equipment Efficiency': equipment_efficiency,
        'Renewable Energy Share': renewable_energy_share,
        'Battery Capacity': battery_capacity,
        'Vehicle Weight': vehicle_weight
    }
    complete_input = {**default_input, **user_input}
    input_df = pd.DataFrame([complete_input])
    cols = rf_model.feature_names_in_
    input_df = input_df[cols]
    
    prediction = rf_model.predict(input_df)[0]
    return prediction
iface = gr.Interface(
    fn=predict_emissions,
    inputs=[
        gr.inputs.Number(label="Production Year"),
        gr.inputs.Number(label="Equipment Efficiency(%)"),
        gr.inputs.Number(label="Renewable Energy Share(%)"),
        gr.inputs.Number(label="Battery Capacity(KWh)"),
        gr.inputs.Number(label="Vehicle Weight(kg)")
    ],
    outputs=gr.outputs.Textbox(label="Predicted Emission(kgco2)"),
    title="Predict Carbon Emission",
    flagging_options=None,

    description="Enter the values to predict the carbon emissions in kgCO2.")
iface.launch()
