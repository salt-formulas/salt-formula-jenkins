{%- from "jenkins/map.jinja" import master with context %}
{%- if master.enabled %}
include:
- jenkins.master.service
- jenkins.master.user
{%- if master.plugins is defined %}
- jenkins.master.plugin
{%- endif %}
{%- endif %}
