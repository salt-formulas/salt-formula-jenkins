{% from "jenkins/map.jinja" import client with context %}

include:
  - jenkins.client

{%- for job_name, job in client.get('job', {}).iteritems() %}
  {%- include "jenkins/client/_job.sls" %}
{%- endfor %}

{%- if client.get('purge_jobs', False) %}

  {%- set jobs =  client.get('job', {}).keys() %}

  {%- for job_template_name, job_template in client.get('job_template', {}).iteritems() %}
    {%- if job_template.get('enabled', true) %}
      {%- for param_name, params in job_template.param.iteritems() %}
        {%- set replacer = "{{" + param_name + "}}" %}
        {%- for param in params %}
          {%- set job_name = job_template.name|replace(replacer, param) %}
          {%- do jobs.append(job_name) %}
        {%- endfor %}
      {%- endfor %}

      {%- for job_params in job_template.get('jobs', []) %}
        {%- set job_name = job.template.name %}
        {%- for key, value in job_params.iteritems() %}
          {%- set replacer = "{{" + key + "}}" %}
          {%- set job_name = job_name|replace(replacer, value) %}
          {%- do jobs.append(job_name) %}
        {%- endfor %}
      {%- endfor %}
    {%- endif %}
  {%- endfor %}

jenkins_clean_undefined_jobs:
  jenkins_job.cleanup:
  - jobs: {{ jobs|yaml }}

{%- endif %}
