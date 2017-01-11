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

Setup jenkins master.

``jenkins.slave``
-----------------

Setup jenkins slave.

``jenkins.job_builder``
-----------------------

Setup jenkins job builder.

``jenkins.client``
------------------

Setup jenkins client, works with Salt 2016.3+, supports pipeline workflow projects only now.


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

Sample pillars
==============

Jenkins master
--------------

Simple master with reverse proxy

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

Jenkins with experimental plugin source support

.. code-block:: yaml

    jenkins:
      master:
        enabled: true
        update_site_url: 'http://updates.jenkins-ci.org/experimental/update-center.json'


Agent (former slave)
--------------------

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

Client
------

Simple client with workflow job definition

.. code-block:: yaml

    jenkins:
      client:
        master:
          host: jenkins.example.com
          port: 80
          protocol: http
        job:
          jobname:
            type: workflow
            param:
              bool_param:
                type: boolean
                description: true/false
                default: true
              string_param:
                type: string
                description: 1 liner
                default: default_string
              text_param:
                type: text
                description: multi-liner
                default: default_text
          jobname_scm:
            type: workflow-scm
            concurrent: false
            scm:
              type: git
              url: https://github.com/jenkinsci/docker.git
              branch: master
              script: Jenkinsfile
              github:
                url: https://github.com/jenkinsci/docker
                name: "Jenkins Docker Image"
            trigger:
              github:
              pollscm:
                spec: "H/15 * * * *"
              reverse:
                projects:
                 - test1
                 - test2
                state: SUCCESS
            param:
              bool_param:
                type: boolean
                description: true/false
                default: true
              string_param:
                type: string
                description: 1 liner
                default: default_string
              text_param:
                type: text
                description: multi-liner
                default: default_text

Inline Groovy script samples

.. code-block:: yaml

    jenkins:
      client:
        job:
          test_workflow_jenkins_simple:
            type: workflow
            display_name: Test jenkins simple workflow
            script:
              content: |
                node {
                   stage 'Stage 1'
                   echo 'Hello World 1'
                   stage 'Stage 2'
                   echo 'Hello World 2'
                }
          test_workflow_jenkins_input:
            type: workflow
            display_name: Test jenkins workflow inputs
            script:
              content: |
                node {
                   stage 'Enter string'
                   input message: 'Enter job parameters', ok: 'OK', parameters: [
                     string(defaultValue: 'default', description: 'Enter a string.', name: 'string'),
                   ]
                   stage 'Enter boolean'
                   input message: 'Enter job parameters', ok: 'OK', parameters: [
                     booleanParam(defaultValue: false, description: 'Select boolean.', name: 'Bool'),
                   ]
                   stage 'Enter text'
                   input message: 'Enter job parameters', ok: 'OK', parameters: [
                     text(defaultValue: '', description: 'Enter multiline', name: 'Multiline')
                   ]
                }


GIT controlled groovy script samples

.. code-block:: yaml

    jenkins:
      client:
        source:
          base:
           engine: git
            address: repo_url
            branch: branch
          domain:
           engine: git
            address: domain_url
            branch: branch
        job:
          test_workflow_jenkins_simple:
            type: workflow
            display_name: Test jenkins simple workflow
            param:
              bool_param:
                type: boolean
                description: true/false
                default: true
            script:
              repository: base
              file: workflows/test_workflow_jenkins_simple.groovy
          test_workflow_jenkins_input:
            type: workflow
            display_name: Test jenkins workflow inputs
            script:
              repository: domain
              file: workflows/test_workflow_jenkins_input.groovy
          test_workflow_jenkins_input_jenkinsfile:
            type: workflow
            display_name: Test jenkins workflow inputs (jenknisfile)
            script:
              repository: domain
              file: workflows/test_workflow_jenkins_input/Jenkinsfile

GIT controlled groovy script with shared libraries

