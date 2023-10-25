import socket
import json
import sys
from kafka import KafkaProducer, KafkaConsumer

def cargar_tokens():
    try:
        with open('tokens.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {'Drones': {}}
    
def obtener_token(id):
    tokens = cargar_tokens()
    return tokens['Drones'].get(id)

def guardar_tokens(tokens):
    with open('tokens.json', 'w') as file:
        json.dump(tokens, file, indent=4)

def guardar_token(id, token):
    tokens = cargar_tokens()
    tokens["Drones"].append({"ID": id, "token": token})
    guardar_tokens(tokens)

# Función para registrar el dron en el AD_Registry
def registrar_dron(id, alias, registry_host, registry_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((registry_host, registry_port))

    mensaje = json.dumps({'id': id, 'alias': alias}).encode()
    client_socket.sendall(mensaje)

    respuesta = client_socket.recv(1024).decode()
    client_socket.close()

    respuesta = json.loads(respuesta)

    if 'token' in respuesta:
        token = respuesta['token']
        guardar_token(id, token)

    return respuesta

# Función para unirse al espectáculo en el AD_Engine
def obtener_coordenadas(id, token, engine_host, engine_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((engine_host, engine_port))

    mensaje = json.dumps({'id': id, 'token': token}).encode()
    client_socket.sendall(mensaje)

    respuesta = client_socket.recv(1024).decode()
    client_socket.close()

    return json.loads(respuesta)

def calcular_mejor_movimiento(pos_actual, pos_objetivo):
    x_actual, y_actual = pos_actual
    x_objetivo, y_objetivo = pos_objetivo

    # Calcular la diferencia en coordenadas
    dx = x_objetivo - x_actual
    dy = y_objetivo - y_actual

    # Elegir el siguiente movimiento en base a la diferencia
    if dx > 0 and dy == 0:
        return (x_actual + 1, y_actual)
    elif dx > 0 and dy < 0:
        return (x_actual + 1, y_actual - 1)
    elif dx == 0 and dy < 0:
        return (x_actual, y_actual - 1)
    else:
        return pos_actual  # No hay necesidad de moverse

def mover_dron(id, pos_actual, pos_objetivo):
    return calcular_mejor_movimiento(pos_actual, pos_objetivo)

def menu(host, port):
    print("Menú de opciones:")
    print("1. Registrar Dron (AD_Registry)")
    print("2. Unirse al espectáculo (AD_Engine)")
    opcion = input("Ingrese el número de la opción que desea ejecutar: ")

    if opcion == '1':
        id = input("Ingrese el ID del dron: ")
        alias = input("Ingrese el alias del dron: ")
        respuesta = registrar_dron(id, alias, host, port)
        print(respuesta)
    elif opcion == '2':
        id = input("Ingrese el ID del dron: ")
        token = obtener_token(id)

        if token:
            coordenadas = obtener_coordenadas(id, token, host, port)
            if 'coordenadas' in coordenadas:
                print(f"Coordenadas recibidas: {coordenadas['coordenadas']}")
                nueva_posicion=(0,0)
                # Simular movimiento del dron
                nueva_posicion = mover_dron(id, nueva_posicion, coordenadas['coordenadas'])
                print(f"Nueva posición del dron: {nueva_posicion}")
            else:
                print("Error al obtener coordenadas del AD_Engine")
        else:
            print(f"No se encontró un token para el ID {id}")
    else:
        print("Opción no válida")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python AD_Drone.py <registry_host> <registry_port>")
        sys.exit(1)

    registry_host = sys.argv[1]
    registry_port = int(sys.argv[2])

    menu(registry_host, registry_port)