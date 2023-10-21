import socket
import json

# Definir la dirección y puerto del servidor
HOST = 'localhost'
PORT = 5000

# Nombre del archivo que se utilizará como base de datos
DB_FILE = 'drones.json'

# Función para cargar la base de datos desde el archivo de texto
def cargar_base_de_datos():
    try:
        with open(DB_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        with open(DB_FILE, 'w') as file:
            json.dump({"Drones": []}, file)
            return {"Drones": []}

# Función para guardar la base de datos en el archivo de texto
def guardar_base_de_datos():
    with open(DB_FILE, 'w') as file:
        json.dump(base_de_datos, file, indent=4)

# Función para registrar un dron en la base de datos
def registrar_dron(id, alias):
    base_de_datos["Drones"].append({'ID': id, 'Alias': alias})
    guardar_base_de_datos()
    return {'token': f'TOKEN-{id}'}

# Inicializar la base de datos
base_de_datos = cargar_base_de_datos()

# Inicializar el socket del servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

print(f'AD_Registry escuchando en {HOST}:{PORT}')

while True:

    print('Esperando conexiones...')
    
    # Esperar a que un cliente se conecte
    client_socket, client_address = server_socket.accept()
    
    # Recibir el mensaje del cliente y convertirlo a diccionario
    mensaje = client_socket.recv(1024).decode()
    datos = json.loads(mensaje)

    # Comprobar si la operación es de registro y realizarla
    #if datos.get('operacion') == 'registro':
    id = datos.get('id')
    alias = datos.get('alias')
    respuesta = registrar_dron(id, alias)
    #else:
        #respuesta = {'error': 'Operación no vlida'}
    
    # Enviar la respuesta al cliente
    client_socket.send(json.dumps(respuesta).encode())

    # Cerrar la conexión con el cliente
    client_socket.close()