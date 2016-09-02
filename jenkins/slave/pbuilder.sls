{% from "jenkins/map.jinja" import slave with context %}

jenkins_debian_glue_packages:
  pkg.latest:
  - names:
    - reprepro
    - cowbuilder
    - jenkins-debian-glue
    - git-buildpackage
    - debhelper
    {%- if slave.get('arch', grains.osarch) != grains.osarch %}
    - qemu-user
    {%- endif %}

/srv/repository:
  file:
  - directory
  - user: jenkins
  - mode: 755
  - makedirs: true
  - require:
    - service: jenkins_slave_service

/etc/sudoers.d/98-jenkins-debian-glue:
  file.managed:
  - source: salt://jenkins/files/slave/sudoer_debian_glue
  - template: jinja
  - user: root
  - group: root
  - mode: 440
  - require:
    - service: jenkins_slave_service

/etc/pbuilderrc:
  file.managed:
    - source: salt://jenkins/files/slave/pbuilderrc
    - template: jinja
    - user: root
    - group: root
    - mode: 644
    - require:
      - pkg: jenkins_debian_glue_packages

/var/cache/pbuilder:
  file.symlink:
  - target: /var/lib/jenkins/pbuilder
  - require:
    - file: /var/lib/jenkins/pbuilder
  - require_in:
    - pkg: jenkins_debian_glue_packages

/var/lib/jenkins/pbuilder:
  file:
  - directory
  - user: jenkins
  - group: jenkins
  - mode: 755
  - makedirs: true

{%- if slave.pbuilder.ccachedir is defined %}
{{ slave.pbuilder.ccachedir }}:
  file.directory:
  - user: root
  - group: root
  - mode: 777
  - makedirs: true
  - require:
    - file: /var/cache/pbuilder
{%- endif %}
