{% from "jenkins/map.jinja" import client with context %}
{% for name, prop in client.get('globalenvprop',{}).items() %}
{% if prop.get('enabled', True) %}
prop_{{ name }}:
  jenkins_globalenvprop.present:
  - name: {{ prop.get('name', name) }}
  - value: {{ prop.value }}
{% else %}
prop_{{ name }}_absent:
   jenkins_globalenvprop.absent:
   - name: {{ prop.get('name', name) }}
{% endif %}
{% endfor %}