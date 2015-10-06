{% from "jenkins/map.jinja" import job_builder with context %}
{%- if pillar.jenkins.job_builder.enabled %}

include:
- git

{%- if not job_builder.pkgs %}
# Install job builder with pip if we don't have package

include:
- python

jenkins_job_builder_install:
  pip.installed:
    - names:
      - jenkins-job-builder
    - require:
      - pkg: jenkins_job_builder_packages

{%- else %}

jenkins_job_builder_install:
  pkg.installed:
    - names: {{ job_builder.pkgs }}
    - require:
      - pkg: jenkins_job_builder_packages

jenkins_job_builder_packages:
  pkg.installed:
  - names:
    - python-yaml
    - python-jenkins
    - python-pip
    - python-pbr
  - require:
    - pkg: python_packages

{%- endif %}

/srv/jenkins:
  file.directory:
  - user: root
  - group: root
  - mode: 755
  - makedirs: true

{{ job_builder.conf_dir }}:
  file.directory:
  - user: root
  - group: root
  - mode: 755
  - makedirs: true

{{ job_builder.config_file }}:
  file.managed:
  - source: salt://jenkins/files/jenkins_jobs.ini
  - user: root
  - group: root
  - mode: 400
  - template: jinja
  - require:
    - file: /etc/jenkins_jobs

{{ pillar.jenkins.job_builder.config.address }}:
  git.latest:
  - target: /srv/jenkins/job_builder_config
  - rev: {{ pillar.jenkins.job_builder.config.branch }}
  - require:
    - file: /srv/jenkins

jenkins_job_builder_jobs_update:
  cmd.run:
  - name: jenkins-jobs update /srv/jenkins/job_builder_config
  - require:
    - git: {{ pillar.jenkins.job_builder.config.address }}
    - file: {{ job_builder.config_file }}
    {%- if not job_builder.pkgs %}
    - pkg: jenkins_job_builder_install
    {%- else %}
    - pip: jenkins_job_builder_install
    {%- endif %}

{%- endif %}
