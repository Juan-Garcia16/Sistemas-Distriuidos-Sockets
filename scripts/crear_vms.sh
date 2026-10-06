#!/usr/bin/env bash
# Crea las dos VMs del laboratorio con Multipass y monta ./src en ambas.
# Uso (desde la raiz del repo):  bash scripts/crear_vms.sh
# Requisito: brew install --cask multipass
set -e

REPO="$(cd "$(dirname "$0")/.." && pwd)"

for VM in vm-servidor vm-cliente; do
  if multipass info "$VM" >/dev/null 2>&1; then
    echo ">> $VM ya existe, la arranco"
    multipass start "$VM"
  else
    echo ">> creando $VM (Ubuntu 24.04, 1 CPU, 1 GB RAM, 5 GB disco)"
    multipass launch 24.04 --name "$VM" --cpus 1 --memory 1G --disk 5G
  fi
  # Monta la carpeta src del Mac dentro de la VM (se edita en el Mac, se ejecuta en la VM)
  multipass mount "$REPO/src" "$VM:/home/ubuntu/lab" 2>/dev/null || true
  # Herramientas de diagnostico usadas en la guia (nc, ss ya viene)
  multipass exec "$VM" -- sudo apt-get install -y -qq netcat-openbsd >/dev/null 2>&1 || true
  multipass exec "$VM" -- sudo hostnamectl set-hostname "$VM"
done

echo
multipass list
echo
echo "Listo. Abre dos terminales:"
echo "  multipass shell vm-servidor   ->  cd lab && python3 servidor_eco.py"
echo "  multipass shell vm-cliente    ->  cd lab && python3 cliente_eco.py <IP_vm-servidor> 5000"
