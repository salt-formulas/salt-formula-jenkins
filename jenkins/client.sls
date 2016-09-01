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

{%- for source_name, source in client.source.iteritems() %}

{%- if source.engine == "git" %}

jenkins_{{ source_name }}_source:
  git.latest:
  - name: {{ source.address }}
  - target: {{ client.dir.jenkins_root }}/{{ source_name }}
  - rev: {{ source.branch }}
  - reload_pillar: True

{%- elif client.source.engine == "local" %}

jenkins_{{ source_name }}_dir:
  file.managed:
  - name: {{ client.dir.jenkins_root }}/{{ source_name }}
  - mode: 700

{%- endif %}

{%- endfor %}

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
  - config: salt://_jenkins/cache/{{ job_name }}.xml
  - require:
    - file: {{ client.dir.salt_root }}/_jenkins/cache/{{ job_name }}.xml

{%- endfor %}

{%- endif %}
