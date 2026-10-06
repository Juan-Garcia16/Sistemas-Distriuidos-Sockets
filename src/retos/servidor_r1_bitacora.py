#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
servidor_r1_bitacora.py
Laboratorio de Sistemas Distribuidos - Reto R1 (obligatorio)
Maquina: VM-SERVIDOR

Servidor de eco (igual que servidor_eco.py) que ademas registra cada
conexion en el archivo bitacora.log. Por cada conexion escribe UNA linea con:
  - marca de tiempo de inicio y de fin
  - IP:puerto del cliente, obtenido con getpeername()
  - numero de mensajes y bytes recibidos (cliente -> servidor)
  - numero de mensajes y bytes enviados  (servidor -> cliente)
  - como termino la conexion

Nota: "mensaje" = una llamada a recv() que trajo datos. Como TCP no conserva
fronteras, varios envios del cliente pueden contarse como un solo mensaje
(ver experimento E4).

Ejecucion:  python3 servidor_r1_bitacora.py
Ver log  :  cat bitacora.log   (se crea en la carpeta desde donde se ejecuta)
"""

import socket
from datetime import datetime

HOST = "0.0.0.0"
PUERTO = 5000
TAM_BUFFER = 1024
ARCHIVO_LOG = "bitacora.log"


def ahora():
    # Marca de tiempo legible con milisegundos, ej: 2026-10-06 14:03:12.345
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]


def escribir_bitacora(linea):
    # Modo "a" (append): agrega al final sin borrar conexiones anteriores.
    # El "with" cierra el archivo y asegura que la linea quede en disco.
    with open(ARCHIVO_LOG, "a", encoding="utf-8") as log:
        log.write(linea + "\n")


def atender(conexion):
    # getpeername() devuelve (IP, puerto) del extremo REMOTO de la conexion.
    # Se llama al inicio porque despues de que el cliente se desconecta
    # la llamada puede fallar (socket ya no conectado).
    ip_cliente, puerto_cliente = conexion.getpeername()
    inicio = ahora()

    # Contadores de la conexion, uno por sentido.
    msgs_recibidos = 0
    bytes_recibidos = 0
    msgs_enviados = 0
    bytes_enviados = 0
    motivo_cierre = "desconocido"

    print(f"\n[r1] conexion de {ip_cliente}:{puerto_cliente} a las {inicio}")

    try:
        while True:
            datos = conexion.recv(TAM_BUFFER)
            if not datos:
                # 0 bytes: el cliente cerro ordenadamente (envio FIN).
                motivo_cierre = "cliente cerro (FIN)"
                break

            msgs_recibidos += 1
            bytes_recibidos += len(datos)
            print(f"[r1] recibidos {len(datos)} bytes: {datos!r}")

            respuesta = datos.upper()
            conexion.sendall(respuesta)
            msgs_enviados += 1
            bytes_enviados += len(respuesta)
            print(f"[r1] enviados  {len(respuesta)} bytes: {respuesta!r}")

    except ConnectionResetError:
        # El cliente aborto la conexion (RST) en vez de cerrarla con FIN.
        motivo_cierre = "conexion reiniciada (RST)"
    except OSError as e:
        motivo_cierre = f"error de red: {e}"
    finally:
        # El finally se ejecuta SIEMPRE: aunque haya error, la conexion
        # queda registrada en la bitacora.
        conexion.close()
        fin = ahora()
        linea = (f"inicio={inicio} | fin={fin} | "
                 f"cliente={ip_cliente}:{puerto_cliente} | "
                 f"recibidos={msgs_recibidos} msgs/{bytes_recibidos} B | "
                 f"enviados={msgs_enviados} msgs/{bytes_enviados} B | "
                 f"cierre={motivo_cierre}")
        escribir_bitacora(linea)
        print(f"[r1] bitacora: {linea}")


def main():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind((HOST, PUERTO))
    servidor.listen(1)
    print(f"[r1] escuchando en {servidor.getsockname()}, "
          f"registrando en {ARCHIVO_LOG} (Ctrl+C para terminar)")

    try:
        while True:
            # Se ignora la direccion que devuelve accept(): la obtenemos
            # con getpeername() dentro de atender(), como pide el reto.
            conexion, _ = servidor.accept()
            atender(conexion)
    except KeyboardInterrupt:
        print("\n[r1] interrumpido por el usuario")
    finally:
        servidor.close()
        print("[r1] socket de escucha cerrado")


if __name__ == "__main__":
    main()
