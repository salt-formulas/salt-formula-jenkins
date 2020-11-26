{% from "jenkins/map.jinja" import master with context %}

{%- for user_name, user in master.user.items() %}

{{ master.home }}/users/{{ user_name }}:
  file.directory:
  - makedirs: true
  - user: jenkins
  - group: jenkins

{{ master.home }}/users/{{ user_name }}/config.xml:
  file.managed:
  - source: salt://jenkins/files/config.xml.user
  - template: jinja
  - user: jenkins
  - group: jenkins
  - require:
    - file: {{ master.home }}/users/{{ user_name }}
  - defaults:
      user_name: "{{ user_name }}"
  - watch_in:
    - service: jenkins_master_service
  - unless: test -e {{ master.home }}/users/{{ user_name }}/.config_created

{{ master.home }}/users/{{ user_name }}/.config_created:
  file.managed:
  - user: jenkins
  - group: jenkins
  - require:
    - file: {{ master.home }}/users/{{ user_name }}/config.xml
  - unless: test -e {{ master.home }}/users/{{ user_name }}/.config_created

{%- endfor %}
