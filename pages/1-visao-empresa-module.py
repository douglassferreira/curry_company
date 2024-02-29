# Libraries
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go
 
# bibliotecas necessárias
import folium
import pandas as pd
import streamlit as st
from PIL import Image
from datetime import datetime
from streamlit_folium import folium_static



st.set_page_config(page_title = 'Visão Empresa', page_icon = '📈', layout = 'wide')

#-------------------------------------------------
# Funções
#-------------------------------------------------
def country_maps(df1):
    ## medianas de latitude e longitude
    df_aux = df1.loc[:, ['City','Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude']].groupby(['City', 'Road_traffic_density']).median().reset_index()
           
    # Remover NAs
    df_aux= df_aux.loc[df_aux['City'] != 'NaN', :]
    df_aux= df_aux.loc[df_aux['Road_traffic_density'] != 'NaN', :]
            
    map = folium.Map()
        
    for index, location_info in df_aux.iterrows():
        folium.Marker([location_info['Delivery_location_latitude'],
        location_info['Delivery_location_longitude']],
        popup = location_info[['City','Road_traffic_density']]).add_to(map) # Marca um ponto
            
    folium_static(map, width=1024, height=600)
    return None


def order_share_by_city(df1):
    # Quantidade de pedidos por semana / Número único de entregadores por semana 
    df_aux01 = df1.loc[:, ['ID', 'week_of_year']].groupby(['week_of_year']).count().reset_index()
    df_aux02 = df1.loc[:, ['Delivery_person_ID', 'week_of_year']].groupby(['week_of_year']).nunique().reset_index()
    # Juntar dois data frames. Função merge()
    df_aux = pd.merge(df_aux01, df_aux02, how = 'inner')
    df_aux['order_by_deliver'] = df_aux['ID'] / df_aux['Delivery_person_ID']
    # Grafico de linhas
    fig = px.line(df_aux, x = 'week_of_year', y = 'order_by_deliver')
    return fig


def order_by_week(df1):
# Criar a coluna semana
    df1['week_of_year'] = df1['Order_Date'].dt.strftime('%U')
    df1.head()
    df_aux = df1.loc[:, ['ID','week_of_year']].groupby(['week_of_year']).count().reset_index()
    # Grafico de linhas
    fig = px.line(df_aux, x = 'week_of_year', y = 'ID')
    return fig


def traffic_order_city( df1 ):
    df_aux = df1.loc[:, ['ID','City','Road_traffic_density']].groupby(['City','Road_traffic_density']).count().reset_index()
    df_aux= df_aux.loc[df_aux['City'] != 'NaN', :]
    df_aux= df_aux.loc[df_aux['Road_traffic_density'] != 'NaN', :]
    # Grafico de bolhas
    fig = px.scatter(df_aux, x = 'City', y = 'Road_traffic_density', size = 'ID', color = 'City')
    return fig


def traffic_order_share(df1):
                df_aux = df1.loc[:, ['ID','Road_traffic_density']].groupby(['Road_traffic_density']).count().reset_index()
                df_aux['entregas_perc'] = df_aux['ID']/df_aux['ID'].sum()
                # Grafico de pizza
                fig = px.pie(df_aux, values = 'entregas_perc', names = 'Road_traffic_density')
                return fig
            

def order_metric(df1):
    df_aux = df1.loc[:,['ID', 'Order_Date']].groupby(['Order_Date']).count().reset_index()
    fig = px.bar(df_aux, x = 'Order_Date', y = 'ID')
    return fig


