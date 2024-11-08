import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px
from streamlit_js_eval import get_geolocation
from streamlit_lottie import st_lottie 

with st.sidebar:
    st_lottie('https://lottie.host/cbe61e44-1322-4801-85a8-df19abfa38ed/zQLlG2qOMD.json')
    st.subheader('How It Works')
    st.markdown('The "Satellites in Sight" web app offers an fun way to track satellites orbiting overhead in real-time! It utilizes the [N2YO REST API](https://www.n2yo.com/api/#above) to gather satellite information based on your specified location and viewing angle. You can also filter by satellite categories, such as Starlink or weather satellites. The data is presented on an interactive map and table, which you can download as a CSV file.')
    st.image('degree.png')
    st.markdown('\"The radius (θ), expressed in degrees, is measured relative to the point in the sky directly above an observer (azimuth). The search radius range is 0 to 90 degrees, nearly 0 meaning to show only satellites passing exactly above the observer location, while 90 degrees to return all satellites above the horizon.\"  — N2YO API Documentation')
    st.markdown('### Resources:')
    st.markdown('[N2YO API Documentation](https://www.n2yo.com/api/#above)')
    st.markdown('[Open Elevation API](https://open-elevation.com/)')
    

st.title("Satellites in Sight: Track What's Above 🛰️")
st.subheader("Discover the Satellites Orbiting Your Location", divider = 'blue')

loc = get_geolocation()

lat = 0
lng = 0


try:
    lat = loc['coords']['latitude']
    lng = loc['coords']['longitude']
    print(f"Latitude: {lat}, Longitude: {lng}")
except (TypeError, KeyError) as e:
    print(f"Error accessing data: {e}")


with st.form("main form",clear_on_submit=False, border=False):
    col1, col2 = st.columns(2)

    with col1:
        st.write("Your current location 🌍")
        st.write("Latitude = " ,lat)
        st.write("Longitude = " ,lng)
        

    with col2:
        with st.expander("Or choose location manually 📍"):

            cities = pd.read_csv('worldcities.csv')
            city = st.selectbox("Choose Your City", cities, index = None, placeholder='Choose Your City..')
    
            if city:
                # Filter the DataFrame for the selected city
                city_data = cities[cities['city'] == city].iloc[0]
                lat = city_data['lat']
                lng = city_data['lng']
    
                # Display the results
                st.write(f"Selected City: {city}")
                st.write(f"Latitude: {lat}, Longitude: {lng}")

        
    st.success(f"Stored Location: {lat}, {lng}")

    degree = st.slider("Select the radius of the search? ", 0, 90, 45, help='0 shows the satellites orbiting right above you, 90 shows all satellite above the horizen.')

    

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
        endOfURL = "&apiKey="+ st.secrets["key"]   
        finalURL = beginingOfURL + middleOfURL + endOfURL
        response = requests.get(finalURL)

        text = json.dumps(response.json(), sort_keys=True, indent=4)

        data = json.loads(text)
        if data == None:
            st.warning('No satellites were detected, try increasing the search degree or choose a different category')
            st.stop()
        
        satellites = data['above']
        df = pd.DataFrame(satellites)
        df.rename(columns={'satlat':'lat', 'satlng':'lon'}, inplace=True)

        tab1, tab2 = st.tabs(['Map', 'Table'])

        with tab1:
            def classify_decade(launchDate):
                year = int(launchDate.split('-')[0])
                if 1950 <= year < 1960:
                    return '1950s'
                elif 1960 <= year < 1970:
                    return '1960s'
                elif 1970 <= year < 1980:
                    return '1970s'
                elif 1980 <= year < 1990:
                    return '1980s'
                elif 1990 <= year < 2000:
                    return '1990s'
                elif 2000 <= year < 2010:
                    return '2000s'
                elif 2010 <= year < 2020:
                    return '2010s'
                else:
                    return '2020s'
                
            df['Launch Decade'] = df['launchDate'].apply(classify_decade)
            map = px.scatter_mapbox(df, lat = 'lat', lon = 'lon', color = 'Launch Decade', hover_name = 'satname', hover_data = ['intDesignator', 'launchDate', 'satalt', 'satid'], color_discrete_sequence=px.colors.qualitative.Set1, zoom = 3, mapbox_style = 'open-street-map', height = 600)
            st.plotly_chart(map)

        with tab2:
            st.write(df)
                                    
                            