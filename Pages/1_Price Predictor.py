import streamlit as st
import pickle
import pandas as pd
import numpy as np

# Set page configuration
st.set_page_config(page_title="🏡 Property Price Prediction", 
                   layout="wide")

# Load necessary files
with open("df.pkl", "rb") as file:
    df = pickle.load(file)

with open("pipeline.pkl", "rb") as file:
    pipeline = pickle.load(file)

# Property Price Prediction Page
st.title("🏡 Property Price Prediction Tool")

st.markdown("""
Welcome to the **Property Price Prediction Tool**!  
Fill in the details below to get an **estimated price range** for your property. 
Our tool uses advanced machine learning algorithms to provide accurate predictions. 
""")

# Add a divider for better readability
st.markdown("---")

# Create a form in the center of the page
with st.form("property_form"):
    st.markdown("### 🔢 Enter Property Details")

    # Inputs in a centered layout (columns)
    col1, col2 = st.columns(2)

    with col1:
        property_type = st.selectbox(
            "🏠 Property Type",
            ['flat', 'house'],
            help="Choose the type of property."
        )

        sector = st.selectbox(
            "📍 Sector",
            sorted(df["sector"].unique().tolist()),
            help="Select the sector or location of the property."
        )

        bedroom = float(st.selectbox(
            "🛏️ Number of Bedrooms",
            sorted(df["bedRoom"].unique().tolist()),
            help="Select the number of bedrooms in the property."
        ))

        bathroom = float(st.selectbox(
            "🛁 Number of Bathrooms",
            sorted(df["bathroom"].unique().tolist()),
            help="Select the number of bathrooms in the property."
        ))

        balcony = st.selectbox(
            "🌅 Number of Balconies",
            sorted(df["balcony"].unique().tolist()),
            help="Select the number of balconies."
        )

        property_age = st.selectbox(
            "🏗️ Property Age",
            sorted(df["agePossession"].unique().tolist()),
            help="How old is the property?"
        )

        built_up_area = st.number_input(
            "📐 Built-Up Area (in sq ft)",
            min_value=0.0,
            step=1.0,
            help="Enter the total built-up area of the property."
        )

    with col2:
        servant_room = float(st.selectbox(
            "🛎️ Servant Room",
            [0.0, 1.0],
            help="Does the property have a servant room?"
        ))

        store_room = float(st.selectbox(
            "📦 Store Room",
            [0.0, 1.0],
            help="Does the property have a store room?"
        ))

        furnishing_type = st.selectbox(
            "🛋️ Furnishing Type",
            sorted(df["furnishing_type"].unique().tolist()),
            help="Select the furnishing type of the property."
        )

        luxury_category = st.selectbox(
            "💎 Luxury Category",
            sorted(df["luxury_category"].unique().tolist()),
            help="Select the luxury category of the property."
        )

        floor_category = st.selectbox(
            "🏢 Floor Category",
            sorted(df["floor_category"].unique().tolist()),
            help="Select the floor category (e.g., ground floor, upper floor)."
        )

    # Submit Button
    submit_button = st.form_submit_button("💰 Predict Price")

    if submit_button:
        # Form a DataFrame with user inputs
        data = [[
            property_type, sector, bedroom, bathroom, balcony, property_age,
            built_up_area, servant_room, store_room, furnishing_type,
            luxury_category, floor_category
        ]]

        columns = [
            'property_type', 'sector', 'bedRoom', 'bathroom', 'balcony',
            'agePossession', 'built_up_area', 'servant room', 'store room',
            'furnishing_type', 'luxury_category', 'floor_category'
        ]

        one_df = pd.DataFrame(data, columns=columns)

        # Make a prediction
        base_price = np.expm1(pipeline.predict(one_df))[0]
        low = base_price - 0.22
        high = base_price + 0.22

        # Display prediction results in the center
        st.markdown("---")
        st.success(
            f"🎉 **Estimated Price Range:** ₹{round(low, 2)} Cr - ₹{round(high, 2)} Cr"
        )

# Add a footer
st.markdown("---")
st.markdown("💡 **Note:** Predictions are approximate and should be used as a guide. For detailed insights, consult a real estate expert.")
