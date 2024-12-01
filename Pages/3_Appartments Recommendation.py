import streamlit as st
import pickle
import pandas as pd
import numpy as np

# Set the page config
st.set_page_config(page_title="Recommend Apartments", page_icon="🏡", layout="wide")

# Load the necessary files

with open("location_distance.pkl", "rb") as file:
    location_df = pickle.load(file)
    
with open("cosine_sim1.pkl", "rb") as file:
    cosine_sim1 = pickle.load(file)
    
with open("cosine_sim2.pkl", "rb") as file:
    cosine_sim2 = pickle.load(file)
    
with open("cosine_sim3.pkl", "rb") as file:
    cosine_sim3 = pickle.load(file)

# Function to recommend properties
def recommend_properties_with_scores(property_name, top_n=5):
    cosine_sim_matrix = 0.5 * cosine_sim1 + 0.8 * cosine_sim2 + 1 * cosine_sim3

    # Get the similarity scores for the property using its name as the index
    sim_scores = list(enumerate(cosine_sim_matrix[location_df.index.get_loc(property_name)]))

    # Sort properties based on the similarity scores
    sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the indices and scores of the top_n most similar properties
    top_indices = [i[0] for i in sorted_scores[1:top_n + 1]]
    top_scores = [i[1] for i in sorted_scores[1:top_n + 1]]

    # Retrieve the names of the top properties using the indices
    top_properties = location_df.index[top_indices].tolist()

    # Create a dataframe with the results
    recommendations_df = pd.DataFrame({
        'Property Name': top_properties,
        'Similarity Score': top_scores
    })

    return recommendations_df

# Initialize session state to store search results if 'search_results' not in session state
if 'search_results' not in st.session_state:
    st.session_state.search_results = []

# Set custom CSS for dark theme and new button color
st.markdown("""
    <style>
        body {
            background-color: #121212;
            color: white;
        }
        .stButton button {
            background-color: #4CAF50; /* Soothing green */
            color: white;
            border-radius: 10px;
            font-weight: bold;
            padding: 10px;
        }
        .stButton button:hover {
            background-color: #45a049; /* Slightly darker green on hover */
        }
        .stSelectbox select, .stTextInput input {
            background-color: #2E2E2E;
            color: white;
            border-radius: 8px;
            padding: 10px;
        }
        .stTextInput label {
            color: #9e9e9e;
        }
        .stDataFrame table {
            border: 1px solid #4CAF50;
        }
        .stDataFrame td, .stDataFrame th {
            padding: 12px;
            text-align: center;
        }
        .stDataFrame th {
            background-color: #333;
        }
        .stSelectbox label {
            color: #9e9e9e;
        }
    </style>
""", unsafe_allow_html=True)

# Title section for user
st.title('Find and Recommend Apartments')

# Step 1: Location Selection and Radius Input
st.header("Step 1: Select a Location and Radius")

selected_location = st.selectbox(
    'Choose a Location',
    sorted(location_df.columns.to_list()),
    help="Select the location of your choice from the dropdown."
)

radius = st.number_input(
    'Enter Radius (in Kilometers)',
    min_value=0.1, step=0.1,
    help="Define the search radius for nearby properties in kilometers."
)

# Search button
if st.button('Search Properties'):
    if radius <= 0:
        st.error("Please enter a valid radius greater than 0 km.")
    else:
        # Filter the properties based on the radius
        result_ser = location_df[location_df[selected_location] < radius * 1000][selected_location].sort_values()

        # Display results
        if result_ser.empty:
            st.warning("No properties found within the selected radius.")
        else:
            st.write("Properties found within the selected radius:")
            for key, value in result_ser.items():
                st.text(f"{key} - {round(value / 1000, 2)} kms")

        # Update search results in session state
        st.session_state.search_results = result_ser.index.tolist()

# Step 2: Apartment Recommendation
st.header("Step 2: Get Apartment Recommendations")

if st.session_state.search_results:
    selected_apartment = st.selectbox(
        'Select an Apartment to Find Similar Properties',
        sorted(st.session_state.search_results),
        help="Choose an apartment from the list to find similar properties."
    )

    if st.button('Recommend Similar Properties'):
        recommendation_df = recommend_properties_with_scores(selected_apartment)
        st.write("Top Similar Properties:")
        st.dataframe(recommendation_df)

else:
    st.warning("Please search for properties first to get recommendations!")
