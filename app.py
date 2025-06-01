import streamlit as st

'''
# TaxiFareModel front
'''

st.markdown('''
Remember that there are several ways to output content into your web page...

Either as with the title by just creating a string (or an f-string). Or as with this paragraph using the `st.` functions
''')

# Ask user for ride parameters
import datetime
import requests
import pandas as pd
import pydeck as pdk

pickup_date = st.date_input("Pickup date")
pickup_time = st.time_input("Pickup time")
pickup_datetime = datetime.datetime.combine(pickup_date, pickup_time)
pickup_longitude = st.number_input("Pickup longitude", value=-73.985428)
pickup_latitude = st.number_input("Pickup latitude", value=40.748817)
dropoff_longitude = st.number_input("Dropoff longitude", value=-73.985428)
dropoff_latitude = st.number_input("Dropoff latitude", value=40.748817)
passenger_count = st.number_input("Passenger count", min_value=1, max_value=8, value=1, step=1)

url = 'https://taxifare.lewagon.ai/predict'
if url == 'https://taxifare.lewagon.ai/predict':
    st.markdown('Maybe you want to use your own API for the prediction, not the one provided by Le Wagon...')


# 2. Build a dictionary containing the parameters for our API
params = {
    "pickup_datetime": pickup_datetime.strftime("%Y-%m-%d %H:%M:%S"),
    "pickup_longitude": pickup_longitude,
    "pickup_latitude": pickup_latitude,
    "dropoff_longitude": dropoff_longitude,
    "dropoff_latitude": dropoff_latitude,
    "passenger_count": passenger_count
}

# 3. Call our API using the `requests` package
if st.button("Get fare prediction"):
    response = requests.get(url, params=params)
    if response.status_code == 200:
        # 4. Retrieve the prediction from the JSON returned by the API
        prediction = response.json().get("fare", "No fare found")
        fare = round(float(prediction), 2)  # Round to 2 decimal places
        # Display the prediction to the user
        st.success(f"Predicted fare: ${fare}")
    else:
        st.error("Error retrieving prediction from API.")

# 4. display map and overlay trip
# Create a DataFrame with pickup and dropoff points
trip_points = pd.DataFrame({
    'lat': [pickup_latitude, dropoff_latitude],
    'lon': [pickup_longitude, dropoff_longitude]
})

# Define colors: green for pickup, red for dropoff
trip_points['type'] = ['Pickup', 'Dropoff']
trip_points['color'] = trip_points['type'].map({'Pickup': [0, 255, 0], 'Dropoff': [255, 0, 0]})

# Create a pydeck layer for the points
layer = pdk.Layer(
    "ScatterplotLayer",
    data=trip_points,
    get_position='[lon, lat]',
    get_color='color',
    get_radius=100,
    pickable=True
)

# Set the initial view state
view_state = pdk.ViewState(
    latitude=trip_points['lat'].mean(),
    longitude=trip_points['lon'].mean(),
    zoom=12
)

# Render the map
st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip={"text": "{type}"}))

# Display a legend
st.markdown("""
**Legend:**
<span style="color:green">● Pickup</span>
<span style="color:red">● Dropoff</span>
""", unsafe_allow_html=True)

# show coordinates
st.write("Pickup:", (pickup_latitude, pickup_longitude))
st.write("Dropoff:", (dropoff_latitude, dropoff_longitude))
