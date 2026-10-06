# CLAUDE.md — Laboratorio 1 · Sistemas Distribuidos (UTP 2026-2)

## Contexto para Claude Code
Proyecto universitario: **comunicación entre procesos mediante sockets TCP** en Python 3,
entre **dos máquinas virtuales Ubuntu**. El estudiante debe **sustentarlo oralmente**, así que:

- Explica cada cambio de código en español, línea por línea cuando sea nuevo.
- Comentarios del código en español, sin tildes (evita problemas de codificación).
- No uses librerías externas: solo la biblioteca estándar (`socket`, `sys`, `time`, `threading`, `datetime`).
- No "mejores" los códigos base de `src/` (servidor_eco.py, cliente_eco.py, cliente_rafaga.py):
  son los de la guía y los experimentos dependen de su comportamiento exacto.
  Los retos van en archivos nuevos.
- Cuando el estudiante pregunte por un experimento, primero pídele su **predicción** (la guía la exige).

## Entorno (decisión tomada)
La guía pide VirtualBox, pero el equipo es un Mac. Se usa **Multipass** (Canonical): crea VMs
reales de Ubuntu Server en minutos, sobre el hipervisor nativo de macOS, y las conecta en la
misma red privada (equivalente al adaptador solo-anfitrión de VirtualBox).

| Máquina      | Rol                  | IP                                   |
|--------------|----------------------|--------------------------------------|
| vm-servidor  | ejecuta servidores   | la que muestre `multipass list` (192.168.64.x) |
| vm-cliente   | ejecuta clientes     | la que muestre `multipass list` (192.168.64.x) |
| Puerto       | aplicación           | 5000/TCP (código de la guía) · 12345/TCP (código del profe) |

La carpeta `src/` del Mac está montada en ambas VMs en `/home/ubuntu/lab`.
Se edita en el Mac y se ejecuta dentro de las VMs.

Comandos útiles (desde el Mac):
- `multipass list` — estado e IPs
- `multipass shell vm-servidor` / `multipass shell vm-cliente`
- `multipass suspend vm-cliente` — simula "apagón" sin FIN (experimento E3.4)
- `multipass stop vm-servidor vm-cliente` — al terminar

ADVERTENCIA ufw (E6/F5): antes de `sudo ufw enable` ejecutar `sudo ufw allow 22/tcp`,
o se pierde el acceso por `multipass shell` (usa SSH).

## Estructura del repo
```
CLAUDE.md
PLAN.md                 plan por tiempos + checklist de evidencias
scripts/crear_vms.sh    crea y monta las dos VMs
src/
  servidor_eco.py       Anexo 1 de la guía (vm-servidor)
  cliente_eco.py        Anexo 1 de la guía (vm-cliente)
  cliente_rafaga.py     Anexo 1 de la guía, experimento E4 (vm-cliente)
  profe/serverp.py      código entregado por el profe (host corregido a 0.0.0.0)
  profe/cliente.py      código entregado por el profe (IP del servidor por argumento)
  retos/                R1..R5 (por crear)
evidencias/             capturas por parte/experimento (A, B, E1..E6, R1, R2)
informe/                borrador del informe (Markdown -> PDF, máx. 15 páginas)
```

## Tareas pendientes (en orden)
1. [ ] Parte A: VMs creadas, ping entre ellas, `nc -vz` (refused / succeeded), `ss -ltnp`.
2. [ ] Parte B: eco funcionando entre VMs; registrar la cuádrupla. Correr también el código del profe.
3. [ ] Parte C: E1..E6 con tabla predicción / observación / explicación.
4. [ ] R1 (obligatorio) `src/retos/servidor_r1_bitacora.py`: escribe `bitacora.log` por conexión
       con marca de tiempo, IP:puerto del cliente (`getpeername()`), n.º de mensajes y bytes en cada sentido.
5. [ ] R2 (obligatorio) `src/retos/servidor_r2_delimitado.py` + `src/retos/cliente_r2.py` + `src/retos/cliente_rafaga_r2.py`:
       mensajes delimitados por `\n`. Búfer FUERA del bucle de recv(), `while b"\n" in buffer`
       (no `if`), conservar el resto parcial. Debe funcionar con la ráfaga sin pausa.
6. [ ] (Opcional, +nota) R3 comandos HORA/ECO/ESTADISTICAS/ADIOS, R4 hilos (+ Lock para el contador
       compartido), R5 RTT con 100 msgs de 10 B y 100 de 8000 B (min/max/media).
7. [ ] Informe: portada · objetivos · montaje (diagrama de red) · experimentos · 14 preguntas ·
       dificultades encontradas (se califica; incluir el cambio VirtualBox -> Multipass) ·
       conclusiones · referencias APA 7.
8. [ ] Ensayo de sustentación con el banco de preguntas de la sección 7.3 de la guía.

## Entregable final
`SD_Lab1_Apellido_Nombre.zip` = informe PDF + todos los `.py` comentados (incluidos R1 y R2).
