# Importação Bibliotecas

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


#---------------------------------------------------------- Funções De Limpeza -----------------------------------------------------

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

#--------------------------------------------------------------------------- Funções Da Página ----------------------------------------------------------------------------


def restauranteporpais(df1):
    
    i = ['country_code', 'restaurant_id']

    grafico = df1.loc[:,i].groupby(['country_code']).count().reset_index().sort_values('restaurant_id',ascending=False)

    fig = px.bar(grafico, x= 'country_code', y= 'restaurant_id',text_auto=".2f", title= 'Restaurantes registrados por País.', labels={
            "country_code": "País",
            "restaurant_id": "Quantidade de Restaurantes",
        })
    
    return fig


def cidadesporpais(df1):
    i = ['city', 'country_code']

    grafico = df1.loc[:,i].groupby(['country_code']).nunique().reset_index().sort_values('city',ascending=False)

    fig = px.bar(grafico, x= 'country_code', y= 'city', text_auto=".2f", title= 'Cidades registrados por País.', labels={
            "country_code": "País",
            "city": "Quantidade de Cidades",
        })
    return fig

def mediaavaliacao(df1):  
        
    i = ['country_code', 'votes']

    grafico = df1.loc[:,i].groupby(['country_code']).mean().reset_index().sort_values('votes',ascending=False)

    fig = px.bar(grafico, x= 'country_code', y= 'votes',text_auto=".2f", title= 'Média de avaliações por País.', labels={
            "country_code": "País",
            "votes": "Média de Avaliações",
    })
    return fig
    

def precoparadois(df1): 
        
        i = ['country_code', 'average_cost_for_two']

        grafico = df1.loc[:,i].groupby(['country_code']).mean().reset_index().sort_values('average_cost_for_two',ascending=False)

        fig = px.bar(grafico, x= 'country_code', y= 'average_cost_for_two',text_auto=".2f", title= 'Média de preço de prato para dois.', labels={
            "country_code": "País",
            "average_cost_for_two": "Média de preço de prato para dois",
        })
        return fig


# -------------------------------------------------------------------- Inicio da estrutura do código ----------------------------------------------------------------------


#------------------------------------------------
#Sidebar
#------------------------------------------------

st.set_page_config(page_title='Países',page_icon='🌎',layout="wide")

st.header( 'Visão dos Países 🌎 ' )

#image_path = 'logo.png'

image = Image.open( 'logo.png' )

st.sidebar.image( image, width=100)

st.sidebar.markdown ( '# Fome Zero' )

st.sidebar.markdown ( '## Visualize as informações dos países e nosso banco de dados!' )

st.sidebar.markdown ("""---""")

st.sidebar.markdown("## Filtros")

countries = st.sidebar.multiselect(
    "Escolha os Países:",
    df1.loc[:, "country_code"].unique().tolist(),
    default=["Brazil", "England", "Qatar", "South Africa", "Canada", "Australia"],
    )

linhas_selecionadas = df1['country_code'].isin( countries )

df1 = df1.loc[linhas_selecionadas, :]


st.sidebar.markdown ("""---""")
st.sidebar.markdown('#### Powered by Matheus Pinheiro')

#==================================================================================================
#layout Streamlit
#==================================================================================================


with st.container():
    
    fig = restauranteporpais(df1)
    fig.update_layout( width=700, height=500)
    st.plotly_chart (fig, use_countainer=True)
    
with st.container():
    
    fig = cidadesporpais(df1)
    fig.update_layout( width=700, height=500)
    st.plotly_chart (fig, use_countainer=True)
    
with st.container():
    st.markdown('## Os mais diversos restaurantes nas mais diversas localidades:')
        
    col1, col2 = st.columns(2, gap='large')
        
    with col1:
        
        fig = mediaavaliacao(df1)
        fig.update_layout( width=350, height=400)
        st.plotly_chart (fig, use_countainer=True)
            
    with col2:
        
        fig = precoparadois(df1)
        fig.update_layout( width=350, height=400)
        st.plotly_chart (fig, use_countainer=True)   
