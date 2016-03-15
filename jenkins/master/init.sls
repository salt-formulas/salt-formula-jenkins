{%- from "jenkins/map.jinja" import master with context %}
{%- if master.enabled %}
include:
- jenkins.master.service
- jenkins.master.users
{%- if master.plugins is defined %}
- jenkins.master.plugins
{%- endif %}
{%- endif %}
