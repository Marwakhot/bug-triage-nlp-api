import pickle
import pandas as pd
from flask import Flask, request, jsonify

# Initialize the Flask application
app = Flask(__name__)

# LOAD THE TRAINED MODELS AND ENCODERS
MODEL_PATH = 'models/final_multimodel.pkl'

try:
    with open(MODEL_PATH, 'rb') as file:
        data = pickle.load(file)
        component_pipeline = data['component_model']
        priority_pipeline = data['priority_model']
        component_encoder = data['component_encoder']
        priority_encoder = data['priority_encoder']
    print("Models and encoders loaded successfully.")
except FileNotFoundError:
    print(f"Error: Model file not found at {MODEL_PATH}")
    # Exit if the model file is not found
    exit()

# DEFINE THE API ENDPOINTS

# Define a simple root endpoint to check if the API is running
@app.route('/', methods=['GET'])
def home():
    """A simple endpoint to confirm the API is running."""
    return jsonify({
        'status': 'success',
        'message': 'Bug Triage API is running. Use the /predict endpoint for predictions.'
    })

# Define the main prediction endpoint
@app.route('/predict', methods=['POST'])
def predict():
    """
    Accepts a JSON payload with bug report data and returns
    predictions for both component and priority.
    """
    try:
        # Get the JSON data from the request
        json_data = request.get_json(force=True)
        
        # Convert the JSON data into a pandas DataFrame
        # The 'index=[0]' is used because we are predicting for a single instance
        input_df = pd.DataFrame(json_data, index=[0])

        # Make predictions with both models
        component_pred_num = component_pipeline.predict(input_df)
        priority_pred_num = priority_pipeline.predict(input_df)

        # Decode the numerical predictions back to text labels
        component_pred_text = component_encoder.inverse_transform(component_pred_num)
        priority_pred_text = priority_encoder.inverse_transform(priority_pred_num)

        # the JSON response
        response = {
            'status': 'success',
            'predicted_component': component_pred_text[0],
            'predicted_priority': priority_pred_text[0]
        }
        return jsonify(response)

    except Exception as e:
        # Handle potential errors in the request
        return jsonify({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }), 400

# RUN THE FLASK APPLICATION
if __name__ == '__main__':
    app.run(port=8080, debug=True)