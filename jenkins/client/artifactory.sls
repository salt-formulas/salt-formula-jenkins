{% from "jenkins/map.jinja" import client with context %}
{% for name, artifactory in client.get('artifactory',{}).iteritems() %}
{% if artifactory.get('enabled', True) %}
jenkins_artifactory_server_{{ name }}:
  jenkins_artifactory.present:
  - name: {{ artifactory.get('name', name) }}
  - url: {{ artifactory.get('url', '') }}
  - credential_id: {{ artifactory.get('credential_id', '') }}
  - require:
    - sls: jenkins.client.plugin
    - jenkins_credential: {{ artifactory.get('credential_id', '') }}
{% else %}
jenkins_artifactory_server_{{ name }}_disable:
   jenkins_artifactory.absent:
   - name: {{ artifactory.get('name', name) }}
{% endif %}
{% endfor %}
