{% from "jenkins/map.jinja" import master with context %}

{%- for user_name, user in master.user.iteritems() %}

/var/lib/jenkins/users/{{ user_name }}:
  file.directory:
  - makedirs: true

/var/lib/jenkins/users/{{ user_name }}/config.xml:
  file.managed:
  - source: salt://jenkins/files/config.xml.user
  - template: jinja
  - require:
    - file: /var/lib/jenkins/users/{{ user_name }}
  - defaults:
      user_name: "{{ user_name }}"
  - watch_in:
    - service: jenkins_master_service

{%- endfor %}
