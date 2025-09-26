import streamlit as st
import pandas as pd
import pickle
import plotly.express as px
import csv

# 1. Page Configuration
st.set_page_config(
    page_title="Bug Triage Analytics Dashboard",
    page_icon="🐞",
    layout="wide"
)

# 2. Load Models and Encoders
# Use st.cache_resource to load models only once
@st.cache_resource
def load_models():
    """Loads all models and encoders from the pickle file."""
    with open('models/final_multimodel.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

loaded_data = load_models()
component_pipeline = loaded_data['component_model']
priority_pipeline = loaded_data['priority_model']
component_encoder = loaded_data['component_encoder']
priority_encoder = loaded_data['priority_encoder']

# 3. Helper function for CSV download
@st.cache_data
def convert_df_to_csv(df):
    """Converts a DataFrame to a CSV string for download."""
    return df.to_csv(index=False).encode('utf-8')

# 4. Dashboard Title and Description
st.title("🐞 Bug Triage Analytics Dashboard")
st.write(
    "This tool uses a machine learning model to predict the responsible **team (component)** and the **priority** for a given list of bug reports. "
    "Upload a CSV file to begin."
)

# 5. File Uploader
uploaded_file = st.file_uploader("Upload your CSV file", type="csv")

if uploaded_file is not None:
    try:
        # Auto-detect the separator (delimiter) of the CSV
        first_line = uploaded_file.readline().decode('utf-8')
        dialect = csv.Sniffer().sniff(first_line, delimiters=',;')
        uploaded_file.seek(0)
        
        # Load the user's dataframe
        user_df = pd.read_csv(uploaded_file, sep=dialect.delimiter)
        st.success(f"File uploaded successfully! Detected '{dialect.delimiter}' as the separator.")
        
        st.write("### Input Data Preview:")
        st.dataframe(user_df.head())

        # 6. Column Mapping Interface
        st.write("---")
        st.write("### Map Your Columns")
        st.write("Please tell us which columns in your file correspond to the data our model needs.")
        
        uploaded_columns = user_df.columns.tolist()
        required_cols = {'sd': 'Short Description', 'pd': 'Product', 'os': 'Operating System', 'bs': 'Bug Severity'}
        
        with st.form("mapping_form"):
            column_mapping = {}
            for req_col, display_name in required_cols.items():
                column_mapping[req_col] = st.selectbox(
                    f"Which column contains the '{display_name}'?",
                    options=uploaded_columns,
                    index=uploaded_columns.index(req_col) if req_col in uploaded_columns else 0
                )
            
            submitted = st.form_submit_button("Run Predictions")

        # 7. Prediction and Results Display
        if submitted:
            try:
                # Create a new DataFrame using the user's mapping
                predict_df = pd.DataFrame()
                for req_col, user_col in column_mapping.items():
                    predict_df[req_col] = user_df[user_col]

                with st.spinner('Running predictions... This may take a moment.'):
                    # Make Bulk Predictions
                    component_pred_num = component_pipeline.predict(predict_df)
                    priority_pred_num = priority_pipeline.predict(predict_df)

                    # Get confidence scores for the component prediction
                    comp_probabilities = component_pipeline.predict_proba(predict_df)
                    confidence_scores = comp_probabilities.max(axis=1)
                    
                    # Decode numerical predictions to text labels
                    component_pred_text = component_encoder.inverse_transform(component_pred_num)
                    priority_pred_text = priority_encoder.inverse_transform(priority_pred_num)
                    
                    # Display Results
                    results_df = user_df.copy() # Start with the user's original data
                    results_df['predicted_component'] = component_pred_text
                    results_df['predicted_priority'] = priority_pred_text
                    results_df['confidence'] = confidence_scores

                st.success('Predictions complete!')
                st.write("### Prediction Results")
                st.dataframe(results_df)

                csv_results = convert_df_to_csv(results_df)
                st.download_button(
                    label="Download Results as CSV",
                    data=csv_results,
                    file_name='bug_triage_predictions.csv',
                    mime='text/csv',
                )
                
                # Display Visualizations
                st.write("---")
                st.write("### Results Dashboard")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.write("#### Distribution of Predicted Components")
                    fig_pie = px.pie(results_df, names='predicted_component', title='Bug Reports per Team')
                    st.plotly_chart(fig_pie, use_container_width=True)
                with col2:
                    st.write("#### Distribution of Predicted Priorities")
                    fig_bar = px.bar(results_df['predicted_priority'].value_counts())
                    fig_bar.update_layout(xaxis_title="Priority", yaxis_title="Count", showlegend=False)
                    st.plotly_chart(fig_bar, use_container_width=True)

            except Exception as e:
                st.error(f"An error occurred during prediction: {e}")

    except Exception as e:
        st.error(f"Could not parse the CSV file. Please ensure it's a valid CSV. Error: {e}")