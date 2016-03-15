{%- from "jenkins/map.jinja" import master with context %}
{%- if master.enabled %}

include:
- java

jenkins_packages:
  pkg.installed:
  - names: {{ master.pkgs }}
  - require:
    - pkg: java_packages

jenkins_{{ master.config }}:
  file.managed:
  - name: {{ master.config }}
  - source: salt://jenkins/files/jenkins
  - user: root
  - group: root
  - template: jinja
  - require:
    - pkg: jenkins_packages

/var/lib/jenkins/config.xml:
  file.managed:
  {%- if master.get('no_config', False) == False %}
  - source: salt://jenkins/files/config.xml
  - template: jinja
  {%- endif %}
  - user: jenkins
  - group: nogroup
  - require:
    - pkg: jenkins_packages

{%- if master.get('sudo', false) %}

/etc/sudoers.d/99-jenkins-user:
  file.managed:
  - source: salt://jenkins/files/sudoer
  - template: jinja
  - user: root
  - group: root
  - mode: 440
  - require:
    - service: jenkins_master_service

{%- endif %}

jenkins_master_service:
  service.running:
  - name: {{ master.service }}
  - watch:
    - file: jenkins_{{ master.config }}
    - file: /var/lib/jenkins/config.xml

{%- endif %}
