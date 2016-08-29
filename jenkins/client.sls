{% from "jenkins/map.jinja" import client with context %}
{%- if client.enabled %}

jenkins_client_install:
  pkg.installed:
  - names: {{ client.pkgs }}

jenkins_client_dirs:
  file.directory:
  - names:
    - /srv/jenkins
    - {{ client.dir.salt_root }}/_jenkins/cache
  - makedirs: true

/etc/salt/minion.d/_jenkins.conf:
  file.managed:
  - source: salt://jenkins/files/_jenkins.conf
  - template: jinja

{%- if client.source.engine == "git" %}

reclass_data_source:
  git.latest:
  - name: {{ client.source.address }}
  - target: {{ client.dir.jenkins_root }}
  - rev: {{ client.source.branch }}
  - reload_pillar: True

{%- elif client.source.engine == "local" %}

reclass_data_dir:
  file.managed:
  - name: {{ client.dir.jenkins_root }}
  - mode: 700

{%- endif %}

{{ client.dir.salt_root }}/_jenkins/jobs:
  file.symlink:
    - target: {{ client.dir.jenkins_root }}

{%- for job_name, job in client.job.iteritems() %}

{{ client.dir.salt_root }}/_jenkins/cache/{{ job_name }}.xml:
  file.managed:
  - source: salt://jenkins/files/jobs/{{ job.type }}.xml
  - mode: 400
  - template: jinja
  - defaults:
      job_name: {{ job_name }}
  - require:
    - file: jenkins_client_dirs
    - file: /etc/salt/minion.d/_jenkins.conf

jenkins_job_{{ job_name }}_ensure:
  jenkins.present:
  - name: {{ job_name }}
  - config: salt://_jenkins_jobs/{{ job_name }}.xml
  - require:
    - file: {{ client.dir.salt_root }}/_jenkins/cache/{{ job_name }}.xml

{%- endfor %}

{%- endif %}
