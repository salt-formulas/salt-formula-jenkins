{% from "jenkins/map.jinja" import client with context %}

include:
  - jenkins.client

{%- for job_template_name, job_template in client.get('job_template', {}).iteritems() %}

{%- if job_template.get('enabled', true) %}

{# now just 1 defined param is supported #}

{%- if job_template.param|length == 1 %}

{%- for param_name, params in job_template.param.iteritems() %}

{%- set replacer = "{{" + param_name + "}}" %}

{%- for param in params %}

{%- set job_name = job_template.name|replace(replacer, param) %}
{%- set job = job_template.template|yaml|replace(replacer, param) %}

jenkins_job_{{ job_name }}_definition:
  file.managed:
  - name: {{ client.dir.jenkins_jobs_root }}/{{ job_name }}.xml
  - source: salt://jenkins/files/jobs/{{ job.type }}.xml
  - mode: 400
  - template: jinja
  - defaults:
      job_name: {{ job_name }}
      job: {{ job }}
  - require:
    - file: jenkins_client_dirs

jenkins_job_{{ job_name }}_present:
  jenkins_job.present:
  - name: {{ job_name }}
  - config: {{ client.dir.jenkins_jobs_root }}/{{ job_name }}.xml
  - watch:
    - file: jenkins_job_{{ job_name }}_definition
    - file: /etc/salt/minion.d/_jenkins.conf

{%- endfor %}

{%- endfor %}

{%- endif %}

{%- endfor %}
