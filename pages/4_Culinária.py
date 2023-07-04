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
df2 = df1.copy()
#--------------------------------------------------------------------------- Funções Da Página ----------------------------------------------------------------------------

def cuisinescol1(df2):
        
    i = (df1.loc[(df1['cuisines'] == 'Italian') , [ 'aggregate_rating', 'restaurant_name', 'restaurant_id', 'votes']]
     .sort_values(['aggregate_rating','votes'], ascending = False).iloc[0,1])
    j = (df1.loc[(df1['cuisines'] == 'Italian') , [ 'aggregate_rating', 'restaurant_name', 'restaurant_id', 'votes']]
     .sort_values(['aggregate_rating','votes'], ascending = False).iloc[0,0])
    st.metric(f'Italiana: {i}',value=f'{j}/5.0')
    return None

def cuisinescol2(df1):
    
    i = (df1.loc[(df1['cuisines'] == 'American') , [ 'aggregate_rating','votes', 'restaurant_name', 'restaurant_id' ]]
     .sort_values(['aggregate_rating','votes', 'restaurant_id'], ascending = False).iloc[0,2])

    j = (df1.loc[(df1['cuisines'] == 'American') , [ 'aggregate_rating','votes', 'restaurant_name', 'restaurant_id' ]]
     .sort_values(['aggregate_rating','votes', 'restaurant_id'], ascending = False).iloc[0,0])
    st.metric(f'American: {i}',value=f'{j}/5.0')
    return None

def cuisinescol3(df1):
    i = (df1.loc[(df1['cuisines'] == 'Arabian') , ['restaurant_name', 'aggregate_rating','votes', 'restaurant_id' ]]
     .sort_values(['aggregate_rating','votes', 'restaurant_id'], ascending = False).iloc[0,0])
    j = (df1.loc[(df1['cuisines'] == 'Arabian') , ['restaurant_name', 'aggregate_rating','votes', 'restaurant_id' ]]
     .sort_values(['aggregate_rating','votes', 'restaurant_id'], ascending = False).iloc[0,1])
    
    st.metric(f'Arabian: {i}',value=f'{j}/5.0')
    return None

def cuisinescol4(df1):
    i = (df1.loc[(df1['cuisines'] == 'Japanese') , ['restaurant_name', 'aggregate_rating','votes', 'restaurant_id' ]]
     .sort_values(['aggregate_rating','votes', 'restaurant_id'], ascending = False).iloc[0,0])
    j = (df1.loc[(df1['cuisines'] == 'Japanese') , ['restaurant_name', 'aggregate_rating','votes', 'restaurant_id' ]]
     .sort_values(['aggregate_rating','votes', 'restaurant_id'], ascending = False).iloc[0,1])
    st.metric(f'Japanese: {i}',value=f'{j}/5.0')
    return None

def cuisinescol5(df1):
    i = (df1.loc[(df1['cuisines'] == 'Brazilian') , ['restaurant_name', 'aggregate_rating','votes', 'restaurant_id' ]]
     .sort_values(['aggregate_rating','votes', 'restaurant_id'], ascending = False).iloc[0,0])
    j = (df1.loc[(df1['cuisines'] == 'Brazilian') , ['restaurant_name', 'aggregate_rating','votes', 'restaurant_id' ]]
     .sort_values(['aggregate_rating','votes', 'restaurant_id'], ascending = False).iloc[0,1])
    st.metric(f'Brazilian: {i}',value=f'{j}/5.0')
    return None

def topcuisines(df2):
        grafico = (df2.loc[:, ['cuisines','aggregate_rating','votes', 'restaurant_id']]
     .groupby(['cuisines']).max().reset_index()
     .sort_values([ 'aggregate_rating', 'votes', 'restaurant_id'], ascending = False).head(5))
        fig = px.bar(grafico.head(5), x= 'cuisines', y = 'aggregate_rating',text_auto=".2f" , title= 'Melhores culinárias', labels={
            "aggregate_rating": "Nota",
            "cuisines": "Tipos Culinários.",
        })
        return fig 
        
