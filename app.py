import pandas as pd
import re
from stats_can import StatsCan
from flask import Flask, jsonify

# Initialize the Flask application
app = Flask(__name__)

# Initialize StatsCan
sc = StatsCan()

# Load data (Note: This will only load data when the Lambda function is initialized)
df = sc.table_to_df("14-10-0023-01")

# Clean and rename DataFrame
df_clean = df[['REF_DATE', 'Labour force characteristics', 'North American Industry Classification System (NAICS)', 'Sex', 'Age group', 'VALUE']]
df_main = df_clean.rename(columns={
    'REF_DATE': 'Year',
    'Labour force characteristics': 'Characteristics',
    'North American Industry Classification System (NAICS)': 'Industry',
    'VALUE': 'Value'
})
df_main['Year'] = df_main['Year'].astype(str)
df_main['Year'] = df_main['Year'].str[:4]

# Remove content inside square brackets from 'Industry' column
df_main['Industry'] = df_main['Industry'].str.replace(r'\[.*?\]', '', regex=True).str.strip()

df_yearly = df_main.groupby(['Year', 'Characteristics', 'Industry', 'Sex', 'Age group'], as_index=False).mean()

# Define the endpoint for the API
@app.route('/')
def home():
    return "Welcome to the data API. Go to /data to see the data."

# Define the endpoint to get the data
@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(df_yearly.to_dict(orient='records'))

# This block is not needed for manual deployment
# def lambda_handler(event, context):
#     # Create a new Flask app for each request
#     with app.app_context():
#         return app(event, context)

if __name__ == '__main__':
    # This block is not needed for manual deployment
    # app.run(debug=True)
    pass
