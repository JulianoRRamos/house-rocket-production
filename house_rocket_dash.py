#Importação de Bibliotecas
import pandas as pd
import numpy as np
import streamlit as st
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
import geopandas
import plotly.express as px
from datetime import datetime

st.set_page_config(layout='wide')

st.title('House Rocket Company')
st.markdown('Welcome to House Rocket Data Analisis')
st.header('Load Data...')

#Read Data
@st.cache(allow_output_mutation=True)
def data_collect(path):
    #Load Dataset
    data = pd.read_csv(path, delimiter=',')
    return data

@st.cache(allow_output_mutation=True)
def get_geofile(url):
    geofile = geopandas.read_file(url)
    return geofile

def set_features(data):
    data['price_m2'] = data['price'] / data['sqft_lot']
    return data

def overview_data(dados):
    fil_attributes = st.sidebar.multiselect('Enter Columns', dados.columns)
    fil_zipcode = st.sidebar.multiselect('Enter zipcode', dados['zipcode'].unique())

    st.title('Data Overview:')

    if (fil_zipcode != []) & (fil_attributes != []):
        dados = dados.loc[dados['zipcode'].isin(fil_zipcode), fil_attributes]
    elif (fil_zipcode != []) & (fil_attributes == []):
        dados = dados.loc[dados['zipcode'].isin(fil_zipcode), :]
    elif (fil_zipcode == []) & (fil_attributes != []):
        dados = dados.loc[:, fil_attributes]
    else:
        dados = dados.copy()

    st.dataframe(dados)

    # Dividindo as tabelas/gráficos/mapas em grid com varias colunas:
    c1, c2 = st.columns((1, 1))

    # Average metrics

    df1 = dados[['id', 'zipcode']].groupby('zipcode').count().reset_index()
    df2 = dados[['price', 'zipcode']].groupby('zipcode').mean().reset_index()
    df3 = dados[['sqft_living', 'zipcode']].groupby('zipcode').mean().reset_index()
    df4 = dados[['price_m2', 'zipcode']].groupby('zipcode').mean().reset_index()

    # #Merge de metricas
    m1 = pd.merge(df1, df2, on='zipcode', how='inner')
    m2 = pd.merge(m1, df3, on='zipcode', how='inner')
    df = pd.merge(m2, df3, on='zipcode', how='inner')

    df.columns = ['ZipCode', 'Total Houses', 'Price', 'Sqrl_Living', 'Price/m²']

    c1.header('Average Values:')
    c1.dataframe(df, height=600)

    # Filters
    num_attributes = dados.select_dtypes(include=['int64', 'float64'])
    media = pd.DataFrame(num_attributes.apply(np.mean))
    mediana = pd.DataFrame(num_attributes.apply(np.median))
    desviop = pd.DataFrame(num_attributes.apply(np.std))

    maximo = pd.DataFrame(num_attributes.apply(np.max))
    minimo = pd.DataFrame(num_attributes.apply(np.min))

    dfStat = pd.concat([maximo, minimo, media, mediana, desviop], axis=1).reset_index()
    dfStat.columns = ['Atributos', 'Maximo', 'Minimo', 'Media', 'Mediana', 'DesvioPadrao']

    c2.header('Statistics Descriptions:')
    c2.dataframe(dfStat, height=600)

    return None

def portfolio_density(dados, geofile):
    st.title('Region Overview:')
    st.header('Portfolio Density')

    c3, c4 = st.columns((1, 1))

    df5 = dados.sample(2000)

    # Base Map
    density_map = folium.Map(location=[dados['lat'].mean(), dados['long'].mean()], default_zoom_start=15)

    marker_cluster = MarkerCluster().add_to(density_map)
    for name, row in df5.iterrows():
        folium.Marker([row['lat'],
                       row['long']],
                       popup='Sold R${0} on: {1}. Features: {2} sqft, {3} bedrooms, {4} bathrooms, year built: {5}'.format(
                           row['price'],
                           row['date'],
                           row['sqft_living'],
                           row['bedrooms'],
                           row['bathrooms'],
                           row['yr_built'])).add_to(marker_cluster)
    with c3:
        folium_static(density_map)

    # Region Price Map
    # c4.header('Price Density')
    #
    # df6 = dados[['price', 'zipcode']].groupby('zipcode').mean().reset_index()
    # df6.columns = ['ZIP', 'PRICE']
    #
    # #c4.dataframe(df6, height=600)
    #
    # geofile = geofile[geofile['ZIP'].isin(df6['ZIP'].tolist())]
    #
    # region_price_map = folium.Map(location=[dados['lat'].mean(), dados['long'].mean()], default_zoom_start=15)

    # region_price_map.choropleth(
    #                 geo_data=geofile,
    #                 data=df6,
    #                 columns=['ZIP', 'PRICE'],
    #                 key_on='feature.properties.ZIP',
    #                 fill_color='YlOrRd',
    #                 fill_opacity=0.7,
    #                 line_opacity=0.2,
    #                 legend_name='AVG PRICE'
    #                 )
    #
    # with c4:
    #     folium_static(region_price_map)

    return None


