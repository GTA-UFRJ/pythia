#!bin/bash
DESTINATION=172.20.0.2:8080
su -
#echo 1 >/proc/sys/net/ipv4/ip_forward
sysctl -w net.ipv4.ip_forward=1
iptables -t nat -A PREROUTING -p tcp --dport 80 -j DNAT --to-destination $DESTINATION
iptables -t nat -A POSTROUTING -p tcp -d $DESTINATION --dport 80 -j MASQUERADE

echo "olar"