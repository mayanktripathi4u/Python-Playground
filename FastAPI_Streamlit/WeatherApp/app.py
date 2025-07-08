import streamlit as st
import requests
import openai

# Function to get weather data from OpenWeatherMap API
def get_weather_data(city, weather_api_key):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + weather_api_key + "&q=" + city
    response = requests.get(complete_url)
    return response.json()

# Function to generate a weather description using OpenAI's GPT model
def generate_weather_description(data, openai_api_key):
    openai.api_key = openai_api_key

    try:
        # Convert temperature from Kelvin to Celsius
        temperature = data['main']['temp'] - 273.15 # Convert Kelvin to Celsius
        description = data['weather'][0]['description']
        prompt = f"The current weather in your city is {description} with a temperature of {temperature:.1f}℃, Explain this in a simple way for a general audience."

        response = openai.Completion.create(
            engine = "gpt-3.5-turbo-instruct",
            prompt = prompt,
            max_tokens = 60
        )

        return response.choices[0].text.strip()
    
    except Exception as e:
        return str(e)

def get_weekly_forecast(weather_api_key, lat, lon):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}forecast?lat={lat}&lon={lon}&appid={weather_api_key}"
    response = requests.get(complete_url)
    return response.json()

def display_weekly_forecast(data):
    try:
        st.write("=========")
        st.write("### Weekly Weather Forecast")
        displayed_dates = set() # To keep track of dates for which forecast has been displayed.

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("", "Day")
        with c2:
            st.metric("", "Desc")
        with c3:
            st.metric("", "Min_temp")
        with c4:
            st.metric("", "Max_temp")
            
        for day in data['list']:
            date = datetime.fromtimestamp(day['at']).strftime('%A, %B %d')
            # Check if the data has already been displayed
            if data not in displayed_dates:
                displayed_dates.add(date)


    except :
        pass

# Main Function to run the Streamlit App
def main():
    # Sidebar config
    st.sidebar.image("weather-icon.jpg", width=120)
    st.sidebar.title("Weather Forecasting with LLM")
    city = st.sidebar.text_input("Enter City Nmae", "Nashville, TN")

    # API Keys
    weather_api_key = "029ce019f2b06296c9ac32e91d4be39e" # Key from OpenWeatherMap API Key
    openai_api_key = "" # 

    # Button to fetch and display 
    submit = st.sidebar.button("Get Weather")

    if submit:
        st.title(f"Weather updtes for {city} is: \n")
        with st.spinner('Fetching weather data ...')
            weather_data = get_weather_data(city, weather_api_key=weather_api_key)
            print(weather_data)
            # Check if the city is found and display weather data
            if weather_data.get("cod") != 404: # Not Found Error
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Temperature ", f"{weather_data['main']['temp'] - 273.15:.2f} c")
                    st.metric("Humidity", f"{weather_data['main']['humidity']}%")
                with col2:
                    st.metric("Pressure ", f"{weather_data['main']['pressure']} hPa")
                    st.metric("Wind Speed", f"{weather_data['wind']['speed']} m/s")

                # Generate and display a friendly weather description
                weather_desc = generate_weather_description(weather_data, openai_api_key=openai_api_key)
                st.write(weather_desc)
            else:
                # Display as error message if the city is not found
                st.error("City not found or an error occured!")



if __name__ == "__main__":
    main()

