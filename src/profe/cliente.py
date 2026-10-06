import socket
import sys

# Codigo entregado por el profesor.
# UNICO CAMBIO: la IP del servidor se pasa por argumento
# (antes estaba fija en '172.16.0.64', la IP del equipo del profe).
# Uso: python3 cliente.py <IP_vm-servidor>

# Configuración de red
host = sys.argv[1] if len(sys.argv) > 1 else '127.0.0.1'  # IP del servidor
port = 12345  # Puerto arbitrario

# Crear un socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar el socket al servidor remoto
sock.connect((host, port))

while True:
    # Enviar datos al servidor
    message = input("Ingrese un mensaje para el servidor: ")
    sock.sendall(message.encode('utf-8'))

    # Recibir respuesta del servidor
    data = sock.recv(1024)
    print(f"Respuesta del servidor: {data.decode('utf-8')}")

    # Preguntar al usuario si desea enviar otro mensaje
    continuar = input("¿Desea enviar otro mensaje? (s/n): ")
    if continuar.lower() != 's':
        break

# Cerrar la conexión
sock.close()
