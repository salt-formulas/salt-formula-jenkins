{% from "jenkins/map.jinja" import client with context %}

include:
  - jenkins.client

{%- for job_name, job in client.get('job', {}).iteritems() %}

{%- if job.enabled|default(True) %}

jenkins_job_{{ job_name }}_definition:
  file.managed:
  - name: {{ client.dir.jenkins_jobs_root }}/{{ job_name }}.xml
  - source: salt://jenkins/files/jobs/{{ job.type }}.xml
  - mode: 400
  - template: jinja
  - defaults:
      job_name: {{ job_name }}
  - require:
    - file: jenkins_client_dirs

jenkins_job_{{ job_name }}_present:
  jenkins_job.present:
  - name: {{ job_name }}
  - config: {{ client.dir.jenkins_jobs_root }}/{{ job_name }}.xml
  - watch:
    - file: jenkins_job_{{ job_name }}_definition
    - file: /etc/salt/minion.d/_jenkins.conf

{%- else %}

jenkins_job_{{ job_name }}_definition:
  file.absent:
  - name: {{ client.dir.jenkins_jobs_root }}/{{ job_name }}.xml
  - require:
    - file: jenkins_client_dirs

jenkins_job_{{ job_name }}_absent:
  jenkins_job.absent:
  - name: {{ job_name }}
  - watch:
    - file: /etc/salt/minion.d/_jenkins.conf

{%- endif %}

{%- endfor %}

{%- if client.get('purge_jobs', False) %}

{%- set jobs =  client.get('job', {}).keys() %}

{%- for job_template_name, job_template in client.get('job_template', {}).iteritems() %}

{%- if job_template.get('enabled', true) %}

{%- for param_name, params in job_template.param.iteritems() %}

{%- set replacer = "{{" + param_name + "}}" %}

{%- for param in params %}

{%- set job_name = job_template.name|replace(replacer, param) %}

{%- endfor %}

{%- endfor %}

{%- endif %}

jenkins_clean_undefined_jobs:
  jenkins_job.cleanup:
  - jobs: {{ jobs|yaml }}

{%- endif %}