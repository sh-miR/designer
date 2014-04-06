nginx:
  pkg:
    - installed
  service:
    - running
    - require:
      - pkg: nginx
    - watch:
      - pkg: nginx
      - file: /etc/nginx/nginx.conf

/etc/nginx/nginx.conf
  fine.managed:
    - source salt://nginx/nginx.conf
    - user: root
    - group: root
    - mode: 644
