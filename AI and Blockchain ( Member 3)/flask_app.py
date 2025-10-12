from flask import Flask, request, jsonify
import joblib
import pandas as pd

# Initialize the Flask application
app = Flask(__name__)

# Load the trained machine learning model
model = joblib.load('model.pkl')
print("✅ Model loaded successfully!")

# Define the '/predict' endpoint
@app.route('/predict', methods=['POST'])
def predict():
    """
    Receives input data in JSON format and returns a prediction.
    """
    # 1. Get the data from the POST request.
    input_data = request.get_json()
    
    # 2. Convert the input data into a pandas DataFrame.
    features = pd.DataFrame([input_data], columns=['day_of_week', 'month', 'day', 'year'])
    
    # 3. Use the loaded model to make a prediction.
    prediction = model.predict(features)
    
    # 4. Prepare the response.
    response = {
        'predicted_units_requested': round(prediction[0], 2) # Rounding for a cleaner number
    }
    
    # 5. Return the response as JSON.
    return jsonify(response)

# Run the app
if __name__ == '__main__':
    # The app will run on http://127.0.0.1:5000/
    app.run(debug=True)