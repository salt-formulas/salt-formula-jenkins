{#- This state isn't designed to be called explicitly #}
{% from "jenkins/map.jinja" import client with context %}

{%- for source_name, source in client.get('source', {}).iteritems() %}

{%- if source.engine == "git" %}

jenkins_{{ source_name }}_source:
  git.latest:
  - name: {{ source.address }}
  - target: {{ client.dir.jenkins_source_root }}/{{ source_name }}
  - rev: {{ source.branch }}
  - reload_pillar: True
  - require:
    - jenkins_client_dirs

{%- elif client.source.engine == "local" %}

jenkins_{{ source_name }}_file:
  file.managed:
  - name: {{ client.dir.jenkins_source_root }}/{{ source_name }}
  - mode: 700
  - require:
    - jenkins_client_dirs

{%- endif %}

{%- endfor %}
