{% from "jenkins/map.jinja" import client with context %}
{% for name, lib in client.get("lib",{}).iteritems() %}
{%- if lib.enabled|default(True) %}
    global_library_{{ name }}:
      jenkins_lib.present:
        - name: {{ lib.get('name', name) }}
        - url: {{ lib.url }}
        {%- if lib.credential_id is defined %}
        - credential_id: {{ lib.credential_id }}
        - require:
          - jenkins_credential: {{ lib.credential_id }}
        {%- endif %}
        - branch: {{ lib.get("branch", "master") }}
{%- else %}
  global_library_{{ name }}_absent:
    jenkins_lib.absent:
    - name: {{ lib.get('name', name) }}
{%- endif %}
{% endfor %}
