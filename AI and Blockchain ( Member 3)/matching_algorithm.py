# --- Mock Data Simulation ---
import math
# 1. A list of available donors with their details
available_donors = [
    {"name": "Rakesh Sharma", "blood_type": "O+", "location": (12.9720, 77.6001)}, # Near MG Road
    {"name": "Priya Singh", "blood_type": "A+", "location": (12.9345, 77.6244)}, # Koramangala
    {"name": "Amit Kumar", "blood_type": "B+", "location": (12.9986, 77.5531)}, # Malleshwaram
    {"name": "Sunita Devi", "blood_type": "A-", "location": (12.9141, 77.6369)}, # HSR Layout
    {"name": "Jeevan P", "blood_type": "O-", "location": (12.9592, 77.6974)}, # Marathahalli
    {"name": "Anil Verma", "blood_type": "AB+", "location": (13.0358, 77.5970)}, # Hebbal
]

# 2. A sample emergency request from a hospital
hospital_request = {
    "hospital_name": "Apollo Hospital",
    "required_blood_type": "A+",
    "location": (12.9716, 77.5946) # Central Bengaluru (approx. coordinates for demonstration)
}


# --- Core Logic ---

def get_compatible_blood_types(recipient_blood_type):
    """Returns a list of donor blood types compatible with the recipient."""
    compatibility_rules = {
        "A+": ["A+", "A-", "O+", "O-"],
        "A-": ["A-", "O-"],
        "B+": ["B+", "B-", "O+", "O-"],
        "B-": ["B-", "O-"],
        "AB+": ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"], # Universal recipient
        "AB-": ["AB-", "A-", "B-", "O-"],
        "O+": ["O+", "O-"],
        "O-": ["O-"], # Universal donor
    }
    return compatibility_rules.get(recipient_blood_type, [])

def calculate_distance(loc1, loc2):
    """Calculates the simple distance between two (lat, lon) points."""
    # This is a simplified distance calculation for demonstration.
    # A real app would use Google Maps API for road distance.
    lat1, lon1 = loc1
    lat2, lon2 = loc2
    return math.sqrt((lat2 - lat1)**2 + (lon2 - lon1)**2) * 111 # Approx conversion to km

def find_best_donors(request, donors):
    """Finds and ranks compatible donors based on distance."""
    
    # Step 1: Find all donors with a compatible blood type
    compatible_types = get_compatible_blood_types(request["required_blood_type"])
    compatible_donors = [d for d in donors if d["blood_type"] in compatible_types]
    
    # Step 2: Calculate the distance for each compatible donor
    for donor in compatible_donors:
        donor["distance_km"] = calculate_distance(request["location"], donor["location"])
        
    # Step 3: Rank the donors by distance (closest first)
    ranked_donors = sorted(compatible_donors, key=lambda d: d["distance_km"])
    
    return ranked_donors

# --- Main Execution ---
if __name__ == "__main__":
    print(f"Searching for donors for a '{hospital_request['required_blood_type']}' request at {hospital_request['hospital_name']}...")
    
    matched_donors = find_best_donors(hospital_request, available_donors)
    
    print("\n--- Top Matched Donors (Ranked by Distance) ---")
    if not matched_donors:
        print("No compatible donors found in the network.")
    else:
        for i, donor in enumerate(matched_donors):
            print(f"{i+1}. Name: {donor['name']}, Blood Type: {donor['blood_type']}, Approx. Distance: {donor['distance_km']:.2f} km")