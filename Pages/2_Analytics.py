import streamlit as st  
import pandas as pd
import pickle
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.set_page_config(page_title="Plotting Demo", layout="wide")
st.title("Analytics")

# Load the CSV file and pickle file
new_df = pd.read_csv('Pages/data_viz1.csv')

with open("feature_text.pkl", "rb") as file:
    feature_text = pickle.load(file)

# Check if essential columns are available
required_columns = ["sector", "price", "price_per_sqft", "built_up_area", "latitude", "longitude", "property_type", "bedRoom"]
if not all(col in new_df.columns for col in required_columns):
    st.error("Missing required columns in the dataset")
    st.stop()

# Grouping the data
group_df = new_df.groupby('sector')[["price","price_per_sqft","built_up_area","latitude","longitude"]].mean()

# Sector Price per Sqft Geomap
st.header("Sector Price per Sqft Geomap")
if 'latitude' in new_df.columns and 'longitude' in new_df.columns:
    fig = px.scatter_mapbox(group_df, lat="latitude", lon="longitude", color="price_per_sqft", size='built_up_area',
                            color_continuous_scale=px.colors.cyclical.IceFire, zoom=10,
                            mapbox_style="carto-positron", width=2000, height=700, text=group_df.index)
    
    # Adding a rectangle shape as background
    fig.update_layout(
        margin={"r":0,"t":40,"l":0,"b":0},
        font=dict(size=12),
        shapes=[
            dict(
                type="rect",
                x0=0, x1=1, y0=0, y1=1,  # Position and size of the rectangle (full background)
                xref="paper", yref="paper",  # Use paper reference to cover the whole area
                fillcolor="rgba(0, 0, 0, 0.1)",  # Background color with transparency
                layer="below",  # Layer below the plot elements
                line=dict(width=0)  # No border for the rectangle
            )
        ]
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Location data is missing for geospatial mapping.")


# Features Wordcloud
st.header("Features Wordcloud")
if feature_text:
    wordcloud = WordCloud(width=800, height=800, 
                          background_color='white', 
                          stopwords=set(['s']),  # Any stopwords you'd like to exclude
                          min_font_size=10).generate(feature_text)

    plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.tight_layout(pad=0)
    st.pyplot(plt)
else:
    st.warning("Feature text for wordcloud is missing.")

# Area Vs Price
st.header("Area Vs Price")
property_type = st.selectbox("Select Property Type", ["flat", "house"])

if property_type not in new_df["property_type"].unique():
    st.warning(f"No data available for {property_type}s.")
else:
    if property_type == "house":
        fig1 = px.scatter(new_df[new_df["property_type"] == "house"], x='built_up_area', y="price", 
                          color="bedRoom", title="Area VS Price", 
                          labels={'built_up_area': 'Built-up Area (sq ft)', 'price': 'Price (in CR)'},
                          color_continuous_scale='Viridis', 
                          hover_data={'bedRoom': True, 'price': True})
    else:
        fig1 = px.scatter(new_df[new_df["property_type"] == "flat"], x='built_up_area', y="price", 
                          color="bedRoom", title="Area VS Price", 
                          labels={'built_up_area': 'Built-up Area (sq ft)', 'price': 'Price (in CR)'},
                          color_continuous_scale='Viridis', 
                          hover_data={'bedRoom': True, 'price': True})
    fig1.update_layout(margin={"r":0,"t":40,"l":0,"b":0}, 
                      title_x=0.5)
    st.plotly_chart(fig1, use_container_width=True)

# BHK Pie Chart
st.header("BHK Distribution Pie Chart")

select_options = new_df["sector"].unique().tolist()
select_options.insert(0, "Overall")

selected_sector = st.selectbox("Select Sector", select_options)

if selected_sector == "Overall":
    fig2 = px.pie(new_df, names='bedRoom', 
                  color='bedRoom', 
                  color_discrete_map={ '1': 'gold', '2': 'lightblue', '3': 'lightgreen', '4': 'orange'},
                  title="BHK Distribution Across All Sectors")
else:
    fig2 = px.pie(new_df[new_df["sector"] == selected_sector], names='bedRoom',
                  color='bedRoom', 
                  color_discrete_map={ '1': 'gold', '2': 'lightblue', '3': 'lightgreen', '4': 'orange'},
                  title=f"BHK Distribution in {selected_sector} Sector")
    
fig2.update_traces(textinfo="percent+label", pull=[0.05, 0.05, 0.05, 0.05]) # Add pull effect for visual appeal
st.plotly_chart(fig2, use_container_width=True)

# Side by Side BHK Price Comparison
st.header("Side by Side BHK Price Comparison")
if "bedRoom" in new_df.columns and "price" in new_df.columns:
    fig3 = px.box(new_df[new_df["bedRoom"] <= 4], x="bedRoom", y="price", title="BHK Price Range",
                  labels={'bedRoom': 'Number of BHK', 'price': 'Price (in CR)'},
                  color='bedRoom', 
                  boxmode='group', 
                  color_discrete_map={ '1': 'gold', '2': 'lightblue', '3': 'lightgreen', '4': 'orange'})
    fig3.update_layout(title="Price Comparison Based on BHK Type", 
                      title_x=0.5,
                      margin={"r":0,"t":40,"l":0,"b":0})
    st.plotly_chart(fig3, use_container_width=True)
else:
    st.warning("Missing price or bedRoom data for BHK comparison.")
    


