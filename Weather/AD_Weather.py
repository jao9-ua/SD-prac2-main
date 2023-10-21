import socket 
import threading
import sys
import json 


PUERTO = 12345
SERVER = "127.0.0.1"
FORMAT = 'utf-8'
#SERVER = socket.gethostbyname(socket.gethostname()) 
CONFIG = {}
MAX_CONEXIONES = 3 # DUDA: Cuántas conexiones cómo máximo se pueden poner a la vez?
MAX_CARACTERES_CIUDAD = 256

STX = chr(2)
ETX = chr(3)

def handle_client(conn, addr):
    print(f"[NUEVA CONEXION] {addr} connected.")

    peticionLeida = ""
    while not (ETX in peticionLeida):
        peticionLeida += conn.recv(MAX_CARACTERES_CIUDAD).decode(FORMAT) # Esperando a recibir el nombre de la ciudad
    
    if peticionLeida[0] == STX:
        peticionLeida = peticionLeida[1:-1]

    else:
        raise Exception("El mensaje no comienza con STX: {}".format(peticionLeida))

    print("[PETICIÓN CLIENTE] Saber la temperatura".format(peticionLeida))

    with open("temperatura.json", 'r') as nom:
        temp = json.load(nom)

        # TODO: qué pasa si no exite la ciudad en el fichero
        #esEcontrada = False
        msg = STX + str(temp["temperatura"]) + ETX
        conn.send(msg.encode(FORMAT))

        # for ciudad in ciudades:
        #     if temperatura["nombre"] == peticionLeida:
        #         esEcontrada = True
        #         msg = STX + str(temperatura["temperatura"]) + ETX
        #         conn.send(msg.encode(FORMAT))
        
        # if esEcontrada == False:
        #     msg = STX + "No hay registros de temperatura de esa ciudad" + ETX
        #     conn.send(msg.encode(FORMAT))


    conn.close()
        



def start(server):
    server.listen()
    print(
        "[LISTENING] Servidor escuchando en el servidor {} y en el puerto {}..."
        .format(SERVER, PUERTO)
        )
    CONEX_ACTIVAS = threading.active_count() - 1 # Cuenta el número de hilos que están activos
    print("CONEXIONES ACTIVAS: {}".format(CONEX_ACTIVAS))

    try:
        while True:
            conn, addr = server.accept() # accept: Se queda esperando a un cliente, cuando le llega uno, te devuelve una tupla ['conn': socket del cliente, 'addr': dirección del cliente]
            CONEX_ACTIVAS = threading.active_count()
            if (CONEX_ACTIVAS <= MAX_CONEXIONES): 
                thread = threading.Thread(target=handle_client, args=(conn, addr)) # Crea un hilo para la nueva conexión
                thread.start() # Se ejecuta el hilo
                print(f"[CONEXIONES ACTIVAS] {CONEX_ACTIVAS}")
                print("CONEXIONES RESTANTES PARA CERRAR EL SERVICIO", MAX_CONEXIONES-CONEX_ACTIVAS)
            else:
                print("DEMASIADAS CONEXIONES. ESPERANDO A QUE ALGUIEN SE VAYA")
                conn.send("DEMASIADAS CONEXIONES. Tendrás que esperar a que alguien se vaya".encode(FORMAT))
                conn.close()
                CONEX_ACTUALES = threading.active_count() - 1
    
    except KeyboardInterrupt:
        print("\nAdiós ;)")
    

def main(args): 
    nombre_archivo = ""
    if len(sys.argv) < 2:
        print("No se ha pasado ningún fichero de configuración")
        print("Usando fichero por defecto weatherCasa.json")

        nombre_archivo = "weatherCasa.json"
    else:
        nombre_archivo = sys.argv[1]

    try:
        with open(nombre_archivo, 'r') as file:
            CONFIG = json.load(file)
        SERVER = CONFIG["direccionIP"]
        PUERTO = CONFIG["puerto"]
        #print(SERVER, PUERTO)
        
        #                     (familia dir. IP, tipo de Socket[TCP])
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((SERVER, PUERTO)) # 'bind': Le dice al server cuando va a tener que escuchar y en qué puerto por lo que se crea una tupla donde se guarda el servidor y el puerto

        print("[STARTING] Servidor inicializándose...")

        start(server)

    except FileNotFoundError:
            print("El fichero proporcinado no existe")

    
    


#Coger los args pasado por la línea de comando y pasárselos al main
if __name__ == "__main__":
    main(sys.argv) 
    
