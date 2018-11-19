=====
Usage
=====

Jenkins CI is an open source automation server written in Java. Jenkins
helps to automate the non-human part of software development process,
with continuous integration and facilitating technical aspects of
continuous delivery.

More information can be found at `<https://jenkins.io/>`_

Setup jenkins client, works with Salt 2016.3+, supports pipeline
workflow projects only for now.

Dependencies
============

To install on Ubuntu, you will need to add the jenkins debian repository
to the target server. You can do this with the
`salt-formula-linux formula <https://github.com/salt-formulas/salt-formula-linux>`_ ,
with the following pillar data:

.. code-block:: yaml

  linux:
    system:
      enabled: true
        repo:
        jenkins:
          enabled: true
          source: "deb http://pkg.jenkins.io/debian-stable binary/"
          key_url: "https://pkg.jenkins.io/debian/jenkins-ci.org.key"

This state will need to be applied *before* the jenkins state.

Using this formula
==================

To use this formula, you must install the formula to your Salt
Master as documented in
`saltstack formula docs <https://docs.saltstack.com/en/latest/topics/development/conventions/formulas.html#installation>`_

This formula is driven by pillar data, and can be used to
install either a Jenkins Master or Client. See pillar data
below for examples.

Sample pillars
==============

Master role
-----------

Simple master with reverse proxy:

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
        java_args: -Xms256m -Xmx1g
        # Do not manage any xml config files via Salt, use UI instead
        # Including config.xml and any plugin xml's.
        no_config: true
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

Jenkins master with experimental plugin source support:

.. code-block:: yaml

    jenkins:
      master:
        enabled: true
        update_site_url: 'http://updates.jenkins-ci.org/experimental/update-center.json'

SMTP server settings:

.. code-block:: yaml

    jenkins:
      master:
        email:
          engine: "smtp"
          host: "smtp.domain.com"
          user: "user@domain.cz"
          password: "smtp-password"
          port: 25

Script approvals from client:

.. code-block:: yaml

    jenkins:
      client:
        approved_scripts:
          - method groovy.json.JsonSlurperClassic parseText java.lang.String

Script approvals:

.. code-block:: yaml

    jenkins:
      master:
        approved_scripts:
        - method groovy.json.JsonSlurperClassic parseText java.lang.String

User enforcement:

.. code-block:: yaml

    jenkins:
      master:
        user:
          admin:
            api_token: xxxxxxxxxx
            password: admin_password
            email: admin@domain.com
          user01:
            api_token: xxxxxxxxxx
            password: user_password
            email: user01@domain.com

Agent (slave) role
------------------

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
        http_proxy: http://proxy.example.com:8080
        https_proxy: http://proxy.example.com:8080
        no_proxy: .corp,127.0.0.1

Client role
-----------

Simple client with workflow job definition:

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
              timer:
                spec: "H H * * *"
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

Inline Groovy scripts:

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

GIT controlled groovy scripts:

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

GIT controlled groovy script with shared libraries:

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

Setting job max builds to keep (amount of last builds stored on Jenkins master)

.. code-block:: yaml

    jenkins:
      client:
        job:
          my-amazing-job:
            type: workflow
            discard:
              build:
                keep_num: 5
                keep_days: 5
              artifact:
                keep_num: 6
                keep_days: 6

Using job templates in similar way as in jjb. For now just
1 defined param is supported:

.. code-block:: yaml

    jenkins:
      client:
        job_template:
          test_workflow_template:
            name: test-{{formula}}-workflow
            template:
              type: workflow
              display_name: Test jenkins {{name}} workflow
              param:
                repo_param:
                  type: string
                  default: repo/{{formula}}
              script:
                repository: base
                file: workflows/test_formula_workflow.groovy
            param:
              formula:
              - aodh
              - linux
              - openssh

Interpolating parameters for job templates:

.. code-block:: yaml

    _param:
      salt_formulas:
      - aodh
      - git
      - nova
      - xorg
    jenkins:
      client:
        job_template:
          test_workflow_template:
            name: test-{{formula}}-workflow
            template:
              ...
            param:
              formula: ${_param:salt_formulas}

Or simply define multiple jobs and it's parameters to
replace from template:

