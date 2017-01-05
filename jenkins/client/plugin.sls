{% from "jenkins/map.jinja" import client with context %}
{% for name, plug in client.get('plugin',{}).iteritems() %}
{% if plug.get('enabled', True) %}
plugin_{{ name }}:
  jenkins_plugin.present:
  - name: {{ plug.get('name', name) }}
  - restart: {{ plug.get('restart', False) }}
{% else %}
plugin_{{ name }}_disable:
   jenkins_plugin.absent:
   - name: {{ plug.get('name', name) }}
   - restart: {{ plug.get('restart', False) }}
{% endif %}
{% endfor %}

