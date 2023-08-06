#!/bin/sh

# OdooPBX firewall implementation.
# It is safe to re-run this script multiple times.

# Create ipsets
ipset create -exist whitelist hash:net family inet hashsize 1024 maxelem 65536 counters comment
ipset create -exist blacklist hash:net family inet hashsize 1024 maxelem 65536 counters comment
ipset create -exist authenticated hash:ip family inet hashsize 1024 maxelem 65536 counters comment
ipset create -exist banned hash:ip family inet hashsize 1024 maxelem 65536 counters comment timeout {{ security_banned_timeout }}
ipset create -exist expire_short hash:ip family inet hashsize 1024 maxelem 65536 counters comment timeout {{ security_expire_short_timeout }}
ipset create -exist expire_long hash:ip family inet hashsize 1024 maxelem 65536 counters comment timeout {{ security_expire_long_timeout }}

# Clean existing rules
iptables -D INPUT -p tcp -m multiport --dports {{ security_ports_tcp }} -m comment --comment "www,manager,sip,http" -j voip 2> /dev/null
iptables -D INPUT -p udp -m multiport --dports {{ security_ports_udp }} -m comment --comment "iax,sip" -j voip 2> /dev/null
iptables -F voip 2>/dev/null || iptables -N voip
# Fill iptables with working rules
iptables -I INPUT -p tcp -m multiport --dports {{ security_ports_tcp }} -m comment --comment "www,manager,sip,http" -j voip
iptables -I INPUT -p udp -m multiport --dports {{ security_ports_udp }} -m comment --comment "iax,sip" -j voip
iptables -A voip -m set --match-set whitelist src -j ACCEPT
iptables -A voip -m set --match-set blacklist src -j DROP
iptables -A voip -m set --match-set authenticated src -j ACCEPT
iptables -A voip -m set --match-set banned src -j DROP
iptables -A voip -m set --match-set expire_short src -j ACCEPT
iptables -A voip -m set --match-set expire_long src -j DROP
iptables -A voip -m string --string "VaxSIPUserAgent" --algo bm --to 65535 -j DROP
iptables -A voip -m string --string "friendly-scanner" --algo bm --to 65535 -j DROP
iptables -A voip -m string --string "sipvicious" --algo bm --to 65535 -j DROP
iptables -A voip -m string --string "sipcli" --algo bm --to 65535 -j DROP
