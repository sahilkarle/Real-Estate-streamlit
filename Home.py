import streamlit as st

# Set the page configuration
st.set_page_config(
    page_title="🏠 Real Estate Price Predictor & Recommendation Tool",
    page_icon="🏠",
    layout="wide"
)

# Title and Welcome Message
st.title("🏠 Welcome to the Real Estate Price Predictor & Recommendation Tool")

# Subtitle
st.markdown("""
Find the perfect property and make smarter real estate decisions with ease!  
Our tool combines **cutting-edge machine learning** and **intuitive design** to simplify the property search and evaluation process.
""")

# Add a banner image
st.image(
    "../Streamlit/1714768726294.jpg", 
    use_container_width=True
)

# Visually separate sections
st.markdown("---")

# What the Tool Offers Section
st.header("🌟 What Does This Tool Offer?")
st.markdown("""
1. **🏠 Price Prediction**: Accurately estimate property prices based on key features like location, size, and amenities.
2. **🔍 Personalized Recommendations**: Discover properties that match your preferences or are similar to a selected property.
3. **📍 Interactive Radius Search**: Explore properties within a specific distance from your chosen location.
4. **📊 Actionable Insights**: Access detailed analytics and trends from historical property data to make informed decisions.
""")

# Visually separate content
st.markdown("---")

# Feature Details in Two Columns
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🔑 Key Features of the Tool:")
    st.markdown("""
    - 🏠 **Price Prediction**: Get an estimated price range for your property.
    - 📍 **Location-Based Search**: Find properties within a defined radius of a selected location.
    - 🏡 **Property Recommendations**: Discover similar properties to your chosen apartment or area.
    - 📏 **Built-Up Area Analysis**: Understand the impact of property size on pricing.
    """)

with col2:
    st.markdown("### 🌟 Why Use This Tool?")
    st.markdown("""
    - 💡 **User-Friendly**: Simple and intuitive interface.
    - 📈 **Accurate Models**: Backed by advanced machine learning algorithms.
    - ⏱️ **Save Time**: Instantly get results without complex setups.
    - 🏘️ **Comprehensive Insights**: Ideal for buyers, sellers, and real estate agents.
    """)

# Analytics Section
st.markdown("---")
st.header("📊 Data-Driven Insights")
st.markdown("""
To help you make better decisions, our tool provides valuable insights from historical property data:
- 📍 **Sector Price per Sqft Geomap**: Visualize property prices by location.
- 💬 **Features Wordcloud**: Discover frequently mentioned property features.
- 🏠 **Area vs Price**: Explore how property size impacts pricing.
- 📊 **BHK Distribution**: Analyze the distribution of BHK types across sectors.
- 📉 **Price Comparison**: Compare prices for different property types side by side.

Visit the **Analytics** section for detailed visualizations and trends.
""")
