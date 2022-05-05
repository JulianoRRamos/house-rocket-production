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

    # Merge de metricas
    m1 = pd.merge(df1, df2, on='zipcode', how='inner')
    m2 = pd.merge(m1, df3, on='zipcode', how='inner')
    df = pd.merge(m2, df3, on='zipcode', how='inner')

    df.columns = ['ZipCode', 'Total Houses', 'Price', 'Sqrl_Living', 'Price/m²']

    c1.header('Average Values:')
    c1.dataframe(df[['ZipCode', 'Total Houses', 'Price', 'Price/m²']], height=600)

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

    #--------------Indicação de Compra
    # Novo Dataframe com coluna price_median_reg agrupando preço por região (cep)
    dfBuy = dados[['price', 'zipcode']].groupby('zipcode').median().reset_index()
    dfBuy.rename(columns={'price': 'price_median_reg'}, inplace=True)
    # Novo DataFrame merge com o principal
    dfMedianPriceZip = pd.merge(dados, dfBuy, on='zipcode', how='inner')
    # Nova coluna com status se deve comprar ou não
    # - Comprar aqueles com preço menor do que a média da região e for imóvel de boa condição
    dfMedianPriceZip['status_buy'] = 'not buy'
    for i, row in dfMedianPriceZip.iterrows():
        if (row["price"] < row["price_median_reg"]) & (row["condition"] >= 2):
            dfMedianPriceZip.at[i, 'status_buy'] = 'yes buy'
    if (fil_zipcode != []):
        dfMedianPriceZip = dfMedianPriceZip.loc[dfMedianPriceZip['zipcode'].isin(fil_zipcode), :]

    st.header('Indication of purchase - criteria:\n- Properties that are below the median price in the region\n- And that they are in good condition.')
    st.dataframe(dfMedianPriceZip[['id', 'zipcode', 'price', 'price_median_reg', 'condition','status_buy']].sort_values(by=['condition','status_buy'],ascending=False), height=600)

    # --------------Indicação de Venda
    st.header('''Indication of the best price and time to sell them:\n 
              SALE CONDITIONS: 
              - 1. If the purchase price is greater than the regional median + seasonality: 
                  The sale price will be equal to the purchase price + 10%\n
              - 2. If the purchase price is less than the regional median + seasonality: 
              The sale price will be equal to the purchase price + 30%''')
    # Criando coluna de preço médio por região
    df2 = dados[['price', 'zipcode']].groupby('zipcode').median().reset_index()
    df2.rename(columns={'price': 'price_median_reg'}, inplace=True)

    # Coletando estação do ano de acordo com a data de compra (date)
    dados['month'] = pd.DatetimeIndex(dados['date']).month
    dados['season'] = dados['month'].apply(lambda x: 'spring' if 3 < x < 5 else
    'summer' if 6 < x < 8 else
    'fall' if 9 < x < 11
    else 'winter')
    # Criando coluna de preço médio por estação do ano
    df3 = dados[['price', 'season']].groupby(['season']).median().reset_index()
    df3.rename(columns={'price': 'price_median_season'}, inplace=True)

    # Novo DataFrame merge com o principal
    dfTmp = pd.merge(dados, df2, on='zipcode', how='inner')
    dfSeasonReg = pd.merge(dfTmp, df3, on='season', how='inner')

    dfSeasonReg['sale_price'] = 0.0
    for i, row in dfSeasonReg.iterrows():
        if (row["price"] > row["price_median_reg"]) & (row["price"] > row["price_median_season"]):
            dfSeasonReg.at[i, 'sale_price'] = float(row["price"]) + (float(row["price"]) * 0.1)
        else:
            dfSeasonReg.at[i, 'sale_price'] = float(row["price"]) + (float(row["price"]) * 0.3)

    if (fil_zipcode != []):
        dfSeasonReg = dfSeasonReg.loc[dfSeasonReg['zipcode'].isin(fil_zipcode), :]

    st.dataframe(dfSeasonReg[['id', 'season', 'zipcode', 'price', 'price_median_reg', 'price_median_season', 'sale_price']].sort_values(by=['sale_price'], ascending=False), height=600)

    return None

def portfolio_density(dados, geofile):
    st.title('Region Overview:')
    st.header('Portfolio Density')

    c3, c4 = st.columns((1, 1))

    #Base reduzida para testes
    df5 = dados.sample(2000)

    #Base completa - produção:
    #df5 = dados.copy()

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
    st.title('Commercial Attributes (average price):')

    # ---------Preço por ano

    c10, c11 = st.columns((2, 4))

    dados['date'] = pd.to_datetime(dados['date']).dt.strftime('%Y-%m-%d')

    # Filters
    min_year_built = int(dados['yr_built'].min())
    max_year_built = int(dados['yr_built'].max())
    st.sidebar.subheader('Select maximum construction year:')
    fil_year_built = st.sidebar.slider('Build Year', min_year_built, max_year_built, min_year_built)

    c10.header('per Year Built')
    # Data Filters
    dfPrecoAno = dados.loc[dados['yr_built'] < fil_year_built]
    dfPrecoAno = dfPrecoAno[['yr_built', 'price']].groupby('yr_built').mean().reset_index()

    c10.dataframe(dfPrecoAno)
    # Data Plot
    fig = px.line(dfPrecoAno, x='yr_built', y='price', title="Price evolution per year")
    c11.plotly_chart(fig, use_container_width=True)

    # ---------Preço por dia
    st.header('per Day')
    st.sidebar.subheader('Select the maximum date:')

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

    # ---------Preço por mês
    c12, c13 = st.columns((2, 4))

    dados['data'] = pd.to_datetime(dados['date'])
    dados['month'] = pd.to_datetime(dados['data'].dt.year.astype(str) + "-" + dados['data'].dt.month.astype(str) + "-" + "01")

    # Filters

    c12.header('per Month')
    # Data Filters
    dfMediaPrecoPorMes = dados[['price', 'month']].groupby('month').mean().reset_index()
    c12.dataframe(dfMediaPrecoPorMes, height=600)
    dfPrecoMes = dfMediaPrecoPorMes.loc[dfMediaPrecoPorMes['month'] < fil_date]

    # Data Plot
    fig = px.line(dfPrecoMes, x='month', y='price', markers=True, title= "Monthly price evolution")
    c13.plotly_chart(fig, use_container_width=True)


    # ---------Histograma
    st.header('Price Distribution')
    st.sidebar.subheader('Select maximum price:')

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
    fil_bedrooms = st.sidebar.selectbox('Maximum number of Rooms', sorted(set(dados['bedrooms'].unique())))
    fil_bathrooms = st.sidebar.selectbox('Maximum number of Bathrooms', sorted(set(dados['bathrooms'].unique())))
    fil_floors = st.sidebar.selectbox('Maximum number of floors', sorted(set(dados['floors'].unique())))
    fil_waterview = st.sidebar.checkbox('Only houses overlooking the sea')

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






