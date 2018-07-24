{%- if job.enabled|default(True) %}

jenkins_job_{{ job_name }}_definition:
  file.managed:
  - name: {{ client.dir.jenkins_jobs_root }}/{{ job_name }}.xml
  - source: salt://jenkins/files/jobs/{{ job.type }}.xml
  - mode: 400
  - template: jinja
  - defaults:
      job_name: {{ job_name }}
      {%- if job is defined %}
      job: {{ job|yaml }}
      {%- endif %}
  - require:
    - file: jenkins_client_dirs

jenkins_job_{{ job_name }}_present:
  jenkins_job.present:
  - name: {{ job_name }}
  - config: {{ client.dir.jenkins_jobs_root }}/{{ job_name }}.xml
  - watch:
    - file: jenkins_job_{{ job_name }}_definition
  - require:
    - sls: jenkins.client.approval
    - sls: jenkins.client.artifactory
    - sls: jenkins.client.credential
    - sls: jenkins.client.gerrit
    - sls: jenkins.client.globalenvprop
    - sls: jenkins.client.jira
    - sls: jenkins.client.lib
    - sls: jenkins.client.node
    - sls: jenkins.client.plugin
    - sls: jenkins.client.security
    - sls: jenkins.client.slack
    - sls: jenkins.client.smtp
    - sls: jenkins.client.throttle_category

{%- else %}

jenkins_job_{{ job_name }}_definition:
  file.absent:
  - name: {{ client.dir.jenkins_jobs_root }}/{{ job_name }}.xml
  - require:
    - file: jenkins_client_dirs

jenkins_job_{{ job_name }}_absent:
  jenkins_job.absent:
  - name: {{ job_name }}

{%- endif %}