.. code-block:: yaml

   jenkins:
     client:
       job_template:
         test_workflow_template:
           name: test-{{name}}-{{myparam}}
           template:
             ...
           jobs:
             - name: firstjob
               myparam: dummy
             - name: secondjob
               myparam: dummyaswell

Purging undefined jobs from Jenkins:

.. code-block:: yaml

    jenkins:
      client:
        purge_jobs: true
        job:
          my-amazing-job:
            type: workflow

Plugins management from client:

.. code-block:: yaml

    jenkins:
      client:
        plugin_remove_unwanted: false
        plugin_force_remove: false
        plugin:
          plugin1: 1.2.3
          plugin2:
          plugin3: {}
          plugin4:
            version: 3.2.1
            enabled: false
          plugin5: absent

Adding plugin params to job:

.. code-block:: yaml

    jenkins:
      client:
        job:
          my_plugin_parametrized_job:
            plugin_properties:
              throttleconcurrents:
                enabled: True
                max_concurrent_per_node: 3
                max_concurrent_total: 1
                throttle_option: category #one of project (default or category)
                categories:
                  - my_throuttle_category
        plugin:
          throttle-concurrents:

LDAP configuration (depends on LDAP plugin):

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

Matrix configuration (depends on auth-matrix plugin):

.. code-block:: yaml

    jenkins:
      client:
        security:
          matrix:
            # set true for use ProjectMatrixAuthStrategy instead of GlobalMatrixAuthStrategy
            project_based: false
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

Views enforcing from client:

.. code-block:: yaml

    jenkins:
      client:
        view:
         my-list-view:
           enabled: true
           type: ListView
           include_regex: ".*"
         my-view:
           # set false to disable
           enabled: true
           type: MyView

View specific params:

- ``include_regex`` for ``ListView`` and ``CategorizedJobsView``
- categories for ``CategorizedJobsView``

Categorized views:

.. code-block:: yaml

    jenkins:
      client:
        view:
          my-categorized-view:
            enabled: true
            type: CategorizedJobsView
            include_regex: ".*"
            categories:
              - group_regex: "aptly-.*-nightly-testing"
                naming_rule: "Nightly -> Testing"
              - group_regex: "aptly-.*-nightly-production"
                naming_rule: "Nightly -> Production"

Credentials enforcing from client:

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
          cred_with_text_secret:
            secret: SOMETEXTSECRET
          cred_with_secret_file:
            filename: somefile.json
            content: |
              { "Hello": "world!" }

Users enforcing from client:

.. code-block:: yaml

    jenkins:
      client:
        user:
          admin:
            password: admin_password
            admin: true
          user01:
            password: user_password

Node enforcing from client using JNLP launcher:

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

Node enforcing from client using SSH launcher:

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

Configure Jenkins master:

.. code-block:: yaml

    jenkins:
      client:
        node:
          master:
            num_executors: 1
            node_mode: Normal # or Exclusive
            labels:
              - example
              - label

Setting node labels:

.. code-block:: yaml

    jenkins:
      client:
        label:
          node-name:
            lbl_text: label-offline
            append: false # set true for label append instead of replace

SMTP server settings from client:

.. code-block:: yaml

    jenkins:
      client:
        smtp:
          host: "smtp.domain.com"
          username: "user@domain.cz"
          password: "smtp-password"
          port: 25
          ssl: false
          reply_to: reply_to@address.com

Jenkins admin user email enforcement from client:

.. code-block:: yaml

    jenkins:
      client:
        smtp:
          admin_email: "My Jenkins <jenkins@myserver.com>"

Slack plugin configuration:

.. code-block:: yaml

    jenkins:
      client:
        slack:
          team_domain: example.com
          token: slack-token
          room: slack-room
          token_credential_id: cred_id
          send_as: Some slack user

Pipeline global libraries setup:

.. code-block:: yaml

    jenkins:
      client:
        lib:
          my-pipeline-library:
            enabled: true
            url: https://path-to-my-library
            credential_id: github
            branch: master # optional, default master
            implicit: true # optional default true

Artifactory server enforcing:

.. code-block:: yaml

    jenkins:
      client:
        artifactory:
          my-artifactory-server:
            enabled: true
            url: https://path-to-my-library
            credential_id: github

