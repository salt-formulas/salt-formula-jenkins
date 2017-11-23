{% from "jenkins/map.jinja" import client with context %}
{%- if client.gerrit is defined %}
{% for name, gerrit in client.get('gerrit',{}).iteritems() %}
jenkins_gerrit_trigger_{{ name }}:
  jenkins_gerrit.present:
  - name: {{ name }}
  - hostname: {{ gerrit.get('host', '') }}
  - port: {{ gerrit.get('port', '29418') }}
  - proxy: {{ gerrit.get('proxy', '')  }}
  - username: {{ gerrit.get('username', '') }}
  - email: {{ gerrit.get('email', '') }}
  - auth_key_file: {{ gerrit.get('auth_key_file', '') }}
  - frontendurl: {{ gerrit.get('frontendURL','') }}
  {%- if gerrit.authkey is defined %}
  - authkey: |
      {{ gerrit.get('authkey','')|indent(6) }}
  {%- endif %}
  - auth_key_file_password: {{ gerrit.get('auth_key_file_password', '') }}
{% endfor %}
{%- endif %}
