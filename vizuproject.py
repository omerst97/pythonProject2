import numpy as np
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
# from kaggle.api.kaggle_api_extended import KaggleApi
# # import os
# #
# # os.environ['KAGGLE_USERNAME'] = 'shemtoo@post.bgu.ac.il'
# # os.environ['KAGGLE_KEY'] = 'Oo25041997'
# api = KaggleApi()
# api.authenticate()

# df = pd.read_csv('kaggle datasets download -d ulrikthygepedersen/co2-emissions-by-country')

df = pd.read_csv('co2_emissions_kt_by_country(1).csv')
asia = df[df['country_name'].str.contains('Asia')]['country_name'].unique()
europe = df[df['country_name'].str.contains('Euro')]['country_name'].unique()
caribbean = df[df['country_name'].str.contains('Caribbean')]['country_name'].unique()
africa = df[df['country_name'].str.contains('Africa')]['country_name'].unique() # remove South Africa
africa = africa[africa != 'South Africa']

demographic = df[df['country_name'].str.contains('demo')]['country_name'].unique()
ida = df[df['country_name'].str.contains('IDA')]['country_name'].unique()
ibrd = df[df['country_name'].str.contains('IBRD')]['country_name'].unique()

income = df[df['country_name'].str.contains('income')]['country_name'].unique()
other_regions = ['World', 'Europe', 'North America', 'South Asia', 'OECD members', 'Euro area', 'Arab World', 'Heavily indebted poor countries (HIPC)',
          'Small states','Other small states' , 'Fragile and conflict affected situations', 'Least developed countries: UN classification',
          'Pacific island small states']

country_groups = np.concatenate((asia, europe, caribbean, africa, demographic, ida, ibrd,income, other_regions))
df_country = df.query("country_name not in @country_groups").copy() # Data with onl
df_income = df.query("country_name  in @income").copy()
# Create a Streamlit app
st.title(':blue[Visualization of information - Final Project]')
st.subheader(':blue[CO2 Emission over the world]')

# Assuming you have a DataFrame named 'df' with columns: 'country_name', 'year', 'value'

# Define the list of climate change events
events = [
    {"name": "World Oil Crisis", "year": 1979},
    {"name": "Dissolution Of Soviet Union", "year": 1990},
    {"name": "Global Financial Crisis", "year": 2007},
    {"name": "China Joins World Trade Organization", "year": 2001}
]


#
# # Create a dropdown menu in the sidebar for country selection
# selected_countries = st.sidebar.multiselect('Select Countries/continents', df_country['country_name'].unique(),
#                                             default=['United States', 'China', 'Russian Federation'])
selected_countries=[]

# Button to select all countries
selected_option = st.sidebar.radio('Select option', [ 'countries','countries groups', 'income type'])

# Check the selected option and display corresponding selection inputs
if selected_option == 'countries':
    selected_countries = st.sidebar.multiselect('Select countries', df_country['country_name'].unique(),
                                                default=['United States', 'China', 'Russian Federation','Japan','United Kingdom','Ukraine','Canada','Israel','Indonesia'])

elif selected_option == 'countries groups':
    selected_countries = st.sidebar.multiselect('Select countries groups', ['World', 'Central Europe and the Baltics', 'North America', 'South Asia', 'OECD members', 'Arab World'],
                                                default=['Central Europe and the Baltics', 'North America', 'South Asia', 'OECD members', 'Arab World'])
elif selected_option == 'income type':
    selected_countries = st.sidebar.multiselect('Select income types', ['Middle income','Low income','High income'],
                                                default=['Middle income','Low income','High income'])
# Button to select all countries
# select_all_countries = st.sidebar.button('Select All Countries')
# if select_all_countries:
#     selected_countries = sorted(['United States', 'China', 'Russian Federation','Japan','United Kingdom'])
# ['United States', 'China', 'Russian Federation','Japan','United Kingdom','Ukraine','Canada','Israel']

# Create a multiselect dropdown menu in the sidebar for event selection
selected_events = st.sidebar.multiselect('Select Events', [event['name'] for event in events]
                                         , default=['China Joins World Trade Organization','Dissolution Of Soviet Union'])

# Filter the DataFrame based on the selected countries
filtered_df_country = df[df['country_name'].isin(selected_countries)]

# Get the maximum value from the filtered DataFrame
max_value_country = filtered_df_country['value'].max()

# Filter the DataFrame based on the selected countries
filtered_df_country_map = df_country[df_country['country_name'].isin(df_country)]

# Get the maximum value from the filtered DataFrame
max_value_country_map = filtered_df_country_map['value'].max()

# Create the second graph
fig2 = px.choropleth(df_country, locations="country_code",
                     animation_frame="year",
                     animation_group="country_name",
                     color="value",
                     hover_name="country_name",
                     hover_data=['year', 'country_name', 'value'],
                     color_continuous_scale=px.colors.sequential.dense,
                     range_color=(0, 10000000))  # Set the color range

# Display the second graph
st.subheader('Global overview of CO2 emission levels by countries from 1960 to 2019:')
st.plotly_chart(fig2)

# Create the first graph
fig1 = go.Figure()
colors=['orange','green','blue','red','pink']
# Loop through each selected country
j=0
for country in selected_countries:
    # Filter the DataFrame for the current country
    country_df = filtered_df_country[filtered_df_country['country_name'] == country]

    # Add a trace for the current country
    fig1.add_trace(go.Scatter(
        x=country_df['year'],
        y=country_df['value'],
        mode='lines',
        name=country,
        legendgroup=country,
        showlegend=True,
        hovertemplate='Country: %s<br> Year: %%{x}<br> Value: %%{y}' % country
    ))
