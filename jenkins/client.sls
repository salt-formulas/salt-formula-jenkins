{% from "jenkins/map.jinja" import client with context %}
{%- if client.enabled %}

jenkins_client_install:
  pkg.installed:
  - names: {{ client.pkgs }}

jenkins_client_dirs:
  file.directory:
  - name: /srv/salt/env/dev/_jenkins_jobs
  - makedirs: true

/etc/salt/minion.d/_jenkins.conf:
  file.managed:
  - source: salt://jenkins/files/_jenkins.conf
  - template: jinja

{%- for job_name, job in client.job.iteritems() %}

/srv/salt/env/dev/_jenkins_jobs/{{ job_name }}.xml:
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
    - file: /srv/salt/env/dev/_jenkins_jobs/{{ job_name }}.xml

{%- endfor %}

{%- endif %}
