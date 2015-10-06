=======
Jenkins
=======

Install and configure Jenkins master and slave.

Available states
================

.. contents::
    :local:

``jenkins.master``
------------------

Setup jenkins master

``jenkins.slave``
-----------------

Setup jenkins slave

``jenkins.job_builder``
-----------------------

Setup jenkins job builder

Available metadata
==================

.. contents::
    :local:

``metadata.jenkins.master.single``
----------------------------------

Setup single-node master


``metadata.jenkins.slave.single``
---------------------------------

Setup Jenkins slave

Configuration parameters
========================


Example reclass
===============

Master
------

.. code-block:: yaml

   classes:
   - service.jenkins.master

  parameters:
    _param:
      jenkins_admin_token: xyz
      jenkins_admin_password_hash: xyz
      jenkins_admin_password: xyz
      job_builder_config_address: git@github.com:xyz/myjobs.git
      job_builder_config_branch: master
    nginx:
      server:
        site:
          jenkins:
            enabled: true
            type: nginx_proxy
            name: jenkins
            proxy:
              host: 127.0.0.1
              port: 8080
              protocol: http
            host:
              name: jenkins.example.com
              port: 80
    jenkins:
      master:
        mode: EXCLUSIVE
        slaves:
          - name: slave01
             label: pbuilder
             executors: 2
          - name: slave02
             label: image_builder
             mode: EXCLUSIVE
             executors: 2
        views:
          - name: "Package builds"
            regex: "debian-build-.*"
          - name: "Contrail builds"
            regex: "contrail-build-.*"
          - name: "Aptly"
            regex: "aptly-.*"
        plugins:
        - name: slack
        - name: extended-choice-parameter
        - name: rebuild
        - name: test-stability

Slave
-----

.. code-block:: yaml

     classes:
     - service.jenkins.slave.single
     - service.java.environment

     parameters:
        _param:
          java_environment_platform: openjdk
          java_environment_version: 7

        jenkins:
          slave:
            master:
              host: jenkins.example.com
              port: 80
            user:
              name: jenkins_slave
              password: dexiech6AepohthaiHook2iesh7ol5ook4Ov3leid3yek6daid2ooNg3Ee2oKeYo
            gpg:
              keypair_id: A76882D3
              public_key: |
                -----BEGIN PGP PUBLIC KEY BLOCK-----
                ...
              private_key: |
                -----BEGIN PGP PRIVATE KEY BLOCK-----
                ...

Read more
=========

* https://wiki.jenkins-ci.org/display/JENKINS/Use+Jenkins