i=-2
# Loop through each selected event
for event in events:
    i += 10
    if event['name'] in selected_events:
        # Add a dashed vertical line for the selected event year
        fig1.add_shape(
            type="line",
            x0=event['year'],
            y0=0,
            x1=event['year'],
            y1=max_value_country,
            line=dict(dash="dash", color=colors[j])
        )

        # Add a text annotation next to the vertical line
        fig1.add_annotation(
            x=event['year'],
            y=max_value_country,
            yshift=i,
            text=event['name'],
            showarrow=False,
            # xshift=10,
            # yshift=10,
            hovertext=event['name'],  # Set the hovertext to display the event name
            font=dict(color=colors[j])
        )
    j += 1

# Update hover mode
fig1.update_layout(title='Explore countries and regions trends CO2 Emissions and see the effect of global events',
                    hovermode='closest',
                   title_font=dict(size=20)
                   )

# Set the labels for x-axis and y-axis for the first graph
fig1.update_layout(xaxis=dict(title='Year'), yaxis=dict(title='CO2 Emission'))

# Display the first graph
st.subheader('CO2 Emission Trends')
st.plotly_chart(fig1)


# ////////////////////////////////////////////////////////////////////////////////////////////////////
import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression

# Load the data
df = pd.read_csv('co2_emissions_kt_by_country(1).csv')

# Filter the data for the relevant columns and rows (until 1990)
filtered_df = df[df['year'] <= 1990][['country_name', 'year', 'value']]

# Pivot the DataFrame to have years as columns
pivot_df = filtered_df.pivot(index='country_name', columns='year', values='value').reset_index()

# Get the CO2 emission values until 1990 for each country
X = pivot_df.drop(['country_name'], axis=1)

# Create a list to store the predicted values for the year 2020
predicted_values = []
actual_values = []

# Iterate over each country
for i in range(len(X)):
    # Get the CO2 emission values until 1990 for the current country
    X_country = X.iloc[i, :].values.reshape(-1, 1)

    # Get the years until 1990 as the feature
    years = np.array(X.columns).astype(int).reshape(-1, 1)

    # Remove NaN values from X_country and years
    valid_mask = ~np.isnan(X_country.flatten())
    X_country = X_country[valid_mask].reshape(-1, 1)
    years = years[valid_mask].reshape(-1, 1)

    # Create a linear regression model
    model = LinearRegression()
    model.fit(years, X_country)

    # Predict the CO2 emission value for the year 2020
    predicted_value = model.predict([[2019]])

    # Append the predicted value to the list
    predicted_values.append(predicted_value[0])

    # Get the latest available year and actual CO2 emission value for the current country
    latest_year = years[-1][0]
    actual_value = X_country[-1][0]
    actual_values.append(actual_value)

# Add the predicted values and actual values to the DataFrame
pivot_df['predicted_value'] = predicted_values
pivot_df['actual_value'] = actual_values


# Filter the DataFrame for the selected countries
selected_df = pivot_df[pivot_df['country_name'].isin(selected_countries)]
st.subheader('UNFCCC Agreement VS Reality')
st.text('This graph shows the impact of the United Nations Framework Convention on Climate '+"\n"+'Change (UNFCCC). '
        ' This committee, signed in year 1990 by 154 countries. each country '+"\n"+'sighed that in year '
        '@ its emissions will not exceed the emissions in year 1990. '+"\n"+
        'We used a machine learning algorithm to predict the emissions of each country in the '+"\n"+''
        'year 2020 if it had continued on a similar trend from 1960 to 1990. Based on this,'+"\n"+
        ' we can estimate the impact of this committee on the emissions level of different '+"\n"+'countries.'
'The following graph allows us to investigate the impact of the committee.')
# Add the 1990 value for the latest year
fig = go.Figure()

fig.add_trace(go.Bar(
    x=selected_df['country_name'],
    y=selected_df['actual_value'],
    name='CO2 emmision at 1990',
    marker=dict(color='#ffee65'),
    text=selected_df['actual_value'].astype(int),
    textposition='auto'
))

# Initialize an empty list to store the values for 2019
values_2019 = []

# Iterate over each country in selected_df
for country in selected_df['country_name']:
    # Filter df for the specific country and year = 2019, then get the corresponding value
    value_2019 = df.loc[(df['country_name'] == country) & (df['year'] == 2019), 'value'].values
    # Append the value to the list
    values_2019.append(value_2019[0] if len(value_2019) > 0 else None)

# Add the values for 2019 to selected_df as a new column
selected_df['2019'] = values_2019

# Add the 2019 value for the latest year
fig.add_trace(go.Bar(
    x=selected_df['country_name'],
    y=selected_df['2019'],
    name='2019 reality',
    marker=dict(color='#8bd3c7'),
    text=selected_df['2019'].astype(int),
    textposition='auto'
))



# Add the predicted value for 2020
fig.add_trace(go.Bar(
    x=selected_df['country_name'],
    y=selected_df['predicted_value'].apply(lambda x: x[0]),  # Unpack the predicted values
    name='Prediction of 2019 without the UFNCCC ',
    marker=dict(color='#fd7f6f'),
    text=selected_df['predicted_value'].apply(lambda x: int(x[0])),  # Unpack the predicted values
    textposition='auto'
))
# Update the layout of the bar plot
fig.update_layout(
    yaxis_title='CO2 Emission',
    barmode='group',
    legend=dict(orientation='h', x=0.5, y=-0.2),
    height=600
)

# Display the bar plot
st.plotly_chart(fig)