.. code-block:: yaml

    jenkins:
      client:
        source:
          base:
           engine: git
            address: repo_url
            branch: branch
          domain:
           engine: git
            address: domain_url
            branch: branch
        job:
          test_workflow_jenkins_simple:
            type: workflow
            display_name: Test jenkins simple workflow
            param:
              bool_param:
                type: boolean
                description: true/false
                default: true
            script:
              repository: base
              file: workflows/test_workflow_jenkins_simple.groovy
            libs:
            - repository: base
              file: macros/cookiecutter.groovy
            - repository: base
              file: macros/git.groovy

Plugins management from client

.. code-block:: yaml

    
    jenkins:
      client:
        plugin:
          swarm:
            restart: false
          hipchat:
            enabled: false
            restart: true

LDAP configuration (depends on LDAP plugin)

.. code-block:: yaml

    jenkins:
      client:
        security:
          ldap:
            server: 1.2.3.4
            root_dn: dc=foo,dc=com
            user_search_base: cn=users,cn=accounts
            manager_dn: ""
            manager_password: password
            user_search: ""
            group_search_base: ""
            inhibit_infer_root_dn: false


Matrix configuration (depends on auth-matrix plugin)

.. code-block:: yaml

    jenkins:
      client:
        security:
          matrix:
            permissions:
              Jenkins:
                # administrator access
                ADMINISTER:
                  - admin
                # read access (anonymous too)
                READ:
                  - anonymous
                  - user1
                  - user2
                # agents permissions
                MasterComputer: 
                  BUILD: 
                    - user3
              # jobs permissions
              hudson: 
                model:
                  Item:
                    BUILD: 
                      - user4

`Common matrix strategies <https://github.com/arbabnazar/configuration/blob/c08a5eaf4e04a68d2481375502a926517097b253/playbooks/roles/tools_jenkins/templates/projectBasedMatrixSecurity.groovy.j2>`_


Credentials enforcing from client

.. code-block:: yaml
    
    jenkins:
      client:
        credential:
          cred_first:
            username: admin
            password: password
          cred_second:
            username: salt
            password: password
          cred_with_key:
            username: admin
            key: SOMESSHKEY

Users enforcing from client

.. code-block:: yaml

    jenkins:
      client:
        user:
          admin:
            password: admin_password
            admin: true
          user01:
            password: user_password

Node enforcing from client using JNLP launcher

.. code-block:: yaml

    jenkins:
        client:
          node:
            node01:
              remote_home: /remote/home/path
              desc: node-description
              num_executors: 1
              node_mode: Normal
              ret_strategy: Always
              labels:
                - example
                - label
              launcher:
                 type: jnlp

Node enforcing from client using SSH launcher

.. code-block:: yaml

    jenkins:
        client:
          node:
            node01:
              remote_home: /remote/home/path
              desc: node-description
              num_executors: 1
              node_mode: Normal
              ret_strategy: Always
              labels:
                - example
                - label 
              launcher:
                 type: ssh
                 host: test-launcher
                 port: 22
                 username: launcher-user
                 password: launcher-pass

Setting node labels

.. code-block:: yaml

    jenkins:
        client:
            label:
              node-name:
                lbl_text: label-offline
                append: false # set true for label append instead of replace

SMTP server settings

.. code-block:: yaml

    jenkins:
      master:
        email:
          engine: "smtp"
          host: "smtp.domain.com"
          user: "user@domain.cz"
          password: "smtp-password"
          port: 25

Jenkins script approvals

.. code-block:: yaml
    
    jenkins:
      master:
        approved_scripts:
        - method groovy.json.JsonSlurperClassic parseText java.lang.String


Users enforcing from master

.. code-block:: yaml

    jenkins:
      user:
        admin:
          api_token: xxxxxxxxxx
          password: admin_password
          email: admin@domain.com
        user01:
          api_token: xxxxxxxxxx
          password: user_password
          email: user01@domain.com

Usage
=====

Generate password hash:

.. code-block:: bash

    echo -n "salt{plainpassword}" | openssl dgst -sha256

Place in the configuration ``salt:hashpassword``.

Read more
=========

* https://wiki.jenkins-ci.org/display/JENKINS/Use+Jenkins
