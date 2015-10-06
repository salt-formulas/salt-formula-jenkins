{% from "jenkins/map.jinja" import slave with context %}

jenkins_gpg_key_dir:
  file.directory:
  - name: /var/lib/jenkins/.gnupg
  - user: jenkins
  - group: jenkins
  - mode: 700

gpg_priv_key:
  file.managed:
  - name: /var/lib/jenkins/.gnupg/secret.gpg
  - contents_pillar: jenkins:slave:gpg:private_key
  - user: jenkins
  - group: jenkins
  - mode: 600
  - require:
    - file: jenkins_gpg_key_dir

gpg_pub_key:
  file.managed:
  - name: /var/lib/jenkins/.gnupg/public.gpg
  - contents_pillar: jenkins:slave:gpg:public_key
  - user: jenkins
  - group: jenkins
  - mode: 644
  - require:
    - file: jenkins_gpg_key_dir

import_gpg_pub_key:
  cmd.run:
  - name: gpg --no-tty --import /var/lib/jenkins/.gnupg/public.gpg
  - user: jenkins
  - unless: gpg --no-tty --list-keys | grep '{{ slave.gpg.keypair_id }}'
  - require:
    - file: jenkins_gpg_key_dir

import_gpg_priv_key:
  cmd.run:
  - name: gpg --no-tty --allow-secret-key-import --import /var/lib/jenkins/.gnupg/secret.gpg
  - user: jenkins
  - unless: gpg --no-tty --list-secret-keys | grep '{{ slave.gpg.keypair_id }}'
  - require:
    - file: jenkins_gpg_key_dir
