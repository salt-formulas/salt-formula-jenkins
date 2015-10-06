{% from "jenkins/map.jinja" import master with context %}

/var/lib/jenkins/updates:
  file.directory:
  - user: jenkins
  - group: nogroup

setup_jenkins_cli:
  cmd.run:
  - names:
    - sleep 30
    - wget http://localhost:{{ master.http.port }}/jnlpJars/jenkins-cli.jar
  - unless: "[ -f /root/jenkins-cli.jar ]"
  - cwd: /root
  - require:
    - service: jenkins_master_service

{%- for plugin in master.plugins %}

install_jenkins_plugin_{{ plugin.name }}:
  cmd.run:
  - name: java -jar jenkins-cli.jar -s http://localhost:{{ master.http.port }} install-plugin --username admin --password {{ master.user.admin.password }} {{ plugin.name }}
  - unless: "[ -d /var/lib/jenkins/plugins/{{ plugin.name }} ]"
  - cwd: /root
  - require:
    - cmd: setup_jenkins_cli

{%- endfor %}
