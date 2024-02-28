import gradio as gr
import csv
import matplotlib.pyplot as plt
import io
from PIL import Image
from geopy.distance import geodesic  
import numpy as np

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

chennai_coordinates = (13.0827, 80.2707)

def calculate_distance(city):
    if city.lower() in city_coordinates:
        city_coord = city_coordinates[city.lower()]
        distance = geodesic(chennai_coordinates, city_coord).kilometers
        return distance
    else:
        return None

def get_identifiers_from_csv(file_path):
    identifiers = []
    try:
        with open(file_path, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            identifiers = [row['Identifier'] for row in reader]
    except FileNotFoundError:
        print("The CSV file was not found.")
    return identifiers


def display_emissions_data_and_chart(tire_id, city, end_of_cycle_method):
    distance = calculate_distance(city)
    if distance is not None:
        file_path = 'predictions.csv'
        try:
            with open(file_path, mode='r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['Identifier'] == tire_id:
                        tire_weight = float(row.get('Tire Weight', 0))
                        emissions_per_tire = 0.00056 * tire_weight * distance
                        end_of_life_emission = 0

                        # Calculate end of life emission based on the method
                        if end_of_cycle_method == "Recycling":
                            end_of_life_emission = tire_weight * 0.35
                        elif end_of_cycle_method == "Incineration":
                            end_of_life_emission = tire_weight * 2.127

                        manufacturing_and_energy_emission = float(row.get('Fuel CO2 Emissions', 0)) + float(row.get('Plant Energy Consumption CO2 Emissions', 0))
                        emissions_values = [
                            float(row.get('Predicted Material CO2 Emissions', 0)),
                            float(row.get('Raw Material Transportation CO2 Emissions', 0)),
                            manufacturing_and_energy_emission,  # Combined value
                            emissions_per_tire,
                            end_of_life_emission
                        ]
                        emissions_labels = ['Raw Material Production', 'Raw Material Transportation', 'Manufacturing and Energy Process', 'Distribution', 'End of Life']
                        total_life_cycle_emission = sum(emissions_values)  # Sum of all emissions categories

                        # Adjust pie chart colors to be more subtle and light
                        colors = ['cornflowerblue', 'mediumseagreen', 'lightcoral', 'khaki', 'thistle', 'lightsteelblue']
                            # Calculate both recycling and incineration emissions for message purposes
                        recycle_emission = tire_weight * 0.35
                        incineration_emission = tire_weight * 2.127
                        co2_difference = incineration_emission - recycle_emission
                         # Generate Pie Chart
                        # Generate Pie Chart
                        fig, ax = plt.subplots()
                        wedges, texts, autotexts = ax.pie(emissions_values, startangle=90, colors=colors, autopct='%1.1f%%')
                        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.  # Equal aspect ratio ensures that pie is drawn as a circle.

                        for i, p in enumerate(wedges):
                                ang = (p.theta2 - p.theta1) / 2. + p.theta1
                                y = np.sin(np.deg2rad(ang))
                                x = np.cos(np.deg2rad(ang))
                                horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
                                connectionstyle = "angle,angleA=0,angleB={}".format(ang)
                                percentage = 100. * emissions_values[i] / total_life_cycle_emission
                                # Calculate the offset to prevent overlapping
                                xytext_value = (1.5*np.sign(x), 1.2*y) if percentage > 5 else (1.8*np.sign(x), 1.6*y)
                                
                                 # Check if it is 'Distribution' or 'End of Life' slice and adjust the annotation position
                                if emissions_labels[i] in ['Distribution', 'End of Life']:
                                    if end_of_cycle_method == "Recycling":
                                        # Point 'End of Life' to the left and 'Distribution' to the right
                                        align_direction = -1 if emissions_labels[i] == 'End of Life' else 1
                                        xytext_value = (1.5*align_direction, 1.2*y)
                                
                                ax.annotate(f'{emissions_values[i]:.2f} kgCO2e\n({percentage:.1f}%)', xy=(x, y), xytext=xytext_value,
                                            horizontalalignment=horizontalalignment,
                                            arrowprops=dict(arrowstyle="->", connectionstyle=connectionstyle))

                            
                            # Place the legend outside the pie chart
                        ax.legend(wedges, emissions_labels, title="Emissions Category", loc="center left", bbox_to_anchor=(1.2, 0.5))

    # CO2 savings or additional emissions message based on the end-of-cycle method
                        message = ""
                        if end_of_cycle_method == "Recycling":
                            message = f'By choosing recycling over incineration, you have reduced {co2_difference:.2f} kg of CO2. You made the right choice!'
                        else:
                                additional_emissions = co2_difference
                                message = f'Hmmm, you could have eliminated {additional_emissions:.2f} kg of CO2 by recycling. Consider recycling next time!'

                        plt.figtext(0.5, -0.1, message, wrap=True, horizontalalignment='center', fontsize=12)

                        buf = io.BytesIO()
                        plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.5)
                        buf.seek(0)
                        plt.close(fig)

                        buf_image = Image.open(buf)
                        sustainability_text = "By choosing recycling over incineration, you have reduced {0:.2f} kg of CO2. You made the right choice!".format(co2_difference)
                        additional_info_text = ("1. You can retread the End of Life Tyres(ELT) and help reduce the carbon footprint by 20%.\n2. It is possible to offset this emission by planting 5 Trees.\n3. Choose cleaner and sustainable approach and join the march to attain Net neutral by 2050") # Add your points here

                        return ("Total life cycle emissions: {:.2f} kg CO2".format(total_life_cycle_emission), buf_image,additional_info_text)

        except FileNotFoundError:
            return "The predictions.csv file was not found."
    else:
        return "City not found or distance not available."

# Define a wrapper function for Gradio that calls the display function
def get_emissions_data(tire_id, city):
    info, image = display_emissions_data_and_chart(tire_id, city)
    if image:
        return info, image
    else:
        # If the result isn't an image, return a placeholder or error image
        return info, Image.new('RGB', (200, 200), color='red')

# Gradio interface setup
with gr.Blocks() as demo:
    identifiers = get_identifiers_from_csv('predictions.csv')  # Load identifiers from CSV

    
    

    with gr.Row():
        tire_id_input = gr.Dropdown(label="Select Tyre Identifier", choices= identifiers  , searchable=True)
        city_dropdown = gr.Dropdown(label="Select City", choices=list(city_coordinates.keys()))
        end_of_cycle_dropdown = gr.Radio(label="End of Cycle Method", choices=["Recycling", "Incineration"])
    
    submit_button = gr.Button("Submit").style()  # Make the button full width

    output_info = gr.Textbox(label="Emissions Information")
    output_image = gr.Image(label="Emissions Data Chart")
    output_additional_info = gr.Textbox(label="Tips to reduce the Carbon Footprint")  # For the additional dummy points

    submit_button.click(
        fn=display_emissions_data_and_chart,
        inputs=[tire_id_input, city_dropdown, end_of_cycle_dropdown],
        outputs=[output_info, output_image, output_additional_info]
    )

    #gr.Row(submit_button).style(justify_content='center')  # Center the submit button
demo.launch()