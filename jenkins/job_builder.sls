{% from "jenkins/map.jinja" import job_builder with context %}
{%- if job_builder.enabled %}

include:
- git

{%- if job_builder.source.engine == 'pkg' %}

jenkins_job_builder_install:
  pkg.installed:
  - names: {{ job_builder.pkgs }}
  - require_in:
    - cmd: jenkins_job_builder_jobs_update

{%- else %}

jenkins_job_builder_packages:
  pkg.installed:
  - names:
    - python-yaml
    - python-jenkins
    - python-pip
    - python-pbr

jenkins_job_builder_install:
  pip.installed:
  - names:
    - jenkins-job-builder
  - require:
    - pkg: jenkins_job_builder_packages
  - require_in:
    - cmd: jenkins_job_builder_jobs_update

{%- endif %}

jenkins_job_dirs:
  file.directory:
  - names:
    - {{ job_builder.dir.base }}
    - {{ job_builder.dir.conf }}
  - user: root
  - group: root
  - mode: 755
  - makedirs: true

{{ job_builder.dir.conf }}/jenkins_jobs.ini:
  file.managed:
  - source: salt://jenkins/files/jenkins_jobs.ini
  - user: root
  - group: root
  - mode: 400
  - template: jinja
  - require:
    - file: jenkins_job_dirs

{{ job_builder.config.address }}:
  git.latest:
  - target: /srv/jenkins/job_builder_config
  - rev: {{ job_builder.config.branch }}
  - require:
    - file: jenkins_job_dirs

jenkins_job_builder_jobs_update:
  cmd.run:
  - name: jenkins-jobs update /srv/jenkins/job_builder_config
  - require:
    - git: {{ job_builder.config.address }}
    - file: {{ job_builder.dir.conf }}/jenkins_jobs.ini

{%- endif %}
