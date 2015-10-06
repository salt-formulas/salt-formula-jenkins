{% from "jenkins/map.jinja" import slave with context %}

/var/lib/jenkins/keystonerc:
  file.managed:
  - source: salt://jenkins/files/keystonerc
  - user: jenkins
  - group: jenkins
  - mode: 0400
  - template: jinja
  - require:
    - service: jenkins_slave_service

jenkins_slave_openstack_clients:
  pkg.installed:
  - names:
    - python-keystoneclient
    - python-novaclient
    - python-neutronclient
    - python-glanceclient
