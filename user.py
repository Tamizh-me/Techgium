import gradio as gr
import csv
import matplotlib.pyplot as plt
import io
from PIL import Image

def display_emissions_data_and_chart(tire_id):
    file_path = 'predictions.csv'
    try:
        with open(file_path, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['Identifier'] == tire_id:
                    # Extracting data for pie chart
                    emissions_labels = [
                        'Predicted Material CO2', 
                        'Raw Material Transportation CO2', 
                        'Fuel CO2', 
                        'Plant Energy Consumption CO2'
                    ]
                    emissions_values = [
                        float(row.get('Predicted Material CO2 Emissions', 0)),
                        float(row.get('Raw Material Transportation CO2 Emissions', 0)),
                        float(row.get('Fuel CO2 Emissions', 0)),
                        float(row.get('Plant Energy Consumption CO2 Emissions', 0))
                    ]

                    # Generate Pie Chart
                    fig, ax = plt.subplots(figsize=(9, 6))  # Adjusted figure size to be 50% larger
                    ax.pie(emissions_values, labels=emissions_labels, autopct='%1.1f%%', startangle=90)
                    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

                    buf = io.BytesIO()
                    plt.savefig(buf, format='png', bbox_inches='tight')
                    buf.seek(0)
                    plt.close(fig)

                    # Convert bytes to PIL Image
                    buf_image = Image.open(buf)
                    return buf_image
                    
    except FileNotFoundError:
        return "The predictions.csv file was not found."

# Define a wrapper function for Gradio that calls the display function
def get_emissions_data(tire_id):
    image = display_emissions_data_and_chart(tire_id)
    if isinstance(image, Image.Image):
        return image
    else:
        # If the result isn't an image, return a placeholder or error image
        return Image.new('RGB', (200, 200), color='red')

# Set up the Gradio Blocks
with gr.Blocks() as demo:
    with gr.Row():
        tire_id_input = gr.Textbox(label="Enter Tire ID")
        submit_button = gr.Button("Submit")
    
    output_image = gr.Image(label="Emissions Data Chart")
    
    submit_button.click(
        fn=get_emissions_data,
        inputs=tire_id_input,
        outputs=output_image
    )

demo.launch()
