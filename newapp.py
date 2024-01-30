import pandas as pd
import numpy as np
from scipy import stats
import random

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error


num_samples = 500000
# Emissions over time
years = np.arange(2015, 2025)
emissions_factors = stats.expon(0.05).pdf(np.arange(2015, 2025))
base_emissions = stats.norm(10000, 2500).rvs(num_samples)

# Manufacturing features
factory_size = stats.lognorm(5, 2).rvs(num_samples)
production_volume = stats.poisson(10000).rvs(num_samples)
equipment_efficiency = stats.norm(75, 10).rvs(num_samples)
renewable_energy_share = stats.uniform(0, 1).rvs(num_samples)
logistics_distance = stats.expon(100).rvs(num_samples)

# Product features
battery_capacity = stats.norm(75, 20).rvs(num_samples)
battery_chemistry = np.random.choice(['Li-ion', 'NiMH', 'Lead-Acid'], num_samples)
vehicle_weight = stats.norm(2000, 500).rvs(num_samples)
material_composition = np.random.choice(['Aluminum', 'Steel', 'Plastic'], num_samples)

years = np.arange(2015, 2025)
emissions_factors = stats.expon(0.05).rvs(num_samples)
sample_years = np.random.choice(np.arange(2015, 2025), num_samples)
year_factors = emissions_factors[sample_years - 2015]

print("Base Emissions:")
print(base_emissions[:5])

print("\nYear Factors:")
print(year_factors[:5])

emissions = base_emissions * year_factors
print("\nResulting Emissions:")
print(emissions[:5])


# Create DataFrame
df = pd.DataFrame({
    'Production Year': sample_years,
    'Factory Size': factory_size,
    'Production Volume': production_volume,
    'Equipment Efficiency': equipment_efficiency,
    'Renewable Energy Share': renewable_energy_share,
    'Logistics Distance': logistics_distance,
    'Battery Capacity': battery_capacity,
    'Battery Chemistry': battery_chemistry,
    'Vehicle Weight': vehicle_weight,
    'Material Composition': material_composition,
    'Emissions': emissions
})


# Save to CSV file
csv_file_path = 'new-dataset-50k.csv'
df.to_csv(csv_file_path, index=False)




# Read the dataset
df = pd.read_csv('new-dataset-5l.csv')

# Handle categorical variables (if any)
df = pd.get_dummies(df)

# Separate features and target variable
X = df.drop('Emissions', axis=1)
y = df['Emissions']

# Split data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# Initialize Random Forest Regressor
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)

# Train the model
rf_model.fit(X_train, y_train)


# Predict on test set
y_pred = rf_model.predict(X_test)

# Calculate RMSE
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
print("Root Mean Squared Error:", rmse)


# Define a function to predict emissions
def predict_emissions(features):
    # Convert input to DataFrame
    input_df = pd.DataFrame([features])

    # Reorder columns to match the order during training
    input_df = input_df[X.columns]

    # Make prediction
    prediction = rf_model.predict(input_df)[0]

    return prediction
# Test the model with sample input
sample_input = {
    'Production Year': 2021,
    'Factory Size': 67868.006042283,
    'Production Volume': 67,
    'Equipment Efficiency': 69.46,
    'Renewable Energy Share': 0.67,
    'Logistics Distance': 78.78,
    'Battery Capacity': 78.88776441,
    'Battery Chemistry_Li-ion': 78,
    'Battery Chemistry_Lead-Acid': 0,
    'Battery Chemistry_NiMH': 0,
    'Vehicle Weight': 7.301545,
    'Material Composition_Aluminum': 0,
    'Material Composition_Plastic': 1,
    'Material Composition_Steel': 0
}

# Make prediction
predicted_emissions = predict_emissions(sample_input)
print("Predicted Emissions:", predicted_emissions)




# Calculate R^2 score
r2_score = rf_model.score(X_test, y_test)
print("R^2 Score:", r2_score)

# Predict on test set
y_pred = rf_model.predict(X_test)

# Calculate Mean Absolute Error
mae = mean_absolute_error(y_test, y_pred)
print("Mean Absolute Error:", mae)

# Calculate Mean Squared Error
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)

# Calculate Root Mean Squared Error
rmse = np.sqrt(mse)
print("Root Mean Squared Error:", rmse)



