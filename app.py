import streamlit as st
import requests
import json
import geocoder
from streamlit_folium import st_folium
import folium
import pandas as pd

g = geocoder.ip('me')
lat = g.latlng[0]
lng = g.latlng[1]


st.title("Satellite Finder")
st.subheader("This webapp shows all the satallites orbiting the Earth above you!!")
st.divider()

with st.form("main form",clear_on_submit=False, border=False):
    col1, col2 = st.columns(2)

    with col1:
        st.write("Your current location")
        st.write("Latitude = " ,lat)
        st.write("Longitude = " ,lng)

    with col2:
        with st.expander("Or choose location manually"):
            #with st.form("my_form", clear_on_submit=False, border=False):

            latitude = st.number_input("Enter Latitude", value=lat, placeholder="Type a number...", key=1, format="%f")
            longitude = st.number_input("Enter Longitude", value=lng, placeholder="Type a number...", key=2, format="%f")

            #setLocation = st.form_submit_button("Set Location")

            #if setLocation:
            lat = latitude
            lng = longitude
            st.success(f"Stored Location: {lat}, {lng}")


    degree = st.slider("Select the degree of the look up?", 0, 90, 45)
   
    categories = {
        'All': 0,
        'Brightest': 1,
        'ISS': 2,
        'Weather': 3,
        'NOAA': 4,
        'GOES': 5,
        'Earth resources': 6,
        'Search & rescue': 7,
        'Disaster monitoring': 8,
        'Tracking and Data Relay Satellite System': 9,
        'Geostationary': 10,
        'Intelsat': 11,
        'Gorizont': 12,
        'Raduga': 13,
        'Molniya': 14,
        'Iridium': 15,
        'Orbcomm': 16,
        'Globalstar': 17,
        'Amateur radio': 18,
        'Experimental': 19,
        'Global Positioning System (GPS) Operational': 20,
        'Glonass Operational': 21,
        'Galileo': 22,
        'Satellite-Based Augmentation System': 23,
        'Navy Navigation Satellite System': 24,
        'Russian LEO Navigation': 25,
        'Space & Earth Science': 26,
        'Geodetic': 27,
        'Engineering': 28,
        'Education': 29,
        'Military': 30,
        'Radar Calibration': 31,
        'CubeSats': 32,
        'XM and Sirius': 33,
        'TV': 34,
        'Beidou Navigation System': 35,
        'Yaogan': 36,
        'Westford Needles': 37,
        'Parus': 38,
        'Strela': 39,
        'Gonets': 40,
        'Tsiklon': 41,
        'Tsikada': 42,
        'O3B Networks': 43,
        'Tselina': 44,
        'Celestis': 45,
        'IRNSS': 46,
        'QZSS': 47,
        'Flock': 48,
        'Lemur': 49,
        'Global Positioning System (GPS) Constellation': 50,
        'Glonass Constellation': 51,
        'Starlink': 52,
        'OneWeb': 53,
        'Chinese Space Station': 54
    }
    # options = st.multiselect(
    # "Choose Satellite Categories", reversed_catg)

    # st.write("You selected:", options)

    categoryName = st.selectbox(
    "Choose Satellite Category", categories
    )

    category = categories.get(categoryName)

    submit = st.form_submit_button("Submit")
    
    if submit:
        ## Getting the elevation from the provided coordinates 
        baseURL = "https://api.open-elevation.com/api/v1/lookup?locations="
        fullURL = baseURL + str(lat) + "," + str(lng)
        #Exaple URL: "https://api.open-elevation.com/api/v1/lookup?locations=29.337010605861433,48.03245186805726"
        response1 = requests.get(fullURL).json()
        elevation = response1['results'][0]['elevation']
        print("elevation =  %s" %elevation)

        ## Getting satellites information
        beginingOfURL = "https://api.n2yo.com/rest/v1/satellite//above/"
        middleOfURL = "/" + str(lat) + "/" + str(lng) + "/" + str(elevation) + "/" + str(degree) + "/" + str(category) + "/"
        endOfURL = "&apiKey=" + str(st.secrets.key)
        finalURL = beginingOfURL + middleOfURL + endOfURL
        print(finalURL) 
        response = requests.get(finalURL)

        def jprint(obj): #takes json object and converts into formatted string to print 
            text = json.dumps(obj, sort_keys=True, indent=4)
            print(text)


        jprint(response1)
        jprint(response.json())
        text = json.dumps(response.json(), sort_keys=True, indent=4)
        print(type(text))
        st.write(finalURL)

        data = json.loads(text)
        satellites = data['above']
        df = pd.DataFrame(satellites)
        df.rename(columns={'satlat':'lat', 'satlng':'lon'}, inplace=True)
        st.write(df)
        st.map(df)

                                    
                            