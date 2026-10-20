#!/bin/bash
# shellcheck disable=SC2016
gcloud compute instances create graphql \
    --zone=us-east1-b \
    --machine-type=e2-micro \
    --image-family=debian-13 \
    --image-project=debian-cloud \
    --boot-disk-size=20GB \
    --boot-disk-type=pd-standard \
    --network-interface=network=default,subnet=default \
    --tags=http-server,https-server \
    --metadata=startup-script='#!/bin/bash
set -euo pipefail

if [ ! -f /swapfile ]; then
    fallocate -l 1G /swapfile || dd if=/dev/zero of=/swapfile bs=1M count=1024
    chmod 600 /swapfile
    mkswap /swapfile
    swapon /swapfile
    echo "/swapfile swap swap defaults 0 0" >> /etc/fstab
fi

# Update and install prerequisite packages
apt-get update
apt-get install -y ca-certificates curl gnupg

# Add Docker official GPG key and repository
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
chmod a+r /etc/apt/keyrings/docker.asc

echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian bookworm stable" \
  > /etc/apt/sources.list.d/docker.list

# Install Docker CE and Compose plugin
apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Enable and start Docker service
systemctl enable --now docker

if [ ! -d /root/pokeapi ]; then
    git clone https://github.com/PokeAPI/pokeapi.git /root/pokeapi
fi

touch /tmp/done
'
