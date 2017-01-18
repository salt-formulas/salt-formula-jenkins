{%- from "jenkins/map.jinja" import client with context %}
{%- if client.smtp is defined %}
set_jenkins_smtp:
  jenkins_smtp.config:
    - host: {{ client.smtp.host }}
    - username: {{ client.smtp.get('username','') }}
    - password: {{ client.smtp.get('password', '') }}
    - reply_to: {{ client.smtp.get('reply_to','') }}
    - port: {{ client.smtp.get('port', '') }}
    - ssl: {{ client.smtp.get('ssl', '') }}
    - charset: {{ client.smtp.get('charset', '') }}
{%- endif %}
