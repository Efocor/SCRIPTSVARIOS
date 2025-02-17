# || SCRIPT 02: DL de WEBS || (AUTOMATIZACION)
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# ...función para crear una carpeta en el escritorio...
def crear_carpeta_en_escritorio(nombre_carpeta):
    # ...sacamos folder de desktop...
    escritorio = os.path.join(os.path.expanduser("~"), "Desktop")
    ruta_carpeta = os.path.join(escritorio, nombre_carpeta)
    
    # ...la creamos la carpeta si no existe...
    if not os.path.exists(ruta_carpeta):
        os.makedirs(ruta_carpeta)
    
    return ruta_carpeta

# ...función para descargar un archivo desde una URL...
def descargar_archivo(url, carpeta_destino):
    try:
        # ...obtener el nombre del archivo desde la URL...
        nombre_archivo = os.path.join(carpeta_destino, urlparse(url).path.split('/')[-1])
        
        # ...hacemos GET al servidor...
        respuesta = requests.get(url)
        
        # ... vemos si la solicitud fue exitosa (código 200)...
        if respuesta.status_code == 200:
            # ...colcamos el contenido en un archivo local...
            with open(nombre_archivo, 'wb') as archivo:
                archivo.write(respuesta.content)
            print(f"Archivo descargado: {nombre_archivo}")
        else:
            print(f"No se pudo descargar el archivo desde {url}. Código de estado: {respuesta.status_code}")
    
    except Exception as e:
        print(f"Error al descargar {url}: {e}")

# ...función para descargar una página web y sus recursos (o sea contenidos públicos)...
def descargar_pagina_web(url, carpeta_destino):
    try:
        # ...solicitud GET para obtener el contenido HTML...
        respuesta = requests.get(url)
        
        if respuesta.status_code != 200:
            print(f"No se pudo acceder a la página {url}. Código de estado: {respuesta.status_code}")
            return
        
        # ...analizamos el contenido HTML con beautifulsoup...
        soup = BeautifulSoup(respuesta.content, 'html.parser')
        
        # ...guardamos el archivo HTML en la carpeta de destino...
        nombre_html = os.path.join(carpeta_destino, "index.html")
        with open(nombre_html, 'w', encoding='utf-8') as archivo_html:
            archivo_html.write(str(soup))
        print(f"Página HTML guardada en: {nombre_html}")
        
        # ...descargamos esos los recursos asociados (imágenes, CSS, JS)...
        for tag in soup.find_all(['img', 'link', 'script']):
            if tag.name == 'img' and tag.get('src'):
                recurso_url = urljoin(url, tag.get('src'))
                descargar_archivo(recurso_url, carpeta_destino)
            elif tag.name == 'link' and tag.get('href') and tag.get('rel') == ['stylesheet']:
                recurso_url = urljoin(url, tag.get('href'))
                descargar_archivo(recurso_url, carpeta_destino)
            elif tag.name == 'script' and tag.get('src'):
                recurso_url = urljoin(url, tag.get('src'))
                descargar_archivo(recurso_url, carpeta_destino)
    
    except Exception as e:
        print(f"Error al procesar la página {url}: {e}")

# Función principal
def main():
    # ...pedimos al usuario el zelda de la página web...
    url = input("Introduce la URL de la página web que deseas descargar: ")
    
    # ...creamos la carpetita en el escritorio con el nombre de la página...
    nombre_carpeta = urlparse(url).netloc.replace('.', '_')  # ...usamos el dominio como nombre de carpeta
    carpeta_destino = crear_carpeta_en_escritorio(nombre_carpeta)
    
    # ...descargamos la página web y sus recursos...
    descargar_pagina_web(url, carpeta_destino)
    
    print(f"La página web y sus recursos han sido descargados en: {carpeta_destino}")

if __name__ == "__main__":
    main()
