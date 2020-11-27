{#- It's not recommended to call this state explicitly as it should be called
 in the end of Jenkins instance configuration #}
{% from "jenkins/map.jinja" import client with context %}

{%- for job_name, job in client.get('job', {}).items() %}
  {%- include "jenkins/client/_job.sls" %}
{%- endfor %}

{%- if client.get('purge_jobs', False) %}

  {%- set jobs =  client.get('job', {}).keys() %}

  {%- for job_template_name, job_template in client.get('job_template', {}).items() %}
    {%- if job_template.get('enabled', true) %}
      {%- for param_name, params in job_template.get('param', {}).items() %}
        {%- set replacer = client.replacer.open + param_name + client.replacer.close %}
        {%- for param in params %}
          {%- set job_name = job_template.name|replace(replacer, param) %}
          {%- do jobs.append(job_name) %}
        {%- endfor %}
      {%- endfor %}

      {%- for job_params in job_template.get('jobs', []) %}
        {%- set job_name = job_template.name %}
        {%- for key, value in job_params.items() %}
          {%- set replacer = client.replacer.open + key + client.replacer.close %}
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
