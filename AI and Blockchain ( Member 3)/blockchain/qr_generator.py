import qrcode
import json
import os

def create_blood_unit_qr(unit_id, donor_id, blood_type, block_index):
    """
    Generates a QR code for a new blood unit and saves it to a file.
    """
    # 1. Prepare the data to be stored in the QR code
    qr_data = {
        "unit_id": unit_id,
        "donor_id": donor_id,
        "blood_type": blood_type,
        "initial_block_index": block_index
    }

    # Convert the dictionary to a JSON string
    qr_string = json.dumps(qr_data)

    # 2. Create the QR code image
    img = qrcode.make(qr_string)

    # 3. Save the image to a 'qrcodes' folder
    # Create the folder if it doesn't exist
    if not os.path.exists('qrcodes'):
        os.makedirs('qrcodes')

    filepath = f"qrcodes/{unit_id}.png"
    img.save(filepath)

    print(f"✅ QR Code generated for Unit ID: {unit_id}")
    print(f"   Saved to: {filepath}")
    return filepath

# --- Main execution block for testing ---
if __name__ == "__main__":
    print("--- BloodX QR Code Generator ---")

    # Simulate creating a QR code for a new donation
    # This data would come from our main application
    create_blood_unit_qr(
        unit_id="UNIT_789_XYZ",
        donor_id="DONOR_ANON_12345",
        blood_type="O+",
        block_index=2 # The block where the "Donated" transaction was recorded
    )