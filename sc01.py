# || SCRIPT EN PYTHON || (AUTOMATIZACION)
import os
import requests

# ...función para descargar un archivo desde una URL...
def descargar_archivo(url, carpeta_destino):
    try:
        # ...obtener el nombre del archivo desde la URL...
        nombre_archivo = os.path.join(carpeta_destino, url.split('/')[-1])
        
        # ...realizar la solicitud GET al servidor...
        respuesta = requests.get(url)
        
        # ...verificar si la solicitud fue exitosa (código 200)...
        if respuesta.status_code == 200:
            # ...escribir el contenido en un archivo local...
            with open(nombre_archivo, 'wb') as archivo:
                archivo.write(respuesta.content)
            print(f"Archivo descargado: {nombre_archivo}")
        else:
            print(f"No se pudo descargar el archivo desde {url}. Código de estado: {respuesta.status_code}")
    
    except Exception as e:
        print(f"Error al descargar {url}: {e}")

# ...funcion principal... (aquí deben ir los links)
def main():
    # Lista de URLs de los archivos a descargar
    urls = [
        "https://example.com/archivo1.jpg",
        "https://example.com/archivo2.pdf",
        "https://example.com/archivo3.zip"
    ]
    
    # ...carpeta donde se guardarán los archivos descargados...
    carpeta_destino = "archivos_descargados"
    
    # ...crear la carpeta de destino si no existe...
    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)
    
    # ...iterar sobre cada URL...
    for url in urls:
        descargar_archivo(url, carpeta_destino)

if __name__ == "__main__":
    main()
