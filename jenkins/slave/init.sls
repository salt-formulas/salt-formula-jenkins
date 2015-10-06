{% from "jenkins/map.jinja" import slave with context %}

{%- if slave.enabled %}

include:
- java
{%- if slave.pbuilder is defined %}
- jenkins.slave.pbuilder
{%- endif %}
{%- if slave.gpg is defined %}
- jenkins.slave.gpg
{%- endif %}
{%- if slave.keystone is defined %}
- jenkins.slave.keystone
{%- endif %}

{% if slave.pkgs %}

jenkins_slave_package:
  pkg.installed:
  - names: {{ slave.pkgs }}
  - require:
    - pkg: java_packages

{% else %}

# No jenkins-slave package, use magic init script instead
{{ slave.init_script }}:
  file.managed:
    - source: salt://jenkins/files/init.d/jenkins-slave
    - user: root
    - group: root
    - mode: 755
    - template: jinja

{% endif %}

{{ slave.config }}:
  file.managed:
  - source: salt://jenkins/files/jenkins-slave
  - user: root
  - group: root
  - template: jinja
  - require:
    {% if slave.pkgs %}
    - pkg: jenkins_slave_package
    {% else %}
    - file: {{ slave.init_script }}
    {% endif %}

jenkins_slave_service:
  service.running:
  - name: {{ slave.service }}
  - watch:
    - file: {{ slave.config }}
  - require:
    {% if slave.pkgs %}
    - pkg: jenkins_slave_package
    {% else %}
    - file: {{ slave.init_script }}
    {% endif %}

{%- if pillar.linux.system.user.jenkins is not defined %}

jenkins_slave_user:
  user.present:
  - name: jenkins
  - shell: /bin/bash
  - home: /var/lib/jenkins
  - require_in:
    {%- if slave.gpg is defined %}
    - file: jenkins_gpg_key_dir
    {%- endif %}
    {%- if slave.pbuilder is defined %}
    - file: /var/lib/jenkins/pbuilder
    {%- endif %}

{%- endif %}

{%- if slave.get('sudo', false) %}

/etc/sudoers.d/99-jenkins-user:
  file.managed:
  - source: salt://jenkins/files/sudoer
  - template: jinja
  - user: root
  - group: root
  - mode: 440
  - require:
    - service: jenkins_slave_service

{%- endif %}

{%- endif %}
