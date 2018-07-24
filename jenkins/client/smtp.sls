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
    - require:
      - sls: jenkins.client.plugin
{%- endif %}

{%- if client.smtp is defined and client.smtp.admin_email is defined %}
set_jenkins_admin_email:
  jenkins_smtp.admin_email:
    - email: {{ client.smtp.admin_email }}
{%- endif %}
