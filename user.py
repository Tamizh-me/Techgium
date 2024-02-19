import gradio as gr
import csv
import matplotlib.pyplot as plt
import io
from PIL import Image
from geopy.distance import geodesic  # Library to calculate distances between locations

# Dictionary to map city names to their coordinates
city_coordinates = {
    "banglore": (12.9716, 77.5946),
    "hyderabad": (17.3850, 78.4867),
    "mumbai": (19.0760, 72.8777),
    "cochin": (9.9312, 76.2673),
    "pune": (18.5204, 73.8567),
    "delhi": (28.7041, 77.1025),
    "kolkata": (22.5726, 88.3639),
    "haryana": (29.0588, 76.0856),
    "vizag": (17.6868, 83.2185),
    "guwahati": (26.1445, 91.7362)
}

# Coordinates for Chennai, Tamil Nadu
chennai_coordinates = (13.0827, 80.2707)

def calculate_distance(city):
    if city.lower() in city_coordinates:
        city_coord = city_coordinates[city.lower()]
        distance = geodesic(chennai_coordinates, city_coord).kilometers
        return distance
    else:
        return None

def display_emissions_data_and_chart(tire_id, city):
    distance = calculate_distance(city)
    if distance is not None:
        file_path = 'predictions.csv'
        try:
            with open(file_path, mode='r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['Identifier'] == tire_id:
                        tire_weight = float(row.get('Tire Weight', 0))  # Read tire weight from CSV
                        emissions_per_tire = 0.00056 * tire_weight * distance  # Calculate emissions per tire

                        # Extracting data for pie chart
                        emissions_labels = [
                            'Raw Material Production', 
                            'Raw Material Transportation', 
                            'Manufacturing Process', 
                            'Plant Energy Emission'
                        ]
                        emissions_values = [
                            float(row.get('Predicted Material CO2 Emissions', 0)),
                            float(row.get('Raw Material Transportation CO2 Emissions', 0)),
                            float(row.get('Fuel CO2 Emissions', 0)),
                            float(row.get('Plant Energy Consumption CO2 Emissions', 0))
                        ]

                        # Add emissions per tire to the pie chart
                        emissions_labels.append('Distribution')
                        emissions_values.append(emissions_per_tire)

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
                        return f"Emissions per tire for the total distance: {emissions_per_tire:.2f} kg CO2", buf_image
                        
        except FileNotFoundError:
            return "The predictions.csv file was not found.", None
    else:
        return "City not found or distance not available.", None

# Define a wrapper function for Gradio that calls the display function
def get_emissions_data(tire_id, city):
    info, image = display_emissions_data_and_chart(tire_id, city)
    if image:
        return info, image
    else:
        # If the result isn't an image, return a placeholder or error image
        return info, Image.new('RGB', (200, 200), color='red')

# Set up the Gradio Blocks
with gr.Blocks() as demo:
    with gr.Row():
        tire_id_input = gr.Textbox(label="Enter Tire ID")
        city_dropdown = gr.Dropdown(label="Select City", choices=list(city_coordinates.keys()))
        submit_button = gr.Button("Submit")
    
    output_info = gr.Textbox(label="Emissions Information")
    output_image = gr.Image(label="Emissions Data Chart")
    
    submit_button.click(
        fn=get_emissions_data,
        inputs=[tire_id_input, city_dropdown],
        outputs=[output_info, output_image]
    )

demo.launch()