def bottomcuisines(df2):
        grafico = (df2.loc[:, ['cuisines','aggregate_rating','votes', 'restaurant_id']]
     .groupby(['cuisines']).max().reset_index()
     .sort_values(['aggregate_rating', 'votes', 'restaurant_id'], ascending = True).head(5))
        fig = px.bar(grafico.head(5), x= 'cuisines', y = 'aggregate_rating',text_auto=".2f" , title= 'Piores culinárias', labels={
            "aggregate_rating": "Nota",
            "cuisines": "Tipos Culinários.",
        })
        return fig 

def topdfrest(df2):
    st.markdown ('# Top 10 Restaurantes')
    
    df_top_rest = (df2.loc[:, ['restaurant_name','cuisines','city','country_code','aggregate_rating','votes', 'restaurant_id']]
     .sort_values(['aggregate_rating', 'votes', 'restaurant_id'], ascending = False)).head(10)
    df_top_rest
    
    return df_top_rest

# -------------------------------------------------------------------- Inicio da estrutura do código ----------------------------------------------------------------------


#------------------------------------------------
#Sidebar
#------------------------------------------------

st.set_page_config(page_title='Culinária',page_icon='🍽️',layout="wide")

st.header( 'Visão Culinária 🍽️ ' )
st.markdown('### Melhores Restaurantes dos Principais tipos Culinárioss !')

#image_path = 'logo.png'

image = Image.open( 'logo.png' )

st.sidebar.image( image, width=100)

st.sidebar.markdown ( '# Fome Zero' )
 
st.sidebar.markdown ( '## Visualize as informações das cidades cadastradas !' )

st.sidebar.markdown ("""---""")

st.sidebar.markdown("# Utilize os filtros!")

st.sidebar.markdown("## Países:")

filtroculinaria = st.sidebar.multiselect(
    "Escolha os Tipos de Culinária",
    df2.loc[:, "cuisines"].unique().tolist(),
    default=["Japanese","Brazilian","Arabian",'Mineira', 'Durban','Armenian']
)

linhas_selecionadas_cuisines = df1['cuisines'].isin( filtroculinaria )
df2 = df2.loc[linhas_selecionadas_cuisines, :]

st.sidebar.markdown("## Quantidade de restaurantes:")
date_slider = st.sidebar.slider("Quantidade:",value=6929,min_value=1, max_value=6929)
linhas_selecionadas_slider = df2['index'] <= date_slider
df2 = df2.loc[linhas_selecionadas_slider, :]

filtropais = st.sidebar.multiselect("Escolha os Países:",df2.loc[:, "country_code"].unique().tolist(),default=["Brazil","England","Canada", "Australia"])

linhas_selecionadas_countries = df2['country_code'].isin( filtropais )
df2 = df2.loc[linhas_selecionadas_countries, :]


st.sidebar.markdown ("""---""")
st.sidebar.markdown('#### Powered by Matheus Pinheiro')

#==================================================================================================
#layout Streamlit
#==================================================================================================


with st.container():
    col1, col2, col3 , col4, col5 = st.columns(5, gap='small')
    
    with col1:
        cuisinescol1(df1)
    
    with col2:
        cuisinescol2(df1)
    
    with col3:
        cuisinescol3(df1)

    with col4:
        cuisinescol4(df1)
   
    with col5:
        cuisinescol5(df1)
        
with st.container():
        topdfrest(df2)
    
with st.container():
        
    col1, col2 = st.columns(2, gap='large')
        
    with col1:
        fig = topcuisines(df2)
        fig.update_layout( width=350, height=500)
        st.plotly_chart (fig, use_countainer=True)
    
    
    with col2:
        fig = bottomcuisines(df2)
        fig.update_layout( width=350, height=500)
        st.plotly_chart (fig, use_countainer=True)
