{#- It's not recommended to call this state explicitly as it requires plugins #}
{% from "jenkins/map.jinja" import client with context %}
{% for name, view in client.get('view',{}).iteritems() %}
{% if view.get('enabled', True) %}
view_{{ name }}:
  jenkins_view.present:
  - name: {{ view.get('name', name) }}
  {%- for key, value in view.iteritems() %}
  {%- if key != "name" %}
  - {{ key }}: {{ value }}
  {%- endif %}
  {%- endfor %}
{% else %}
view_{{ name }}_disable:
   jenkins_view.absent:
   - name: {{ view.get('name', name) }}
{% endif %}
{% endfor %}