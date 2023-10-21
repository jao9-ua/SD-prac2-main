import socket
import sys

HEADER = 64
PUERTO = 5050
FORMAT = 'utf-8'
STX = chr(2)
ETX = chr(3)
ACK = chr(6)


def send(msg, client):
    message = STX + msg + ETX
    client.send(message.encode(FORMAT))

def weather(server, puerto):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server, puerto))

    print("Conexión establecida con el servidor {} y el puerto {}".format(server, puerto))

    peticion = ""
    peticion = input("¿Desea saber la temperatura? ")
    send(peticion, client)

    respuesta = ""
    while not (ETX in respuesta):
        respuesta += client.recv(2048).decode(FORMAT)
    
    if respuesta[0] == STX:
        respuesta = respuesta[1:-1]

    else:
        raise Exception("El mensaje no comienza con STX: {}".format(respuesta))

    print("Recibo del Servidor [Temperatura]: ", respuesta)

    client.close()

def main(args):
    if(len(sys.argv) != 3):
        
        print("No se han pasado los argumentos correctos")
        print("Se necesitan los siguientes argumentos: <Server_IP_Weather> <Puerto_AD_Weather>")
    else:
        SERVER_W = str(sys.argv[1])
        PUERTO_W = int(sys.argv[2])

        weather(SERVER_W, PUERTO_W)


if __name__ == "__main__":
    main(sys.argv) 