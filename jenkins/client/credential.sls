{#- It's not recommended to call this state explicitly as it requires plugins #}
{% from "jenkins/map.jinja" import client with context %}
{% for name, cred in client.get('credential',{}).items() %}
credential_{{ name }}:
  jenkins_credential.present:
  - name: {{ cred.get('name', name) }}
  - username: {{ cred.get('username', '') }}
  - password: {{ cred.get('password', '') }}
  - desc: {{ cred.get('desc', '') }}
  - scope: {{ cred.get('scope','GLOBAL') }}
  - secret: {{ cred.get('secret', '') }}
  - filename: {{ cred.get('filename', '') }}
  {%- if cred.content is defined %}
  - content: {{ cred.get('content', '')|yaml_encode }}
  {%- endif %}
  {%- if cred.key is defined %}
  - key: |
      {{ cred.get('key','')|indent(6) }}
  {%- endif %}
{% endfor %}
