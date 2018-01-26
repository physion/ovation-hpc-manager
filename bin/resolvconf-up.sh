#!/usr/bin/env bash
echo "nameserver 10.20.30.98" > /etc/resolv.conf
echo "nameserver 10.20.30.2" >> /etc/resolv.conf
echo "nameserver 10.20.30.3" >> /etc/resolv.conf
echo "nameserver 8.8.8.8" >> /etc/resolv.conf
echo "search alphacruncher.net" >> /etc/resolv.conf