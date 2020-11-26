{#- It's not recommended to call this state explicitly as it requires plugins and credentials #}
{% from "jenkins/map.jinja" import client with context %}
{% for name, lib in client.get("lib",{}).items() %}
{%- if lib.enabled|default(True) %}
    global_library_{{ name }}:
      jenkins_lib.present:
        - name: {{ lib.get('name', name) }}
        - url: {{ lib.url }}
        {%- if lib.credential_id is defined %}
        - credential_id: {{ lib.credential_id }}
        {%- endif %}
        - branch: {{ lib.get("branch", "master") }}
{%- else %}
  global_library_{{ name }}_absent:
    jenkins_lib.absent:
    - name: {{ lib.get('name', name) }}
{%- endif %}
{% endfor %}