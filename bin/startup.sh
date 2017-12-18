#!/usr/bin/env bash

OVPN_PATH=$1

# Start VPN. /var/secrets/vpn/credentials should be username\npassword\n

#printf '%s\n' $VPN_USERNAME $VPN_PASSWORD > /etc/openvpn/credentials
#sed -i 's/auth-user-pass/auth-user-pass \/etc\/openvpn\/credentials/g' $OVPN_PATH
openvpn --config $OVPN_PATH &


# Start HPC manager
# python -m hpc_manager.main

gunicorn --reload hpc_manager.main:application
