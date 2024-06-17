import streamlit as st
import pandas as pd
from flask import Flask, jsonify
from stats_can import StatsCan

# Initialize StatsCan
sc = StatsCan()

# Load data
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

# Initialize the Flask application
app = Flask(__name__)

# Define the endpoint to get the data
@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(df_yearly.to_dict(orient='records'))

# Streamlit app
st.title('Labour Market Characteristics Visualization')

# Display the DataFrame
st.write(df_yearly)

# Run the Flask app
if __name__ == '__main__':
    app.run(port=8888)
