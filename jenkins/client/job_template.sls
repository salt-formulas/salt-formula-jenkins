{% from "jenkins/map.jinja" import client with context %}

{%- if salt['pillar.get']('job_template_name', False) %}

{%- set job_template_name = salt['pillar.get']('job_template_name') %}
{%- set job_template = salt['pillar.get']('jenkins:client:job_template:'+job_template_name) %}
{% include "jenkins/client/_job_template.sls" %}

{%- elif salt['pillar.get']('job_template_names', False) is iterable %}

{%- for job_template_name in salt['pillar.get']('job_template_names') %}
{%- set job_template = salt['pillar.get']('jenkins:client:job_template:'+job_template_name) %}
{% include "jenkins/client/_job_template.sls" %}
{%- endfor %}

{%- else %}

{%- for job_template_name, job_template in client.get('job_template', {}).iteritems() %}
{% include "jenkins/client/_job_template.sls" %}
{%- endfor %}

{%- endif %}
