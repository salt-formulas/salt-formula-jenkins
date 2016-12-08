{% from "jenkins/map.jinja" import client with context %}
{%- if client.enabled %}

include:
  - jenkins.client.source
  - jenkins.client.job
  - jenkins.client.credential
  - jenkins.client.user
  
jenkins_client_install:
  pkg.installed:
  - names: {{ client.pkgs }}

/etc/salt/minion.d/_jenkins.conf:
  file.managed:
  - source: salt://jenkins/files/_jenkins.conf
  - template: jinja

jenkins_client_dirs:
  file.directory:
  - names:
    - {{ client.dir.jenkins_source_root }}
    - {{ client.dir.jenkins_jobs_root }}
  - makedirs: true

{%- endif %}