def commercial_category(dados):
    st.sidebar.title('Commercial Options:')
    st.title('Commercial Attributes:')

    # ---------Preço por ano
    dados['date'] = pd.to_datetime(dados['date']).dt.strftime('%Y-%m-%d')

    # Filters
    min_year_built = int(dados['yr_built'].min())
    max_year_built = int(dados['yr_built'].max())
    st.sidebar.subheader('Selecione o ano máximo de construção:')
    fil_year_built = st.sidebar.slider('Ano de Construção', min_year_built, max_year_built, min_year_built)

    st.header('Average price per Year Built')
    # Data Filters
    dfPrecoAno = dados.loc[dados['yr_built'] < fil_year_built]
    dfPrecoAno = dfPrecoAno[['yr_built', 'price']].groupby('yr_built').mean().reset_index()
    # Data Plot
    fig = px.line(dfPrecoAno, x='yr_built', y='price')
    st.plotly_chart(fig, use_container_width=True)

    # ---------Preço por dia
    st.header('Average price per Day')
    st.sidebar.subheader('Selecione a data máxima:')

    # Filters
    min_date = datetime.strptime(dados['date'].min(), '%Y-%m-%d')
    max_date = datetime.strptime(dados['date'].max(), '%Y-%m-%d')
    fil_date = st.sidebar.slider('Date', min_date, max_date, min_date)

    # Data Filters
    dados['date'] = pd.to_datetime(dados['date'])
    dfPrecoDia = dados.loc[dados['date'] < fil_date]
    dfPrecoDia = dfPrecoDia[['date', 'price']].groupby('date').mean().reset_index()

    # Data Plot
    fig = px.line(dfPrecoDia, x='date', y='price')
    st.plotly_chart(fig, use_container_width=True)

    # ---------Histograma
    st.header('Price Distribution')
    st.sidebar.subheader('Selecione o preço máximo:')

    # Filters
    min_price = int(dados['price'].min())
    max_price = int(dados['price'].max())
    mean_price = int(dados['price'].mean())

    # Data Filters
    fil_price = st.sidebar.slider('Price', min_price, max_price, mean_price)
    dfPrice = dados.loc[dados['price'] < fil_price]

    # Data Plot
    fig = px.histogram(dfPrice, x='price', nbins=50)
    st.plotly_chart(fig, use_container_width=True)

    return None

def attributes_distribution(dados):
    st.sidebar.title('Attributes Options')
    st.title('House Attributes')

    #------------House per bedrooms

    c5, c6 = st.columns((1, 1))
    c5.header('Houses per bedrooms')

    # Data Filters
    fil_bedrooms = st.sidebar.selectbox('Número máximo de Quartos', sorted(set(dados['bedrooms'].unique())))
    fil_bathrooms = st.sidebar.selectbox('Número máximo de Banheiros', sorted(set(dados['bathrooms'].unique())))
    fil_floors = st.sidebar.selectbox('Número máximo de andáres', sorted(set(dados['floors'].unique())))
    fil_waterview = st.sidebar.checkbox('Somente casas com vista para o mar')

    dfBedrooms = dados[dados['bedrooms'] < fil_bedrooms]

    # Data Plot
    fig = px.histogram(dfBedrooms, x='bedrooms', nbins=19, color_discrete_sequence=['indianred'])
    c5.plotly_chart(fig, use_container_width=True)

    #------------House per bathrooms
    c6.header('Houses per bathrooms')
    # Data Filters
    dfBathrooms = dados[dados['bathrooms'] < fil_bathrooms]
    # Data Plot
    fig = px.histogram(dfBathrooms, x='bathrooms', nbins=19, color_discrete_sequence=['#330C73'])
    c6.plotly_chart(fig, use_container_width=True)

    c7, c8 = st.columns((1, 1))

    #------------House per floors
    c7.header('Houses per floors')
    # Data Filters
    dfFloors = dados[dados['floors'] < fil_floors]
    # Data Plot
    fig = px.histogram(dfFloors, x='floors', nbins=19, color_discrete_sequence=['#A56369'])
    c7.plotly_chart(fig, use_container_width=True)

    #------------House per water view
    c8.header('Houses weater view')
    # Data Filters
    if fil_waterview:
        dfWaterView = dados[dados['waterfront'] == 1]
    else:
        dfWaterView = dados[['id', 'waterfront']].copy()

    # Data Plot
    fig = px.histogram(dfWaterView, x='waterfront', nbins=19, color_discrete_sequence=['#65DDDD'])
    c8.plotly_chart(fig, use_container_width=True)

    return None

if __name__ == '__main__':
    #ETL
    path = 'dados/kc_house_data.csv'
    url = 'https://opendata.arcgis.com/datasets/83fc2e72903343aabff6de8cb445b81c_2.geojson'
    #Data Extraction
    dados = data_collect(path)
    geofile = get_geofile(url)

    #Transformation
    dados = set_features(dados)
    overview_data(dados)
    portfolio_density(dados, geofile)
    commercial_category(dados)
    attributes_distribution(dados)

    #Loading






