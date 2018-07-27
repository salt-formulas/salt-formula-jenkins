{% from "jenkins/map.jinja" import client with context %}
{%- if client.plugin is defined %}
jenkins_plugins:
  jenkins_plugin.managed:
  - plugins: {{ client.plugin }}
  - remove_unwanted: {{ client.get('plugin_remove_unwanted', False) }}
  - force_remove: {{ client.get('plugin_force_remove', False) }}

jenkins_wait_functional:
  cmd.script:
  - source: salt://jenkins/files/wait4jenkins.sh
  - shell: /bin/bash
  - env:
    - JENKINS_URL: "{{ client.master.get('proto', 'http') }}://{{ client.master.get('host', 'localhost') }}:{{ client.master.get('port', '8080') }}/login"
    - WAIT_TIME: "300"
    - INTERVAL: "5"
  - require:
    - jenkins_plugins
{%- endif %}
