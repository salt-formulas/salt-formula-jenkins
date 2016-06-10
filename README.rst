=======
Jenkins
=======

Jenkins is an application that monitors executions of repeated jobs, such as building a software project or jobs run by cron.

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

Example pillars
===============

Jenkins master

.. code-block:: yaml

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
        # Do not manage config.xml from Salt, use UI instead
        no_config: true
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

Jenkins slave

.. code-block:: yaml

    jenkins:
      slave:
        master:
          host: jenkins.example.com
          port: 80
          protocol: http
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

Usage
=====

Generate password hash:

.. code-block:: bash

    echo -n "salt{plainpassword}" | openssl dgst -sha256

Place in the configuration ``salt:hashpassword``.

Read more
=========

* https://wiki.jenkins-ci.org/display/JENKINS/Use+Jenkins
