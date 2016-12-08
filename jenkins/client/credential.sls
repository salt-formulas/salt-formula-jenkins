{% from "jenkins/map.jinja" import client with context %}
{% for name, cred in client.get('credential',{}).iteritems() %}
credential_{{ name }}:
  jenkins_credentials.present:
  - name: {{ cred.get('name', name) }}
  - username: {{ cred.username }}
  - password: {{ cred.get('password', '') }}
  - desc: {{ cred.get('desc', '') }}
  - scope: {{ cred.get('scope','GLOBAL') }}
  {%- if cred.key is defined %}
  - key: {{ cred.get('key','') }}
  {%- endif %}
{% endfor %}