{%- from "jenkins/map.jinja" import client with context %}
{%- if client.theme is defined %}
set_jenkins_theme:
  jenkins_theme.config:
    - css_url: {{ client.theme.css_url }}
    - js_url: {{ client.theme.js_url }}
{%- endif %}
