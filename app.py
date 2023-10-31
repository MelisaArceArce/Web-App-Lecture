import pandas as pd
import plotly.express as px
import streamlit as st


# Lectura de datos
car_data = pd.read_csv('vehicles_us.csv') # leer los datos

# Limpieza de datos

# Modificar valores nulos
car_data['model_year'] = car_data['model_year'].astype('Int64')
car_data['model_year'] = car_data['model_year'].fillna(0) # 0 es desconocido
car_data['cylinders'] = car_data['cylinders'].fillna(0) # 0 es desconocido
car_data['cylinders'] = car_data['cylinders'].astype('Int64')
car_data['odometer'] = car_data['odometer'].fillna(0) # 0 es desconocido
car_data['odometer'] = car_data['odometer'].astype('Int64')
car_data['paint_color'] = car_data['paint_color'].fillna('unknown') # -1 es desconocido
car_data['is_4wd'] = car_data['is_4wd'].astype('str')
car_data['is_4wd'] = car_data['is_4wd'].replace(['1.0','nan'],['yes','no'])
car_data['date_posted']= pd.to_datetime(car_data['date_posted'])

# Año 
car_year = car_data[car_data['model_year'] != 0]
car_year['year_condition'] = car_year['model_year'].astype('str') +'_' +car_year['condition'].astype('str')
car_year_condition = car_year.groupby(['year_condition'],  as_index=False)['model'].count()

# odometer 
car_odometer = car_data[car_data['odometer'] != 0]

# Tiempo
top = car_data.sort_values('days_listed')
top = top.groupby('model', as_index=False)['days_listed'].sum().sort_values('days_listed')
top_price = car_data.sort_values('days_listed')
top_price = top_price.groupby('model', as_index=False)['price'].mean().sort_values('price')

# Funciones

def Header():
    st.header('Graficación de "vehicles"')
    st.write('Bienvenido querido usuario  ♡.')
    st.write('Puede elegir entre los diferentes graficos para visualizar la información de una empresa que vende/renta autos usados, da click en alguna opción del menú lateral.')


def price():
    st.subheader('Graficas respecto a precios')
    st.write("Haga click en algún botón.")

    # Botones 
    build_odo_price = st.button('Distribución kilometraje x precio')
    build_year_price = st.button('Grafica año x precio', key='a1')

    
    if  build_year_price:

        # Crear grafica
        fig = px.scatter(car_year, x="model_year", y="price", title='Año de los modelos x Precio')
        st.plotly_chart(fig, use_container_width=True)
    if build_odo_price:

       # crear un grafica
       fig = px.scatter(car_data, x="odometer", y="price", title='Kilometraje x precio')
       st.plotly_chart(fig, use_container_width=True) 


def description():
    st.subheader('Decripción de los autos en venta/renta')
    st.write("Haga click en algún botón.")

    # Botones
    build_histogram_year = st.button('Histograma año modelos')
    build_bar_year = st.button('Grafica de barras año y estado')
    hist_button = st.button('Histograma Kilometraje')
    

    if build_histogram_year:

        # Crear un Histograma
        fig = px.histogram(car_year, x="model_year", title='Histograma año')
        st.plotly_chart(fig, use_container_width=True)
    if  build_bar_year:

        # Crear diagrama de barras
        fig = px.bar(car_year_condition, x="model", y="year_condition", title='Modelos_año x Estado')
        st.plotly_chart(fig, use_container_width=True)
    if hist_button: # al hacer clic en el botón
        # crear un histograma
        fig = px.histogram(car_odometer, x="odometer", title='Histograma Kilometraje')
        st.plotly_chart(fig, use_container_width=True) 


def top_vehicle():
    st.subheader('Tops')
    st.write("Haga click en algún botón.")

    # Botones
    build_top = st.button('Top modelo x días publicado', key='b1')
    build_top_price = st.button('Top modelo x precio', key='c1')

    if build_top:
        fig = px.bar(top[:10], x="days_listed", y="model", title='Top modelos con menos dias publicados')
        st.plotly_chart(fig, use_container_width=True) 
    if build_top_price:
        fig = px.bar(top_price[:10], x="price", y="model", title='Top modelos más baratos')
        st.plotly_chart(fig, use_container_width=True) 


# Correr funciones
def execute():
    Header()
    if cb2: price()
    if cb3: description()
    if cb4: top_vehicle()

# sidebar configurations
cb1 = st.sidebar.checkbox('Todos', key='a')
cb2 = st.sidebar.checkbox('Precios', key='b', value=cb1)
cb3 = st.sidebar.checkbox('Descipción', key='c', value=cb1)
cb4 = st.sidebar.checkbox('Top', key='d', value=cb1)

execute()