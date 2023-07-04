import pandas as pd
import plotly.express as px
import inflection
import numpy as np
import streamlit as st
from PIL import Image
import folium
from folium.plugins import MarkerCluster
from PIL import Image
from streamlit_folium import folium_static

# Importando dados
df = pd.read_csv('zomato.csv')
df1 = df.copy()
# Limpando dados
#------------------------------------------------------------------------ Funções -----------------------------------------------------------------------------------------


#Renomear as colunas do DataFrame

def rename_columns(dataframe):
    df1 = dataframe.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df1.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df1.columns = cols_new
    return df1

df1 = rename_columns(df1)

#Redefinindo códigos da coluna 'Country_Code' para nomes dos paises.

countries = {
    1: 'India',
    14: 'Australia', 
    30: 'Brazil', 
    37: 'Canada', 
    94: 'Indonesia', 
    148: 'New Zeland', 
    162: 'Philippines', 
    166: 'Qatar', 
    184: 'Singapure', 
    189: 'South Africa', 
    191: 'Sri Lanka', 
    208: 'Turkey', 
    214: 'United Arab Emirates',
    215: 'England', 
    216: 'United States of America' 
}

def country_name(country_code):
    return countries[country_code]

df1['country_code'] = df1['country_code'].apply(country_name)

#Criação do Tipo de Categoria de Comida

def create_price_type(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"

df1["price_range_description"] = df1["price_range"].apply(create_price_type)
    
#Criação do nome das Cores

COLORS = {
    "3F7E00": "darkgreen",
    "5BA829": "green",
    "9ACD32": "lightgreen",
    "CDD614": "orange",
    "FFBA00": "red",
    "CBCBC8": "darkred",
    "FF7800": "darkred",
}

def color_name(color_code):
    return COLORS[color_code]

df1['color_name'] = df1['rating_color'].apply(color_name)



def clean_code(df1):

    df1.drop('switch_to_order_menu', axis=1, inplace=True)
    df1 = df1.dropna()
    df1["cuisines"] = df1.loc[:, "cuisines"].apply(lambda x: x.split(",")[0])
    df1 = df1.drop_duplicates().reset_index()
    return df1

df1 = clean_code( df1 )


#------------------------------------------------
#Funções Da Pagina
#------------------------------------------------


df2= df1.copy()

def MapaLocalizacao(df2):
    Mapa = (df2.loc[:, ['city', 'longitude', 'latitude', 'average_cost_for_two','cuisines']]
           .groupby(['city','cuisines', 'average_cost_for_two']).median().reset_index())

# Criar o mapa com o objeto Mapa_folium
    Mapa_folium = folium.Map()

# Criar o objeto MarkerCluster
    marker_cluster = MarkerCluster().add_to(Mapa_folium)

    for index, location_info in df2.iterrows():
        name = location_info["restaurant_name"]
        price_for_two = location_info["average_cost_for_two"]
        cuisine = location_info["cuisines"]
        currency = location_info["currency"]
        rating = location_info["aggregate_rating"]
        color = f'{location_info["color_name"]}'

        html = "<p><strong>{}</strong></p>"
        html += "<p>Price: {},00 ({}) para dois"
        html += "<br />Type: {}"
        html += "<br />Aggragate Rating: {}/5.0"
        html = html.format(name, price_for_two, currency, cuisine, rating)

        popup = folium.Popup(
                folium.Html(html, script=True),
                max_width=500,
            )
        folium.Marker([location_info['latitude'], location_info['longitude']], popup=popup, icon=folium.Icon(color=color, icon="home", prefix="fa")).add_to(marker_cluster)

    folium_static(Mapa_folium, width=700, height=450)

    return None 

# -------------------------------------------------------------------- Inicio da estrutura do código ----------------------------------------------------------------------


#------------------------------------------------
#Sidebar
#------------------------------------------------

st.set_page_config(page_title='Fome zero',page_icon='🍽️',layout="wide")

st.header( 'Fome Zero'  )

#image_path = 'logo.png'

image = Image.open( 'logo.png' )

st.sidebar.image( image, width=100)

st.sidebar.markdown ( '# Fome Zero' )

st.sidebar.markdown ( '## A melhor opção perto de você!' )

st.sidebar.markdown ("""---""")

st.sidebar.markdown("## Filtros")

countries = st.sidebar.multiselect(
    "Escolha os Paises:",
    df2.loc[:, "country_code"].unique().tolist(),
    default=["Brazil", "England", "Qatar", "South Africa", "Canada", "Australia"],
    )

linhas_selecionadas = df2['country_code'].isin( countries )

df2 = df2.loc[linhas_selecionadas, :]

st.sidebar.markdown ("""---""")

st.sidebar.markdown("### Dados Tratados")

processed_data = pd.read_csv("zomato.csv")

st.sidebar.download_button(
    label="Download",
    data=processed_data.to_csv(index=False, sep=";"),
    file_name="zomato.csv",
    mime="text/csv",
    )

st.sidebar.markdown ("""---""")
st.sidebar.markdown('#### Powered by Matheus Pinheiro')

#==================================================================================================
#layout Streamlit
#==================================================================================================


#------------------------------------------------
#Visão Geral
#------------------------------------------------


with st.container():
        st.markdown(""" 
        
            -  Visão Geral:
                - Visão Geral: Dados gerais que totalizam nosso banco de dados.
                - Visão Geográfica: Indicadores de Insights Geográficos. (Cores: Verde : Bom | Vermelhor : Ruim)               
            
            """)
        
        col1, col2 , col3, col4, col5 = st.columns(5, gap='large')
        
        with col1:
            quantidade_rest = df1['restaurant_id'].count()
            col1.metric('Restaurantes', quantidade_rest)
            
        with col2:
            paises_unicos = df1['country_code'].nunique()
            col2.metric('Paises', paises_unicos)
            
        with col3:
            cidades_unicas = df1['city'].nunique()
            col3.metric('Cidades', cidades_unicas)
            
        with col4:
            avaliacoes_total = df1['votes'].sum()
            col4.metric('Total de avaliações', avaliacoes_total)   
        
        with col5:
            culinarias_disponiveis = df1.loc[:, 'cuisines'].nunique()
            col5.metric('Culinarias disponiveis', culinarias_disponiveis)

        st.sidebar.markdown ("""---""")


with st.container():
    st.markdown('### localização dos restaurantes. ')
    MapaLocalizacao(df2)
    
