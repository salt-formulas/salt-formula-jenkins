{% from "jenkins/map.jinja" import client with context %}
{% for name, cred in client.get('credential',{}).iteritems() %}
credential_{{ name }}:
  jenkins_credential.present:
  - name: {{ cred.get('name', name) }}
  - username: {{ cred.get('username', '') }}
  - password: {{ cred.get('password', '') }}
  - desc: {{ cred.get('desc', '') }}
  - scope: {{ cred.get('scope','GLOBAL') }}
  - secret: {{ cred.get('secret', '') }}
  {%- if cred.key is defined %}
  - key: |
      {{ cred.get('key','')|indent(6) }}
  {%- endif %}
  - require:
    - sls: jenkins.client.plugin
{% endfor %}
