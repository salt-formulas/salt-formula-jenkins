{% from "jenkins/map.jinja" import client with context %}

include:
  - jenkins.client

{%- for source_name, source in client.get('source', {}).iteritems() %}

{%- if source.engine == "git" %}

jenkins_{{ source_name }}_source:
  git.latest:
  - name: {{ source.address }}
  - target: {{ client.dir.jenkins_root }}/{{ source_name }}
  - rev: {{ source.branch }}
  - reload_pillar: True

{%- elif client.source.engine == "local" %}

jenkins_{{ source_name }}_dir:
  file.managed:
  - name: {{ client.dir.jenkins_root }}/{{ source_name }}
  - mode: 700

{%- endif %}

{%- endfor %}
