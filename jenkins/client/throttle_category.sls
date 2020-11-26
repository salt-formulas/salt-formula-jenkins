{#- It's not recommended to call this state explicitly as it requires plugins #}
{% from "jenkins/map.jinja" import client with context %}
{% for name, throttle_category in client.get("throttle_category",{}).items() %}
{% if throttle_category.get('enabled', True) %}
'throttle_category_{{ name }}':
  jenkins_throttle_category.present:
    - name: '{{ throttle_category.get('name', name) }}'
    - max_total: {{ throttle_category.get('max_total', 0) }}
    - max_per_node: {{ throttle_category.get('max_per_node', 0) }}
    - labels: {{ throttle_category.get('max_per_label',[]) }}
{% else %}
'throttle_category_{{ name }}_disable':
   jenkins_throttle_category.absent:
     - name: '{{ throttle_category.get('name', name) }}'
{% endif %}
{%- endfor %}
