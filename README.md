
# Jenkins continuos integration

Jenkins is an application that monitors executions of repeated jobs, such as building a software project or jobs run by cron.

## Sample pillars

Jenkins masters

Jenkins master with user

    jenkins:
      master:
        enabled: true
        http:
          address: 0.0.0.0
          port: 8080
          protocol: http
        plugins:
        - name: git
        - name: metadata
        - name: envinject
        - name: greenballs
        - name: ansicolor
        - name: build-pipeline-plugin
        user:
          admin:
            api_token: api_token
            password_hash: salt:hashed_pwd_see_usage
            email: root@dmain.com
            public_keys:
            - key: ssh_public_key_of_current_root_user
        slaves:
        - name: slave1.domain.com
          executors: 2

Jenkins master with SSL

    jenkins:
      master:
        enabled: true
        http:
          address: 0.0.0.0
          port: 8080
          protocol: https
        ssl:
          enabled: true
          host: ci.domain.com
          authority: Org_Service_CA
        plugins:
        - name: git
        - name: metadata
        - name: envinject
        - name: greenballs
        - name: ansicolor
        - name: build-pipeline-plugin
        slaves:
        - name: slave1.domain.com
          executors: 2

### Jenkins job builder

Jenkins job builder to configure master

    jenkins:
      job_builder:
        enabled: true
        source: git
        address: https://git.openstack.org/openstack-infra/jenkins-job-builder
        branch: master
        config:
          source: git
          address: git@repo.domain.com:jenkins/jobs-org.git
          branch: develop
        master:
          host: localhost
          port: 8080
          protocol: http
          user: admin
          password: fsdfsdf9438r4fessc9sd

### Jenkins slaves

Slave with sudo :o

    jenkins:
      slave:
        enabled: true
        sudo: true
        master:
          host: localhost
          port: 8080
          protocol: http
        user:
          name: admin
          password: password

Jenkins slave with keystone credentials

    jenkins:
      slave:
        enabled: true
        master:
          host: localhost
          port: 8080
          protocol: http
        user:
          name: admin
          password: password
        keystone:

## Usage

User password generation. foo is password. bar is salt.

    echo -n 'foo{bar}' | sha256sum

## Read more

* https://wiki.jenkins-ci.org/display/JENKINS/Use+Jenkins
* https://wiki.jenkins-ci.org/display/JENKINS/Installing+Jenkins+on+Ubuntu
* https://github.com/jenkinsci/puppet-jenkins
* https://wiki.jenkins-ci.org/display/JENKINS/Distributed+builds
* http://ci.openstack.org/jenkins-job-builder/
* http://ci.openstack.org/jjb.html
* http://techs.enovance.com/6006/manage-jenkins-jobs-with-yaml
* http://zeroturnaround.com/rebellabs/top-10-jenkins-featuresplugins/
* https://wiki.jenkins-ci.org/display/JENKINS/Build+Pipeline+Plugin
* https://wiki.jenkins-ci.org/display/JENKINS/LTS+Release+Line
* https://gist.github.com/rowan-m/1026918
