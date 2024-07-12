import requests
from geopy.distance import geodesic

def obtener_coordenadas(ciudad):
    try:
        url = f"https://nominatim.openstreetmap.org/search?city={ciudad}&format=json"
        headers = {'User-Agent': 'Tu-Usuario'}  # Añade un encabezado de usuario si es requerido por la API

        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Lanza una excepción si hay un error en la solicitud HTTP

        data = response.json()
        if data:
            latitud = data[0]['lat']
            longitud = data[0]['lon']
            return (float(latitud), float(longitud))
        else:
            print(f"No se encontraron coordenadas para {ciudad}.")
            return None
    except requests.exceptions.HTTPError as http_err:
        print(f"Error HTTP al obtener coordenadas para {ciudad}: {http_err}")
        return None
    except requests.exceptions.RequestException as req_err:
        print(f"Error al realizar la solicitud HTTP para {ciudad}: {req_err}")
        return None
    except (KeyError, IndexError):
        print(f"Respuesta JSON no válida para {ciudad}.")
        return None



def calcular_distancia(coordenadas_origen, coordenadas_destino):
    return geodesic(coordenadas_origen, coordenadas_destino).kilometers

def main():
    while True:
        print("\nBienvenido al calculador de distancia y duración de viaje.")
        print("Ingrese 's' para salir en cualquier momento.")

        ciudad_origen = input("Ingrese la Ciudad de Origen (ej: Santiago, Chile): ")
        if ciudad_origen.lower() == 's':
            break
        
        ciudad_destino = input("Ingrese la Ciudad de Destino (ej: Mendoza, Argentina): ")
        if ciudad_destino.lower() == 's':
            break
        
        coordenadas_origen = obtener_coordenadas(ciudad_origen)
        coordenadas_destino = obtener_coordenadas(ciudad_destino)
        
        if coordenadas_origen and coordenadas_destino:
            distancia_km = calcular_distancia(coordenadas_origen, coordenadas_destino)
            distancia_millas = distancia_km * 0.621371
            print(f"\nLa distancia entre {ciudad_origen} y {ciudad_destino} es de {distancia_km:.2f} km o {distancia_millas:.2f} millas.")
            
            print("\nSeleccione el medio de transporte:")
            print("1. Coche (80 km/h)")
            print("2. Bicicleta (20 km/h)")
            print("3. Avión (900 km/h)")
            
            opcion = input("Ingrese el número de la opción deseada: ")
            if opcion.lower() == 's':
                break
            
            if opcion == '1':
                velocidad = 80
                medio = "coche"
            elif opcion == '2':
                velocidad = 20
                medio = "bicicleta"
            elif opcion == '3':
                velocidad = 900
                medio = "avión"
            else:
                print("Opción no válida.")
                continue
            
            duracion_horas = distancia_km / velocidad
            duracion_minutos = duracion_horas * 60
            print(f"\nLa duración del viaje en {medio} es de aproximadamente {duracion_horas:.2f} horas o {duracion_minutos:.0f} minutos.")
            
            print(f"\nNarrativa del viaje: Saldrás desde {ciudad_origen} y viajarás en {medio} durante {duracion_horas:.2f} horas para llegar a {ciudad_destino}, cubriendo una distancia de {distancia_km:.2f} km.")
        else:
            print("No se pudo calcular la distancia. Verifique los nombres de las ciudades e intente nuevamente.")

if __name__ == "__main__":
    main()
