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

def quantidadederestporciy(df1):
    grafico = (df1.loc[:, ['city','restaurant_id','country_code']].groupby(['country_code','city'])
                                         .nunique()
                                         .reset_index()
                                         .sort_values(['restaurant_id', 'city'], ascending = False))
    grafico = grafico
    fig = px.bar(grafico.head(10), x= 'city', y= 'restaurant_id',text_auto=".2f",
        color="country_code", title= 'Cidades com mais restaurantes registrados.', labels={
            "city": "Cidade",
            "restaurant_id": "Quantidade de Restaurantes", 'country_code' : 'Países'
        })
    return fig

def restnota4(df1):
    grafico = (df1.loc[df1['aggregate_rating'] >= 4, ['city','restaurant_id', 'country_code']].groupby(['country_code','city'])
                                                                   .count().reset_index()
                                                                   .sort_values(['restaurant_id','city'], ascending = [False, True]))
    fig = px.bar(grafico.head(7), x= 'city', y = 'restaurant_id',color = 'country_code', title= 'Cidades com mais restaurantes nota 4+.',text_auto=".2f", labels={
            "city": "Cidade",
            "restaurant_id": "Quantidade de Restaurantes",
            'country_code' : 'Países'
        })
    return fig

def bottom2emeiorest(df1):
    grafico = (df1.loc[df1['aggregate_rating'] <= 2.5, ["restaurant_id", "country_code", "city"],
        ]
        .groupby(["country_code", "city"])
        .count()
        .sort_values(["restaurant_id", "city"], ascending=[False,True])
        .reset_index()
    )

    fig = px.bar(grafico.head(7), x="city", y="restaurant_id", text="restaurant_id", text_auto=".2f", color = 'country_code',
        title="Cidades com restaurantes nota abaixo de 2.5", labels={
            "city": "Cidade", "restaurant_id": "Quantidade de Restaurantes",
            "country_code": "País",
        },
    )
    return fig
    
def tipodeculinaria(df1):
    grafico = (df1.loc[:, ['city', 'country_code','cuisines']].groupby(['country_code','city'])
                                            .nunique().reset_index()
                                            .sort_values('cuisines', ascending = False))

    fig = px.bar(grafico.head(10), x= 'city', y = 'cuisines',color = 'country_code',text_auto=".2f" , title= 'Cidades com restaurantes com mais tipos de culinaria', labels={
            "city": "Cidade",
            "cuisines": "Quantidade de Tipos Culinários.",
            'country_code' : 'Países'
        })
    return fig



# -------------------------------------------------------------------- Inicio da estrutura do código ----------------------------------------------------------------------


#------------------------------------------------
#Sidebar
#------------------------------------------------

st.set_page_config(page_title='Cidades',page_icon='🏙️',layout="wide")

st.header( 'Visão das Cidades 🌎 ' )
st.markdown('### Metricas para analise por cidade !')
st.markdown("""---""")

#image_path = 'logo.png'

image = Image.open( 'logo.png' )

st.sidebar.image( image, width=100)

st.sidebar.markdown ( '# Fome Zero' )
 
st.sidebar.markdown ( '## Visualize as informações das cidades cadastradas !' )

st.sidebar.markdown ("""---""")

st.sidebar.markdown("## Filtros")

countries = st.sidebar.multiselect("Escolha os Países:", 
                                   df1.loc[:, "country_code"].unique().tolist(),default=["Brazil", "England", "Qatar", "South Africa", "Canada", "Australia"],)

linhas_selecionadas = df1['country_code'].isin( countries )

df1 = df1.loc[linhas_selecionadas , :]

st.sidebar.markdown ("""---""")
st.sidebar.markdown('#### Powered by Matheus Pinheiro')

#==================================================================================================
#layout Streamlit
#==================================================================================================


with st.container():
    
    fig = quantidadederestporciy(df1)
    fig.update_layout( width=700, height=500)
    st.plotly_chart (fig, use_countainer=True)
    
with st.container():
        
    col1, col2 = st.columns(2, gap='large')
        
    with col1:
        
        fig = restnota4(df1)
        fig.update_layout( width=350, height=500)
        st.plotly_chart (fig, use_countainer=True)
            
    with col2:
        
        fig = bottom2emeiorest(df1)
        fig.update_layout( width=350, height=500)
        st.plotly_chart (fig, use_countainer=True)
    
with st.container():
    
    fig = tipodeculinaria(df1)
    fig.update_layout( width=700, height=500)
    st.plotly_chart (fig, use_countainer=True)
    