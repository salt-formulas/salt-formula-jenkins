{% from "jenkins/map.jinja" import client with context %}
{%- if client.enabled %}

include:
  - .source
  - .job

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
    - {{ client.dir.jenkins_root }}
    - {{ client.dir.salt_root }}/_jenkins/cache
  - makedirs: true

{{ client.dir.salt_root }}/_jenkins/jobs:
  file.symlink:
    - target: {{ client.dir.jenkins_root }}

{%- endif %}
