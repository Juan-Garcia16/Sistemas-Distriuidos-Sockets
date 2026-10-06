# CLAUDE.md — Laboratorio 1 · Sistemas Distribuidos (UTP 2026-2)

## Contexto para Claude Code
Proyecto universitario: **comunicación entre procesos mediante sockets TCP** en Python 3,
entre **dos nodos Ubuntu** (contenedores Docker en lugar de VMs, ver Entorno). El estudiante debe **sustentarlo oralmente**, así que:

- Explica cada cambio de código en español, línea por línea cuando sea nuevo.
- Comentarios del código en español, sin tildes (evita problemas de codificación).
- No uses librerías externas: solo la biblioteca estándar (`socket`, `sys`, `time`, `threading`, `datetime`).
- No "mejores" los códigos base de `src/` (servidor_eco.py, cliente_eco.py, cliente_rafaga.py):
  son los de la guía y los experimentos dependen de su comportamiento exacto.
  Los retos van en archivos nuevos.
- Cuando el estudiante pregunte por un experimento, primero pídele su **predicción** (la guía la exige).

## Entorno (decisión tomada)
La guía pide VirtualBox, pero el equipo es un Mac. Primero se intentó Multipass y falló
(el servicio `multipassd` quedó caído tras cambiar permisos de Acceso total al disco).
Se usa **Docker**: `Dockerfile` (Ubuntu 24.04 + python3, iproute2, ping, netcat, iptables)
y `docker-compose.yml` con dos nodos en una red bridge privada `labnet`
(equivalente al adaptador solo-anfitrión de VirtualBox).

Cada contenedor comparte el kernel del Mac/Docker, pero tiene **su propia pila de red**
(network namespace): su IP, su tabla de puertos, sus sockets y sus procesos. Para el
laboratorio se comporta como dos máquinas distintas en la misma LAN.

| Nodo         | Rol                  | IP                                   |
|--------------|----------------------|--------------------------------------|
| vm-servidor  | ejecuta servidores   | **192.168.56.10** (fija en docker-compose.yml) |
| vm-cliente   | ejecuta clientes     | **192.168.56.11** (fija en docker-compose.yml) |
| Red          | `labnet` (bridge)    | 192.168.56.0/24                      |
| Puerto       | aplicación           | 5000/TCP (código de la guía) · 12345/TCP (código del profe) |

**No se usó netplan**: las IPs se fijan con `ipv4_address` en `docker-compose.yml`.
No se publican puertos al Mac (`ports:`): el tráfico va solo entre los dos nodos por `labnet`.

La carpeta `src/` del Mac está montada en ambos nodos en `/home/ubuntu/lab` (volumen).
Se edita en el Mac y se ejecuta dentro de los contenedores.

Comandos útiles (desde el Mac, en la raíz del repo):
- `docker compose up -d --build` — construir y arrancar los dos nodos
- `docker compose ps` — estado · `docker exec vm-servidor ip -br addr` — IP
- `docker exec -it vm-servidor bash` / `docker exec -it vm-cliente bash` — entrar a un nodo
- E3.4 "apagón" sin FIN: `docker network disconnect <red> vm-cliente`
  (la red se llama `sistemas-distriuidos-sockets_labnet`; ver `docker network ls`).
  Reconectar: `docker network connect --ip 192.168.56.11 <red> vm-cliente`.
  NO usar `docker stop`: mata el proceso y el kernel sí envía FIN/RST.
- E6/F5 cortafuegos (dentro de vm-servidor; requiere `cap_add: NET_ADMIN`, ya puesto):
  `iptables -A INPUT -p tcp --dport 5000 -j DROP` · quitar: `iptables -D INPUT -p tcp --dport 5000 -j DROP`.
  `docker exec` no usa la red, así que no se pierde el acceso al nodo (no aplica la advertencia de ufw/SSH).
- `docker compose down` — al terminar

## Estructura del repo
```
CLAUDE.md
PLAN.md                 plan por tiempos + checklist de evidencias
Dockerfile              imagen de los nodos (Ubuntu 24.04 + herramientas de red)
docker-compose.yml      nodos vm-servidor / vm-cliente en la red labnet
scripts/crear_vms.sh    (obsoleto: era para Multipass)
src/
  servidor_eco.py       Anexo 1 de la guía (vm-servidor)
  cliente_eco.py        Anexo 1 de la guía (vm-cliente)
  cliente_rafaga.py     Anexo 1 de la guía, experimento E4 (vm-cliente)
  profe/serverp.py      código entregado por el profe (host corregido a 0.0.0.0)
  profe/cliente.py      código entregado por el profe (IP del servidor por argumento)
  retos/                R1 (hecho) · R2..R5 (por crear)
evidencias/             capturas por parte/experimento (A, B, E1..E6, R1, R2)
informe/                notas.md (predicción/observación/explicación) y borrador del informe
```

## Tareas pendientes (en orden)
1. [ ] Parte A: nodos creados, ping entre ellos, `nc -vz` (refused / succeeded), `ss -ltnp`.
2. [ ] Parte B: eco funcionando entre nodos; registrar la cuádrupla. Correr también el código del profe.
3. [ ] Parte C: E1..E6 con tabla predicción / observación / explicación.
4. [x] R1 (obligatorio) `src/retos/servidor_r1_bitacora.py`: escribe `bitacora.log` por conexión
       con marca de tiempo, IP:puerto del cliente (`getpeername()`), n.º de mensajes y bytes en cada sentido.
5. [ ] R2 (obligatorio) `src/retos/servidor_r2_delimitado.py` + `src/retos/cliente_r2.py` + `src/retos/cliente_rafaga_r2.py`:
       mensajes delimitados por `\n`. Búfer FUERA del bucle de recv(), `while b"\n" in buffer`
       (no `if`), conservar el resto parcial. Debe funcionar con la ráfaga sin pausa.
6. [ ] (Opcional, +nota) R3 comandos HORA/ECO/ESTADISTICAS/ADIOS, R4 hilos (+ Lock para el contador
       compartido), R5 RTT con 100 msgs de 10 B y 100 de 8000 B (min/max/media).
7. [ ] Informe: portada · objetivos · montaje (diagrama de red) · experimentos · 14 preguntas ·
       dificultades encontradas (se califica; incluir VirtualBox -> Multipass -> Docker) ·
       conclusiones · referencias APA 7.
8. [ ] Ensayo de sustentación con el banco de preguntas de la sección 7.3 de la guía.

## Entregable final
`SD_Lab1_Apellido_Nombre.zip` = informe PDF + todos los `.py` comentados (incluidos R1 y R2).
