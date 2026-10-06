# Plan de 4 h 30 min — Laboratorio 1 (Sockets TCP)

| Bloque | Tiempo | Qué hacer | Evidencia (guardar en `evidencias/`) |
|---|---|---|---|
| 0. Preparar | 0:00–0:15 | Abrir Docker Desktop, `docker compose up -d --build` en la raíz del repo, `docker compose ps` | `A0_docker_compose_ps.png` |
| 1. Parte A | 0:15–0:35 | `docker exec -it <nodo> bash`; `ip -br addr` en ambos, `ping`, `nc -vz IP 5000` (refused), arrancar servidor, `nc -vz` (succeeded), `ss -ltnp` | `A1_ip_addr.png`, `A2_ping.png`, `A3_nc_refused.png`, `A4_nc_ok.png`, `A5_ss_ltnp.png` |
| 2. Parte B | 0:35–0:55 | Eco entre nodos (2 terminales lado a lado). Anotar cuádrupla. Correr también `profe/serverp.py` + `profe/cliente.py` | `B1_eco_lado_a_lado.png`, `B2_codigo_profe.png` |
| 3. E1–E3 | 0:55–1:40 | 3 clientes a la vez + `ss -tn state established '( sport = :5000 )'`; salida del servidor (2 sockets); cierre del cliente, quitar `if not datos: break`, apagón con `docker network disconnect sistemas-distriuidos-sockets_labnet vm-cliente` (E3.4) | `E1_*.png`, `E2_*.png`, `E3_*.png` |
| 4. E4 | 1:40–2:00 | `cliente_rafaga.py` con pausa 0 (×5) y 0.5 | `E4_pausa0.png`, `E4_pausa05.png` |
| 5. E5–E6 | 2:00–2:35 | Comentar SO_REUSEADDR + `ss -tan state time-wait`; fallos F1..F5 (F5: en vm-servidor `iptables -A INPUT -p tcp --dport 5000 -j DROP`, luego `-D` para quitarla) | `E5_*.png`, `E6_F1..F5.png` |
| 6. R1 + R2 | 2:35–3:20 | R1 ya implementado y probado (solo correrlo y capturar `cat bitacora.log`); R2: protocolo delimitado por `\n`; probar con ráfaga sin pausa | `R1_bitacora.png`, `R2_rafaga_ok.png` |
| 7. Informe | 3:20–4:15 | Tabla predicción/observación/explicación, 14 preguntas, dificultades, conclusiones, APA | `informe/informe.md` → PDF |
| 8. Ensayo | 4:15–4:30 | Banco de preguntas 7.3 en voz alta | — |

**Regla de oro de cada experimento:** antes de ejecutar, escribe tu predicción en `informe/notas.md`.
Luego ejecuta, toma captura y escribe qué pasó y por qué.

**Capturas en Mac:** `Cmd+Shift+4` y luego barra espaciadora para capturar una ventana entera.
