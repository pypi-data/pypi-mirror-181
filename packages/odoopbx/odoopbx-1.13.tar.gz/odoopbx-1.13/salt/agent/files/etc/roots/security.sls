{% if salt['config.get']('security_reactor_enabled') %}

security-get-firewall.sh:
  file.managed:
    - name: /etc/salt/firewall.sh
    - source: salt://firewall.sh
    - template: jinja
    - mode: '0755'
    - context:
        security_banned_timeout: {{ salt['config.get']('security_banned_timeout', '86400') }}
        security_expire_short_timeout: {{ salt['config.get']('security_expire_short_timeout', '30') }}
        security_expire_long_timeout: {{ salt['config.get']('security_expire_long_timeout', '86400') }}
        security_ports_tcp: {{ salt['config.get']('security_ports_tcp', '5038,5039,5060,5061,8088,8089,65060') }}
        security_ports_udp: {{ salt['config.get']('security_ports_udp', '5060,65060') }}

security-run-firewall.sh:
  cmd.run:
    - name: /etc/salt/firewall.sh

{% endif %}
