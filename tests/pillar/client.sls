jenkins:
  client:
    enabled: true
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
    approved_scripts:
      - method groovy.json.JsonSlurperClassic parseText java.lang.String
java:
  environment:
    enabled: true
    version: '10'
    release: '0.1'
    build: '10'
    oracle_hash: 'fb4372174a714e6b8c52526dc134031e'
    platform: oracle-java
    development: true