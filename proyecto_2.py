import requests
from tabulate import tabulate
import mysql.connector

URL ='https://restcountries.com/v3.1/region/America'

response = requests.get(URL)

if response.status_code == 200:
    print('Te has conectado a la Api exitosamente')
    data = response.json()
    rows = []

    for contry in data:
        nombre = contry['name']['common']

        # extrar capital con validacion
        capital = (
            contry['capital'][0]
            if 'capital' in contry and len(contry['capital']) > 0
            else 'No definida'
        )

        region = contry.get('region', 'No definida')
        poblacion = contry.get('population', 0)
        
        # guardar lista
        rows.append([nombre, capital, region, poblacion])
     #mostrar tabla
    headers = ['Nombre', 'Capital', 'Region', 'Poblacion']
    print(tabulate(rows, headers, tablefmt='grid'))

    #conexcion a la base de datos
    connection = mysql.connector.connect(
        host = '127.0.0.1',        
        user = 'root',
        password = 'root',
        database = 'db_g6'
    )

    if connection.is_connected(): # evita ejecutar sql si hay fallas
        cursor = connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS pais(
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(255),
                capital VARCHAR(255),
                region VARCHAR(255),
                poblacion BIGINT
            );
            """
        )
        
        for pais in rows:
            cursor.execute(
                """
                INSERT INTO pais(nombre, capital, region, poblacion)
                VALUES (%s, %s, %s, %s)
                """,
                pais
            )

        connection.commit()
        connection.close()

        print('Registro correcto de los paises importados')

    else:
        print('Error al conectar con la base de datos')

else:
    print(f'Error en la API : {response.status_code}')

