import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from prophet import Prophet
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

# Load your data into a dataframe (assuming 'df' is already loaded or you can load it from a file)
df = pd.read_excel('../00_resources/data/data.xlsx')  # Replace with your data source

# Define a function to run the forecast
def run_forecast(data, element, country):
    data = data[(data['Element'] == element) & (data['Area'] == country)]
    if data.empty:
        st.write(f"No data available for {element} in {country}.")
        return None, None
    data = data.groupby('Year')['Value'].sum().reset_index()
    data.columns = ['ds', 'y']
    data['ds'] = pd.to_datetime(data['ds'], format='%Y')

    model = Prophet()
    model.fit(data)

    future = model.make_future_dataframe(periods=10, freq='Y')
    forecast = model.predict(future)

    return model, forecast

# Streamlit app
st.title('GHG Emissions Forecasting')
st.write('This app forecasts GHG emissions for a selected country.')
st.write('The data used for this app is from the FAOstats GHG emissions dataset.')
st.write('The app is developed by [Dr. Muhammad Aammar Tufail](https://www.linkedin.com/in/dr-muhammad-aammar-tufail-02471213b/).')

# add image
st.image('https://www.tandfonline.com/cms/asset/e2239c5e-698e-4bb7-b23a-fe3a3475c7ef/tssp_a_2361068_uf0001_oc.jpg', caption='GHG Emissions', use_column_width=True)

# Sidebar options
st.sidebar.header('Options')
selected_element = st.sidebar.radio('Select GHG:', ('Emissions (CO2)', 'Emissions (CH4)', 'Emissions (N2O)'))
country = st.sidebar.text_input('Enter country name:', 'Germany')

# side bar options
# add a check box if user wants to see the data
if st.sidebar.checkbox('Show data'):
    st.write('## Data')
    st.write(df)

# Side bar options, show trends check box for selected_element and country using plotly
if st.sidebar.checkbox('Show trends'):
    data = df[(df['Element'] == selected_element) & (df['Area'] == country)]
    if data.empty:
        st.write(f"No data available for {selected_element} in {country}.")
    else:
        data = data.groupby('Year')['Value'].sum().reset_index()
        data.columns = ['Year', 'Value']
        st.write('## Trends')
        st.line_chart(data.set_index('Year'))
        

# Run forecast and display results
if country:
    model, forecast = run_forecast(df, selected_element, country)
    if model is not None and forecast is not None:
        st.write("---")
        st.write(f"## Forecast for {selected_element} in {country}")

        # Plot the forecast
        fig1 = model.plot(forecast)
        plt.title(f'Forecast for {selected_element} - {country}')
        plt.xlabel('Year')
        plt.ylabel('Value (kt)')
        st.pyplot(fig1)

        # Plot the components
        fig2 = model.plot_components(forecast)
        st.pyplot(fig2)
        
    else:
        st.write("No data available for the selected GHG and country.")
else:
    st.write("Please enter a country name.")

# add a checkbox if user wants to see the forecast data
if st.sidebar.checkbox('Show forecast data'):
    st.write('## Forecast Data')
    st.write(forecast)


# st.sidebar.header('Additional Options')
# st.sidebar.write("This section can include more options and configurations for the user.")