Jenkins Global env properties enforcing:

.. code-block:: yaml

    jenkins:
      client:
        globalenvprop:
          OFFLINE_DEPLOYMENT:
            enabled: true
            name: "OFFLINE_DEPLOYMENT" # optional, default using dict key
            value: "true"

Throttle categories management from client (requires
`Throttle Concurrent Builds <https://plugins.jenkins.io/throttle-concurrents>`_
plugin):

.. code-block:: yaml

    jenkins:
      client:
        throttle_category:
          'My First Category':
            max_total: 2
            max_per_node: 1
          'My Second Category':
            max_total: 5
            max_per_node: 2
            max_per_label:
              'node_label_1': 1
              'node_label_2': 2
          'My Category To Remove:
            enabled: false

Jira sites management from client (requires
`JIRA <https://plugins.jenkins.io/jira>`_ plugin):

.. code-block:: yaml

    # Remove all sites
    jenkins:
      client:
        jira:
          enabled: False

.. code-block:: yaml

    jenkins:
      client:
        jira:
          sites:
            'http://my.jira.site/':
              link_url: 'http://alternative.link/'
              http_auth: false
              use_wiki_notation: false
              record_scm: false
              disable_changelog: false
              issue_pattern: ''
              any_build_result: false
              user: 'username'
              password: 'passwd'
              conn_timeout: 10
              visible_for_group: ''
              visible_for_project: ''
              timestamps: false
              timestamp_format: ''

Gerrit trigger plugin configuration:

.. code-block:: yaml

    jenkins:
      client:
        gerrit:
          server1:
            host: "gerrit.domain.local"
            port: 29418
            username: "jenkins"
            email: "jenkins@domain.local"
            auth_key_file: "/var/jenkins_home/.ssh/id_rsa"
            frontendURL: "https://gerrit.domain.local"
            build_current_patches_only: true
            abort_new_patchsets: false
            abort_manual_patchsets: false
            abort_same_topic: false
            authkey: |
              SOMESSHKEY
          server2:
            host: "gerrit2.domain.local"
            port: 29418
            username: "jenkins"
            email: "jenkins@domain.local"
            auth_key_file: "/var/jenkins_home/.ssh/id_rsa"
            frontendURL: "https://gerrit2.domain.local"
            build_current_patches_only: true
            abort_new_patchsets: false
            abort_manual_patchsets: false
            abort_same_topic: false
            authkey: |
              SOMESSHKEY

CSRF Protection configuration:

.. code-block:: yaml

    jenkins:
      client:
        security:
          csrf:
            enabled: true
            proxy_compat: false

Agent to Master Access Control:

.. code-block:: yaml

    jenkins:
      client:
        security:
          agent2master:
            enabled: true
            whitelisted: ''
            file_path_rules: ''

Content Security Policy configuration:

.. code-block:: yaml

    jenkins:
      client:
        security:
          csp: "sandbox; default-src 'none'; img-src 'self'; style-src 'self';"

Usage
=====

#. Generate password hash:

   .. code-block:: bash

    echo -n "salt{plainpassword}" | openssl dgst -sha256

#. Place in the configuration ``salt:hashpassword``.


Read more
=========

* https://wiki.jenkins-ci.org/display/JENKINS/Use+Jenkins

Documentation and Bugs
======================

* http://salt-formulas.readthedocs.io/
   Learn how to install and update salt-formulas

* https://github.com/salt-formulas/salt-formula-jenkins/issues
   In the unfortunate event that bugs are discovered, report the issue to the
   appropriate issue tracker. Use the Github issue tracker for a specific salt
   formula

* https://launchpad.net/salt-formulas
   For feature requests, bug reports, or blueprints affecting the entire
   ecosystem, use the Launchpad salt-formulas project

* https://launchpad.net/~salt-formulas-users
   Join the salt-formulas-users team and subscribe to mailing list if required

* https://github.com/salt-formulas/salt-formula-jenkins
   Develop the salt-formulas projects in the master branch and then submit pull
   requests against a specific formula

* #salt-formulas @ irc.freenode.net
   Use this IRC channel in case of any questions or feedback which is always
   welcome