def clean_code(df1):
    """ Esta função tem a responsabilidade de limpar o dataframe
    Tipos de limpeza: 
    1. Remoção dos dados NaN
    2. Mudança do tipo da coluna de dados 
    3. Remoção dos espaços das variáveis de texto
    4. Formatação da coluna de datas
    5. Limpeza da coluna de tempo (remoção do texto da variável numérica)

    Input: Dataframe
    Output: Dataframe """
    
    linhas_removidas = df1['Delivery_person_Age'] != 'NaN '
    df1 = df1.loc[linhas_removidas, :].copy()
    
    linhas_removidas = df1['Weatherconditions'] != 'NaN '
    df1 = df1.loc[linhas_removidas, :].copy()
    
    linhas_removidas = df1['Road_traffic_density'] != 'NaN '
    df1 = df1.loc[linhas_removidas, :].copy()
    
    linhas_removidas = df1['Type_of_order'] != 'NaN '
    df1 = df1.loc[linhas_removidas, :].copy()
    
    linhas_removidas = df1['Type_of_vehicle'] != 'NaN '
    df1 = df1.loc[linhas_removidas, :].copy()
    
    linhas_removidas = df1['Festival'] != 'NaN '
    df1 = df1.loc[linhas_removidas, :].copy()
    
    linhas_removidas = df1['City'] != 'NaN '
    df1 = df1.loc[linhas_removidas, :].copy()
    
    
    #2 Convertendo a coluna Delivery_person_Age de object para inteiro:
    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype( int )
    
    #3 Convertendo a coluna Delivery_person_Ratings de object para float:
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype( float )
    
    #4 Convertendo a coluna Order_Date de object para data:
    df1['Order_Date'] = pd.to_datetime( df1['Order_Date'], format='%d-%m-%Y')
    
    #5 Removendo linhas vazias e convertendo a coluna muliply_deliveries de object para int:
    linhas_removidas = df1['multiple_deliveries'] != 'NaN '
    df1 = df1.loc[linhas_removidas, :].copy()
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype( int )
    
    #6 Resetando index e emovendo espaços vazios das strings
    #df1 = df1.reset_index( drop=True )
    #for i in range ( len(df1) ):
    #  df1.loc[i, 'ID'] = df1.loc[i, 'ID'].strip()
    #  df1.loc[i, 'Delivery_person_ID'] = df1.loc[i, 'Delivery_person_ID'].strip()
    
    # Retirando os numeros da coluna Time_taken(min)
    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply(lambda x: x.split('(min) ')[1])
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype( int)
    
    
    
    df1 = df1.reset_index( drop=True ) #drop=True: Este parâmetro é opcional. Quando definido como True, ele descarta o índice anterior e não o inclui como uma nova coluna no DataFrame.
    
    df1.loc[:, 'ID'] = df1.loc[:, 'ID'].str.strip()
    df1.loc[:, 'Delivery_person_ID'] = df1.loc[:, 'Delivery_person_ID'].str.strip()
    df1.loc[:, 'Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
    df1.loc[:, 'Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip()
    df1.loc[:, 'Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip()
    df1.loc[:, 'City'] = df1.loc[:, 'City'].str.strip()
    df1.loc[:, 'Festival'] = df1.loc[:, 'Festival'].str.strip()
    
    #Adicionando a coluna de Semanas no DF
    df1['week_of_year'] = df1['Order_Date'].dt.strftime( "%U" )
    
    return df1





#------------------------ Inicio da Estrtura Lógica do Código --------------

#-------------------------
# Import dataset
#-------------------------
df = pd.read_csv('train.csv')

#-------------------------
# Limpando os dados
#-------------------------
df1 = clean_code( df )


#==========================================
# Barra Lateral
#==========================================

st.header('Marketplace - Visão Cliente')

# Colocar uma imagem de logo
#image_path = r'C:\Users\user\Documents\repos\Analise de dados\ftc\Ciclo_6\Teste\logo.png'
image_path = 'logo.png'
image = Image.open(image_path)
st.sidebar.image(image, width = 120)


st.sidebar.markdown('# Curry Company') # sidebar= barra lateral
st.sidebar.markdown('## Fastest delivery in Town ')
st.sidebar.markdown("""---""") # Para criar uma linha de separação

st.sidebar.markdown('## Selecione uma data limite')

## Para verificar a data minima: st.dataframe(df1) #Ordenar coluna Order_date e ver a menor data
date_slider = st.sidebar.slider(
    'Até qual valor?',
    value= datetime(2022, 4, 13),
    min_value= datetime(2022, 2, 11),
    max_value= datetime(2022, 4, 6), 
    format = "DD-MM-YYYY"
)
## Obs: Tive que importar a biblioteca datetime, no pandas diz que a função datetime não existe
st.sidebar.markdown("""---""")


traffic_options = st.sidebar.multiselect(
    'Quais as condições de trânsito?',
    ['Low', 'Medium', 'High','Jam'],
    default = ['Low', 'Medium', 'High','Jam'])

st.sidebar.markdown("""---""")
st.sidebar.markdown('### Powered by Comunidade DS')


# Filtro de Data
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas,:]


# Filtro de Trânsito
linhas_selecionadas = df1['Road_traffic_density'] .isin( traffic_options )
df1 = df1.loc[linhas_selecionadas,:]



#==========================================
# Layout no Streamlit 
#==========================================
# essas abas ficarao guardadas em variaveis diferentes: tab1, tab2 e tab3
tab1, tab2, tab3 = st.tabs(['Visão Gerencial', 'Visão Tática', 'Visão Geográfica']) # Para criar abas
    
with tab1:
    with st.container():
        fig = order_metric(df1)
        st.markdown('# Order by Day')
        st.plotly_chart(fig, use_container_width = True) #use_container_width = True: p o graf. caber dentro do espaço
      
    with st.container():  
        col1, col2 = st.columns(2) # Para dividir o container em colunas
       
        with col1:
            fig = traffic_order_share(df1)
            st.header('Traffic Order Share')
            st.plotly_chart(fig, use_container_width = True)

            
        with col2:
            fig = traffic_order_city(df1)
            st.header('Traffic Order City')
            st.plotly_chart(fig, use_container_width = True)

            
with tab2:   
    with st.container():
        fig = order_by_week(df1)
        st.markdown('# Order by Week')
        st.plotly_chart(fig, use_container_width = True)

        
    with st.container():
        fig = order_share_by_city(df1)
        st.markdown('# Order Share by City')
        st.plotly_chart(fig, use_container_width=True)
        
        
        
    
with tab3:
    st.markdown('# Country maps')
    country_maps(df1)








