{% from "jenkins/map.jinja" import client with context %}

include:
  - jenkins.client

{%- for job_name, job in client.get('job', {}).iteritems() %}

{{ client.dir.salt_root }}/_jenkins/cache/{{ job_name }}.xml:
  file.managed:
  - source: salt://jenkins/files/jobs/{{ job.type }}.xml
  - mode: 400
  - template: jinja
  - defaults:
      job_name: {{ job_name }}
  - require:
    - file: jenkins_client_dirs

jenkins_job_{{ job_name }}_ensure:
  jenkins.present:
  - name: {{ job_name }}
  - config: salt://_jenkins/cache/{{ job_name }}.xml
  - watch:
    - file: {{ client.dir.salt_root }}/_jenkins/cache/{{ job_name }}.xml
    - file: /etc/salt/minion.d/_jenkins.conf

{%- endfor %}
