# Notas de laboratorio — Lab 1 Sockets TCP

Regla: escribir la **Predicción** ANTES de ejecutar. Luego la **Observación** (qué pasó,
con referencia a la captura en `evidencias/`) y la **Explicación** (por qué pasó).

Montaje: contenedores Docker en la red `labnet` 192.168.56.0/24 · vm-servidor = 192.168.56.10 · vm-cliente = 192.168.56.11 (IPs fijas en docker-compose.yml).

---

## Parte A — Conectividad entre nodos (ping, nc -vz, ss -ltnp)

**Predicción:**

**Observación:**

**Explicación:**

---

## Parte B — Eco entre VMs y cuádrupla de la conexión

**Predicción:**

**Observación:**

**Explicación:**

---

## E1 — Varios clientes a la vez

**Predicción:**

**Observación:**

**Explicación:**

---

## E2 — Socket de escucha vs. socket de conexión

**Predicción:**

**Observación:**

**Explicación:**

---

## E3 — Cierre de la conexión (FIN, sin `if not datos: break`, apagón con suspend)

**Predicción:**

**Observación:**

**Explicación:**

---

## E4 — Ráfaga: TCP es un flujo de bytes (pausa 0 vs. 0.5)

**Predicción:**

**Observación:**

**Explicación:**

---

## E5 — SO_REUSEADDR y TIME_WAIT

**Predicción:**

**Observación:**

**Explicación:**

---

## E6 — Fallos provocados (F1..F5)

**Predicción:**

**Observación:**

**Explicación:**

---

## Dificultades encontradas

1. **El equipo es un Mac, sin VirtualBox → Multipass.** La guía pide VirtualBox, pero en un Mac
   (sobre todo con Apple Silicon) no es la opción práctica. Primero se eligió Multipass (Canonical),
   que crea VMs Ubuntu reales sobre el hipervisor nativo de macOS y las une en una red privada.

2. **`multipass: command not found`.** Tras la instalación, la terminal no reconocía el comando.
   - Solución: <!-- completar: como se resolvio -->

3. **`exec failed: No route to host` al crear la VM.** Justo después de `multipass launch`, los
   comandos sobre la VM fallaban porque su red todavía no había arrancado.
   - Solución: esperar a que la VM terminara de arrancar su red; se verificó con `ping` antes de seguir.

4. **Carpeta montada vacía por permisos de macOS.** `src/` se montaba en `/home/ubuntu/lab`, pero
   dentro de la VM aparecía vacía y al leer un archivo salía `Operation not permitted`.
   Causa: el repo está en `~/Documents`, y la protección de privacidad de macOS (TCC) no dejaba
   que el demonio `multipassd` leyera esa carpeta.
   - Intento de solución: darle a `multipassd` Acceso total al disco en Ajustes > Privacidad y seguridad.

5. **`multipassd` caído tras cambiar los permisos → cambio a Docker.** Después de cambiar el
   Acceso total al disco, el servicio de Multipass dejó de funcionar y no se pudieron usar las VMs.
   - Solución: se cambió a **Docker** (`Dockerfile` + `docker-compose.yml`): dos contenedores
     Ubuntu 24.04, `vm-servidor` (192.168.56.10) y `vm-cliente` (192.168.56.11), en una red bridge
     privada `labnet` 192.168.56.0/24, con `src/` montado en `/home/ubuntu/lab`.
   - Por qué sirve para el laboratorio: un contenedor **comparte el kernel** del anfitrión (no es una
     VM completa; en Mac ese anfitrión es la VM Linux ligera que ejecuta Docker Desktop), pero tiene **su propia pila de red** gracias a los *network namespaces* de Linux:
     su propia interfaz e IP, su propia tabla de puertos y sockets (los dos nodos pueden usar el
     puerto 5000 sin chocar) y su propio árbol de procesos. El tráfico entre ellos pasa por una red
     real (bridge virtual), con saludo de tres vías, FIN, RST, TIME_WAIT, etc. Eso es exactamente lo
     que el laboratorio necesita observar: dos extremos TCP en hosts distintos de la misma LAN.
   - Equivalencias con la guía: el "apagón" de E3.4 se hace con `docker network disconnect`
     (el cliente desaparece de la red sin enviar FIN) y el cortafuegos de F5 con una regla
     `iptables ... --dport 5000 -j DROP` en vm-servidor (en lugar de ufw).
