import streamlit as st
from PIL import Image
import pandas as pd

st.set_page_config(page_title='Home',page_icon='🏠',layout="wide")

#------------------------------------------------
#Sidebar
#------------------------------------------------
#image_path = 'logo.png'

image = Image.open( 'logo.png' )

st.sidebar.image( image, width=100)

st.sidebar.markdown ( '# Fome Zero' )

st.sidebar.markdown ( '## A melhor opção perto de você!' )

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

st.write('# Projeto Fome Zero')

st.markdown(""" 
           Dashboard desenvolvido para visualização dos indicadores visando á analise de qualidade, tipo de culinárias e licalização dos restaurantes. 
           ### Índice de navegação:

            - Home Page: 
            
                - Visão Geral: Dados gerais que totalizam nosso banco de dados.
                - Visão Geográfica: Indicadores de Insights Geográficos. 
                
            - Visão Países: 
            
                - Média de restaurantes e suas avaliações correspondentes.     
                
            - Visão Cidades:
            
                - Médias correspondentes a quantidades de restaurantes e tipos de culinária por Cidade.
                
            - Visão Culinária:
            
                - Métricas dos melhores restaurantes com os principais tipos culinários !
            
            ### Contato para ajuda:
                - 📧  Matheussouzads@icloud.com
            """)