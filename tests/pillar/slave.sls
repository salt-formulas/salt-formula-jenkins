jenkins:
  slave:
    enabled: true
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
java:
  environment:
    enabled: true
    version: '10'
    release: '0.1'
    build: '10'
    oracle_hash: 'fb4372174a714e6b8c52526dc134031e'
    platform: oracle-java
    development: true
linux:
  system:
    enabled: true
    user:
      not_a_jenkins:
        enabled: true
        name: notJenkins
        sudo: false
        uid: 9991
        full_name: Not A. Jenkins
        home: /home/notjenkins
        home_dir_mode: 755