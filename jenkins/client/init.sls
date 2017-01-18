{% from "jenkins/map.jinja" import client with context %}
{%- if client.enabled %}

include:
{%- if client.plugin is defined %}
  - jenkins.client.plugin
{%- endif %}
{%- if client.security is defined %}
  - jenkins.client.security
{%- endif %}
{%- if client.source is defined %}
  - jenkins.client.source
{%- endif %}
{%- if client.job is defined %}
  - jenkins.client.job
{%- endif %}
{%- if client.credential is defined %}
  - jenkins.client.credential
{%- endif %}
{%- if client.user is defined %}
  - jenkins.client.user
{%- endif %}
{%- if client.node is defined %}
  - jenkins.client.node
{%- endif %}
{%- if client.view is defined %}
  - jenkins.client.view
{%- endif %}
{%- if client.smtp is defined %}
  - jenkins.client.smtp
{%- endif %}

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
