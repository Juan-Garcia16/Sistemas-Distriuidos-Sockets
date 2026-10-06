# Imagen de las "VMs" del laboratorio: Ubuntu 24.04 + Python 3 + herramientas de red
FROM ubuntu:24.04
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 iproute2 iputils-ping netcat-openbsd iptables procps nano \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /home/ubuntu/lab
CMD ["sleep", "infinity"]