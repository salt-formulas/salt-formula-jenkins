{#- It's not recommended to call this state explicitly as it requires plugins and credentials #}
{% from "jenkins/map.jinja" import client with context %}
{% for name, artifactory in client.get('artifactory',{}).items() %}
{% if artifactory.get('enabled', True) %}
jenkins_artifactory_server_{{ name }}:
  jenkins_artifactory.present:
  - name: {{ artifactory.get('name', name) }}
  - url: {{ artifactory.get('url', '') }}
  - credential_id: {{ artifactory.get('credential_id', '') }}
{% else %}
jenkins_artifactory_server_{{ name }}_disable:
   jenkins_artifactory.absent:
   - name: {{ artifactory.get('name', name) }}
{% endif %}
{% endfor %}