#!/usr/bin/env bash

OVPN_PATH=$1

INTERNAL_PORT=$2

# Start VPN. /var/secrets/vpn/credentials should be username\npassword\n

mkdir -p /dev/net
mknod /dev/net/tun c 10 200
chmod 600 /dev/net/tun

#printf '%s\n' $VPN_USERNAME $VPN_PASSWORD > /etc/openvpn/credentials
#sed -i 's/auth-user-pass/auth-user-pass \/etc\/openvpn\/credentials/g' $OVPN_PATH
openvpn --client --script-security 2 --config $OVPN_PATH --daemon

# /app/bin/resolvconf-up.sh


# Start HPC manager
# python -m hpc_manager.main

gunicorn -b 0.0.0.0:$INTERNAL_PORT hpc_manager.main:application