import pickle
import pandas as pd
from flask import Flask, request, jsonify, render_template

# Create a Flask app
app = Flask(__name__)

# Load the saved models and encoders
with open('models/final_multimodel.pkl', 'rb') as file:
    data = pickle.load(file)
    component_pipeline = data['component_model']
    priority_pipeline = data['priority_model']
    component_encoder = data['component_encoder']
    priority_encoder = data['priority_encoder']

# Define the feature columns the models expect
EXPECTED_COLUMNS = ['pd', 'os', 'bs', 'sd']

# Create a route that handles both viewing the page and submitting the form
@app.route('/', methods=['GET', 'POST'])
def index():
    prediction_component = None
    prediction_priority = None
    
    if request.method == 'POST':
        # This block runs when the user clicks "Predict"
        
        # Get data from the form
        form_data = request.form.to_dict()
        input_df = pd.DataFrame(form_data, index=[0])

        # Ensure all columns are strings
        for col in EXPECTED_COLUMNS:
            input_df[col] = input_df.get(col, "").astype(str)
        
        # Make predictions with both models
        component_pred_num = component_pipeline.predict(input_df)
        priority_pred_num = priority_pipeline.predict(input_df)

        # Decode the predictions back to text
        prediction_component = component_encoder.inverse_transform(component_pred_num)[0]
        prediction_priority = priority_encoder.inverse_transform(priority_pred_num)[0]

    # This renders the webpage
    # It shows the page on first visit (GET) or shows it again with results after predicting (POST)
    return render_template(
        'index.html', 
        prediction_component=prediction_component, 
        prediction_priority=prediction_priority
    )

# Run the app
if __name__ == '__main__':
    app.run(port=8080, debug=True)