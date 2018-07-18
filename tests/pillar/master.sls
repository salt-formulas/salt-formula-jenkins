jenkins:
  master:
    enabled: true
    mode: EXCLUSIVE
    no_config: false
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
    email:
      engine: "smtp"
      host: "smtp.domain.com"
      user: "user@domain.cz"
      password: "smtp-password"
      port: 25
    http:
      port: 80
    approved_scripts:
      - method groovy.json.JsonSlurperClassic parseText java.lang.String
    user:
      admin:
        api_token: xxxxxxxxxx
        password: admin_password
        email: admin@domain.com
      user01:
        api_token: xxxxxxxxxx
        password: user_password
        email: user01@domain.com
java:
  environment:
    enabled: true
    version: '10'
    release: '0.1'
    build: '10'
    oracle_hash: 'fb4372174a714e6b8c52526dc134031e'
    platform: oracle-java
    development: true