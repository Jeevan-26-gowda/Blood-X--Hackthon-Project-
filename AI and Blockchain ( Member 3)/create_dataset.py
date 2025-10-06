import pandas as pd
import random
from datetime import datetime, timedelta

# --- Configuration ---
NUM_ROWS = 200
OUTPUT_FILE = "datasets/blood_demand_mock_data.csv"

# --- Data Options for Random Generation ---
CITIES = ["Bengaluru", "Mysuru", "Mangaluru", "Hubballi", "Belagavi"]
BLOOD_TYPES = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
EMERGENCY_LEVELS = ["High", "Medium", "Low"]
HOSPITALS = {
    "Bengaluru": ["Apollo", "Fortis", "Manipal Hospital"],
    "Mysuru": ["JSS Hospital", "Columbia Asia"],
    "Mangaluru": ["KMC Hospital", "AJ Hospital"],
    "Hubballi": ["SDM Hospital", "KIMS Hubli"],
    "Belagavi": ["KLES Dr. Prabhakar Kore Hospital", "Lakeview Hospital"]
}

# --- Main Script ---
def create_mock_data(num_rows):
    """Generates a list of mock data records."""
    data = []
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365) # Data for the last year

    print(f"Generating {num_rows} rows of mock data...")

    for _ in range(num_rows):
        # Generate a random date
        random_date = start_date + timedelta(seconds=random.randint(0, int((end_date - start_date).total_seconds())))
        
        # Choose a random city and then a hospital from that city
        city = random.choice(CITIES)
        hospital = random.choice(HOSPITALS[city])
        
        # Create one row of data as a dictionary
        record = {
            "Date": random_date.strftime("%Y-%m-%d"),
            "City": city,
            "BloodType": random.choice(BLOOD_TYPES),
            "UnitsRequested": random.randint(1, 15),
            "EmergencyLevel": random.choice(EMERGENCY_LEVELS),
            "Hospital": hospital
        }
        data.append(record)
        
    print("✅ Data generation complete.")
    return data

# --- Execution ---
if __name__ == "__main__":
    # 1. Generate the data
    mock_data_list = create_mock_data(NUM_ROWS)
    
    # 2. Convert the list of dictionaries to a pandas DataFrame
    df = pd.DataFrame(mock_data_list)
    
    # 3. Save the DataFrame to a CSV file
    try:
        df.to_csv(OUTPUT_FILE, index=False)
        print(f"✅ Mock data successfully saved to '{OUTPUT_FILE}'")
    except FileNotFoundError:
        print(f"❌ Error: The directory 'datasets/' does not exist. Please create it first.")