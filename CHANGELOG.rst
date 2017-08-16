=========
Changelog
=========

Version 2017.8
=============================

commit 431a69479ff797f0561ee227931cadbae09bca89 (HEAD -> master, origin/master, origin/HEAD)
Author: Jakub Josef <jakub.josef@gmail.com>

    Fixed artifactory config enforcing

commit ff4059c188205660d282c9a25e6ba09f75b9318a
Author: Jakub Josef <jakub.josef@gmail.com>

    Fixed jenkins artifactory server enforcement

commit 63dd4028ea8634669ce53384ad7e992f0859397d
Merge: f4e588d 6606be0
Author: Jakub Josef <jjosef@mirantis.com>

    Merge "Removed hardcode in the LDAP server name"

commit f4e588ddf61e615319f3fb60400ba5fbed780228
Merge: 9bb6865 6f97771
Author: Alexander Evseev <aevseev@mirantis.com>

    Merge "Add optional parameter to set JJB version from PIP"

commit 6f977715b67ed56cb4ae1f178f34c697bb7c1eb1
Author: Alexander Evseev <aevseev@mirantis.com>

    Add optional parameter to set JJB version from PIP

commit 9bb6865a1c17b483e04b7cdc5c1296620c554f6b
Author: Alexander Evseev <aevseev@mirantis.com>

    Don't fail if job_builder.config.path is not set

commit d31123cfa2aa3333261951dd8c75edb904583c5a
Author: Alexander Evseev <aevseev@mirantis.com>

    Add optional path to job definitions for JJB

commit 362c02fde248f36b13c8aa04738d36cd61f24360
Author: Yuriy Taraday <yorik.sar@gmail.com>

    Fix XML for workflow

commit ea190435024c74dd2a213d51276b71fbf8914a6f
Author: chnyda <chnyda@mirantis.com>

    Fix grains and display

commit 9c05a3d7487b6fa76045a9c26bc92ec6852b6eae
Author: chnyda <chnyda@mirantis.com>

    Use version instead of backupVersion for grains

commit 2d78731b32469e7c2d251183d3af69df280bfbd7
Author: chnyda <chnyda@mirantis.com>

    Fix exception if jenkins job doesn't exist

commit d6f7635933fb836d0d88c3a491a603323686c5a3
Author: chnyda <chnyda@mirantis.com>

    Fix grains in case python-jenkins not installed

commit 124ca04baa3d08462aaf09bc9b219f7962595ee8
Author: chnyda <chnyda@mirantis.com>

    Fix job templates and grain

commit 90f133f8b0095b9728758c01416d09ee93313200
Author: chnyda <chnyda@mirantis.com>

    Compare jobs files with their hash and update templates

commit 6606be0354d76b97ad94cdbca599e28766cf4fab
Author: Andrey <agrebennikov@mirantis.com>

    Removed hardcode in the LDAP server name

commit a58e828530683af882bfff3d5c1cb5862cadf972
Author: Ales Komarek <ales.komarek@newt.cz>

    Optional credentials for lib

commit 9d9b0ed9fa5d89ca066a3ac7890ca7c41199a558
Author: Jakub Josef <jakub.josef@gmail.com>

    Improved artifactory servers control

commit 86686e9dd64b1ec8caf0301653478448705e8656
Author: Jakub Josef <jakub.josef@gmail.com>

    Fixed enforcing an artifactory config issue while setting up a new server

commit da02b2e6b3201cbae7c1a6a31e6efa68104067b6
Author: Ruslan Kamaldinov <rkamaldinov@mirantis.com>

    Fix jobs cleanup

commit 3d8bffe2d80ebdfb69bd89b434e763aa1847f978
Author: Ilya Kharin <ikharin@mirantis.com>

    Add verbose error messages at __virtual__

commit 7f95b080009a9691cbab172da24d81c59b743340
Author: Ilya Kharin <ikharin@mirantis.com>

    Add python-bcrypt as a dependency for the formula

commit cfafe5b2eedb7888964cbad107251af5b66058fb
Author: chnyda <chnyda@mirantis.com>

    Add support of regex in trigger from gerrit branch

commit ff010661c80a8a1359bc6a36f6cb5de4a54d25d5
Merge: 0a56d08 7339a00
Author: Jakub Josef <jakub.josef@gmail.com>

    Merge "Fixed jenkins master node configuration"

commit 7339a0044b9175e32ec9b5474727870780c88f29
Author: Jakub Josef <jakub.josef@gmail.com>

    Fixed jenkins master node configuration

commit 0a56d08594b9ed8e31e7c47a67dc76f03c3b3a9e
Merge: 86b7059 5878754
Author: Jakub Josef <jakub.josef@gmail.com>

    Merge "Fixed Jenkins master configuration enforcing"

commit 5878754461cc98125a0ef23be79050931203a363
Author: Jakub Josef <jakub.josef@gmail.com>

    Fixed Jenkins master configuration enforcing

commit 86b7059c71882699c153bfb17a6de51c3a0dbe2e
Merge: 1f0384a d2a6203
Author: Jakub Josef <jakub.josef@gmail.com>

    Merge "Fixed labels in master node config enforcing"

commit d2a62036b3707219e30102248c4772d6112b82df
Author: Jakub Josef <jakub.josef@gmail.com>

    Fixed labels in master node config enforcing

commit 1f0384afa5bf6295a9ffdecfb2229847e8ce74da
Author: Filip Pytloun <filip@pytloun.cz>

    Fix invalid syntax

commit 23d2c24d4ca3eda74533ad5237655c0ab07748c7
Author: Filip Pytloun <filip@pytloun.cz>

    Fix typo

commit c03fdeccb91493cd6ce5aebaf4c6d3caca170ce3
Merge: 5e528da b07ce1d
Author: jenkins-mk jenkins-mk <jenkins-mk@gerrit.mcp.mirantis.net>

    Merge "Fixed pipeline global library configuration saving error"

commit b07ce1dd55ca6e8a16a5330c9b6398e52ac434cd
Author: Jakub Josef <jakub.josef@gmail.com>

    Fixed pipeline global library configuration saving error

commit 5e528da06d09ccac3bb800b386eb84878f0de292
Merge: c614fff 1bb7f44
Author: Jakub Josef <jakub.josef@gmail.com>

    Merge "Added jenkins master configuration possibility"

commit 1bb7f44575285ecd82986a453dbc0456285e7693
Author: Jakub Josef <jakub.josef@gmail.com>

    Added jenkins master configuration possibility

commit c614fff46199b7cbc2c3f8e4fd87e3ae708d809d
Merge: 2c98794 269a104
Author: Jakub Josef <jjosef@mirantis.com>

    Merge "Remove newline at EOF in hudson.model.UpdateCenter.xml"

commit 269a10492889946da76458675563b47ec059ad14
Author: Yuriy Taraday <yorik.sar@gmail.com>

    Remove newline at EOF in hudson.model.UpdateCenter.xml

commit 2c9879445826a1c2fc7807615abc2c00c5225e51
Merge: 69871cf 691fb37
Author: Jakub Josef <jakub.josef@gmail.com>

    Merge "Fixed manipulation with global libraries in some weird cases"

commit 691fb372db5e2cdfcb31cf654ec43f8a5d5714a6
Author: Jakub Josef <jakub.josef@gmail.com>

    Fixed manipulation with global libraries in some weird cases

commit 69871cf67c946591523d9e09bca1be195c8c675b
Merge: 1cd53c9 8fd8294
Author: Jakub Josef <jakub.josef@gmail.com>

    Merge "Fixed SMTP settigns enforcing"

commit 8fd829465463770d85d2697ed44cb65f83da8557
Author: Jakub Josef <jakub.josef@gmail.com>

    Fixed SMTP settigns enforcing

commit 1cd53c9b300b459ecfe901b3807622fc4e996725
Merge: 27d05b3 a081153
Author: Jakub Josef <jakub.josef@gmail.com>

    Merge "Fixed jenkins smtp and admin email enforcing"

commit a08115330f96151723121ade1ed333d8e9310d44
Author: Jakub Josef <jakub.josef@gmail.com>

    Fixed jenkins smtp and admin email enforcing

commit 27d05b3a743b040b4ce1495d1a580e275fadb927
Author: Tomáš Kukrál <tomkukral@users.noreply.github.com>

    fix meta/salt with missing pillar

commit 5b7ae22d1530b421c33efe5d75c9779356bd0e03
Merge: 8ead66b 9f6c570
Author: Jakub Josef <jakub.josef@gmail.com>

    Merge "Fixed typo in jenkins smtp server"

commit 9f6c5702d49d0da4b7b3e989daf53ac8142ae19d
Author: Jakub Josef <jakub.josef@gmail.com>

    Fixed typo in jenkins smtp server

commit 8ead66b72b8449459b4a039331496e46acfbd4e0
Merge: c70d18b 0194025
Author: Filip Pytloun <fpytloun@mirantis.com>

    Merge "Implemented artifactory server enforcing"

commit 01940256e608cddf7796c1fca75214df8fc4848c
Author: Jakub Josef <jakub.josef@gmail.com>

    Implemented artifactory server enforcing

commit c70d18b393d78ba132ad383978e82d0f00fd3330
Author: Filip Pytloun <filip@pytloun.cz>

    Manage minion.d using support metadata

commit b393e4ade6737e44f63f9cdfdee4df9a23c86abd
Author: Mark Mastoras <mmastoras@dprails.com>

    Update service.sls

commit de52b1c11928600254b6bf782ee541675ce20e6e
Merge: b66b2f6 dfb288c
Author: Filip Pytloun <fpytloun@mirantis.com>

    Merge "Improved Jenkins SMTP settings"

commit dfb288c47f4ac01feea6e551ae5edecb98847e35
Author: Jakub Josef <jakub.josef@gmail.com>

    Improved Jenkins SMTP settings

commit b66b2f66b615e03a06f2668ef7fef17fceeeb1fa
Merge: 70d2220 d97f0fa
Author: Jakub Josef <jakub.josef@gmail.com>

    Merge "Revert "Improved Jenkins plugin installing""

commit d97f0fa7d8d646d62d89c73e0c8eb4c2b630bed8
Author: Jakub Josef <jakub.josef@gmail.com>

    Revert "Improved Jenkins plugin installing"

commit 70d22201f2b1767162b65913a19c47c6e04b603b
Merge: 07fc80d bd692e9
Author: Jakub Josef <jakub.josef@gmail.com>

    Merge "Improved Jenkins plugin installing"

commit bd692e97b54b69442dffc0d700479799c453f8c7
Author: Jakub Josef <jakub.josef@gmail.com>

    Improved Jenkins plugin installing

commit 07fc80dc252010e39de10fe2a935af2cdc6f3534
Merge: 17e19f2 e74e7a6
Author: Jakub Josef <jakub.josef@gmail.com>

    Merge "Fixed imports in categorized views"

commit e74e7a62d516cd5c44445b322f554484c6d3ac6f
Author: Jakub Josef <jakub.josef@gmail.com>

    Fixed imports in categorized views

commit 17e19f2d8f97696f627476a1aa08b865331aed99
Author: Tomáš Kukrál <tomkukral@users.noreply.github.com>

    empty timer means no timer

commit 7d9fce3e18fd0d1c0e63e8f1d182eea923de6774
Author: Jakub Josef <jakub.josef@gmail.com>

    Extended jenkins views enforcing by Categorize Views

commit 0a03c2cee0c10e8890f7250332fbff16261f04b0
Author: Jakub Josef <jakub.josef@gmail.com>

    Fix script approvals from client side

commit 1a6627c7b27280b53bd62a3b222979fdd2fb2915
Author: Jakub Josef <jakub.josef@gmail.com>

    Added support for gerrit trigger silent modes

commit 26956a684c470e4f7742d80fbee5e7719807532e
Author: Jakub Josef <jakub.josef@gmail.com>

    New version of jenkins user enforcing

commit bf0b73ee16d72df647d719e33bcb6845200e7635
Author: Jakub Josef <jakub.josef@gmail.com>

    Implemented jenkins scripts approving from client size

commit 1aa64a58fc56df4fdc8b16c89bc7aa9d16bfebbd
Author: Jakub Josef <jakub.josef@gmail.com>

    Fix existence checking in jenkins credential state

commit 81e158a29d06e6395cfbdaad216bcccb8bf4023f
Author: Jakub Josef <jakub.josef@gmail.com>

    Remove whitespace from gerrit trigger vote skipping

commit 7a3d4955edba5826eb390b958ccdd0114c2766d4
Author: Jakub Josef <jakub.josef@gmail.com>

    Deleted extra comma

commit facfadd57fc059ce70448c098fda51ad4e7dac2a
Author: Jakub Josef <jakub.josef@gmail.com>

    Fix Jenkins credentials state

commit 35553056075843b696ff6299d506da617ae14083
Author: Jakub Josef <jakub.josef@gmail.com>

    Fixed working with Jenkins credentials with same id

commit e01cf3c78cae53c70d9c6c0e63b9539d0a10e65b
Author: Jakub Josef <jakub.josef@gmail.com>

    Implemented enforcing of Jenkins themes

commit 2a847fa447ce19f0b87149d6d5ca437abf0c95e4
Author: Filip Pytloun <filip@pytloun.cz>

    Always set user and password in minion config

commit 8539c8909fb4ec2d20292cee2b66cb44f153107b
Author: Jakub Josef <jakub.josef@gmail.com>

    Implement skip voting on gerrit triggers

commit f2450bf995ad43b037d411932edcc68d62fe35ef
Author: Jakub Josef <jakub.josef@gmail.com>

    Add posibility to set compare type in Gerrit triggers

commit 301dff8e09a5d8fbead716be4479850fc634d6ec
Author: Filip Pytloun <filip@pytloun.cz>

    Accept None as value of slave.user

commit 99bc3ef235caaa091fd02ce04403bff84e5e2d76
Author: Filip Pytloun <filip@pytloun.cz>

    Accept None as a parameter to client.master.username

commit f4b304dc8db123ba9f9887fa7cfc70d7d9adc01d
Author: Filip Pytloun <filip@pytloun.cz>

    Always set default value for parameters

commit a9cf2c65ad7540230f1958c037c684b2d963dfcb
Author: Tomáš Kukrál <tomkukral@users.noreply.github.com>

    add support for job timer

commit 83129fc2b5ee567623fa878ffffc983744db69e4
Author: Filip Pytloun <filip@pytloun.cz>

    Add support for replacing more params using job templates

commit 061f77c0043d573f58e6994a3505814879890a0d
Author: Filip Pytloun <filip@pytloun.cz>

    Fix job template

commit dd9f47c54974132f8290a47f0501faddf894aebd
Author: Filip Pytloun <filip@pytloun.cz>

    Add support for defining quiet period

commit 01b485a45558720f21161ab1f4dddd23d7eaa2f5
Author: Filip Pytloun <filip@pytloun.cz>

    Add gerrit triggers

commit 0e1abdb54adc3dbd83d33d37a5523f14465e598a
Author: Filip Pytloun <filip@pytloun.cz>

    Fix jobs cleanup when job templating is used

commit 73bf99530c491dada7b64022f4799f049ca0052c (gerrit/master)
Author: Jakub Josef <jakub.josef@gmail.com>

    Improved Jenkins global lib config state.

commit 6e0cda9a29b921503f3583e4f9b3fc7104d01c9f
Author: Jakub Josef <jakub.josef@gmail.com>

    Implemented Jenkins global libs configuration by salt.

commit ffe8bb20cd59fefcba2d4959f9ab68f78c9d83c6
Author: Ales Komarek <ales.komarek@newt.cz>

    Jenkins job templating

commit 120714d2a0911ca580b7f19d7347ca5b064308e6
Author: Jakub Josef <jakub.josef@gmail.com>

    Implemented max keep builds property on jobs

commit adf72faea369c17baf628fa0434a533a28acd527 (tag: mcp0.5)
Author: Filip Pytloun <filip@pytloun.cz>

    Unify Makefile, .gitignore and update readme

commit 654a148bb903c50214d217910a26c78d289444db
Author: Jakub Josef <jakub.josef@gmail.com>

    Fixed creating jobs diff generating.

commit 2a7739bfbeae8dbbc0bd060638ad253be31c218f
Author: Jakub Josef <jakub.josef@gmail.com>

    Impemented Jenkins jobs cleanup - uninstallation of all undefined jobs.

commit a6d4c83d98c5334beba7cfda951a7b555b6943df
Author: Jakub Josef <jakub.josef@gmail.com>

    Implemented Jenkins Slack plugin configuration.

commit 60cc9d2c2b6588fd48b8682a1424f629607e65dc
Author: Jakub Josef <jakub.josef@gmail.com>

    Implemented SMTP settings from client side via script api.

commit 95ad9806f73bfa9a72a95b61b9d9d03500ed8a40
Author: Jakub Josef <jakub.josef@gmail.com>

    Improved working with None due to weird YAML get() behaviour.

commit 0ee470e197ea77c053b8286d10f66b324f980a9d
Author: Jakub Josef <jakub.josef@gmail.com>

    Matrix security extended to use GlobalMatrixAuthStrategy or ProjectMatrixAuthStrategy

commit 7bb17ab3b5a8c5897deccb259c169e30d39c8edc
Author: Jakub Josef <jakub.josef@gmail.com>

    Implemented Jenkins views enforcing.

commit 063a75367eb49b369e6dd63655dd768d45422b87
Author: Jakub Josef <jakub.josef@gmail.com>

    Implemented LDAP config and matrix auth security enforcements.

commit 10b4e10dceae8d75d2f8683c40747990b2b0958b
Author: Jakub Josef <jakub.josef@gmail.com>

    Implemented plugins management from client side.

commit b395d8e9dd35bf5aed8e627d9a8a8125621e0781
Author: Jakub Josef <jakub.josef@gmail.com>

    Fixed jenkins credential params string generating.

commit ebcf9dde381786dba6f3d9871881145932f4c5a9
Author: Filip Pytloun <filip@pytloun.cz>

    Fix joining list

commit ff34813848dafd94270ba58e9f84472409a9678c
Author: Jakub Josef <jakub.josef@gmail.com>

    Improved existence checking for SSH credentials.

commit f740e037cd47e04fa09bacb9cb5dc404103c47bc
Author: Filip Pytloun <filip@pytloun.cz>

    Fix indent

commit 96465fa0af4b2f08d01b6f9c5a85a0c37b9071dc
Author: Filip Pytloun <filip@pytloun.cz>

    Fix escape

commit b6c60bcd088dbc2e64727866d5a908bf059e8433
Author: Jakub Josef <jakub.josef@gmail.com>

    Fixed creating private-key based creds.

commit ae6bd09969cba0291cf40efcedf41ee8c868dd44
Author: Filip Pytloun <filip@pytloun.cz>

    Escape SSH key

commit 929312cd88ef858e7a5952f5dd2b5c1d26317701
Author: Jakub Josef <jakub.josef@gmail.com>

    Fixed diffing in jenkins_job state, cleanups.

Version 2016.12.1
=============================

commit d50c5fb1832f7b809d7736880a1b2bfc75013094 (tag: mk22-sl, tag: 2016.12.1)
Author: Filip Pytloun <filip@pytloun.cz>

    Add docs for jenkins.client

commit 201f712f00f0d6fcbe4561347126855b2b51e4ec
Author: Jaroslav Steinhaisl <jaroslav.steinhaisl@t-mobile.cz>

    repair name for new module jenkins_common

commit aa3991282685a9d0c57710469901de8a2b6e5ef3
Author: Jaroslav Steinhaisl <jaroslav.steinhaisl@t-mobile.cz>

    add missing endif statement

commit e380798663e95c9ff58ecc6edce1304f06ad3333
Author: Jakub Josef <jakub.josef@gmail.com>

    Implemented new jenkins_job states.
    Added forgotten node enforcement statement.
    Fixed PEP8 errors.

commit cd60ff2ea1da153145d33b0fdbd321eeebae117e
Author: Filip Pytloun <filip@pytloun.cz>

    Fix typo

commit 7ae6b240dffcd44f183b8c26efae72003faaeff7
Author: Jakub Josef <jakub.josef@gmail.com>

    Implemented existence checking in user state.

commit 98123aba83c4409dcb294799ba53d3585a658dfb
Author: Jakub Josef <jakub.josef@gmail.com>

    Added credentials and nodes existence testing.

commit 123be7a0d4f5d740b8183183efad00b068e24d06
Author: Jakub Josef <jakub.josef@gmail.com>

    First version of jenkins nodes enforcing.
    Fixed python-bcrypt dependency definition.
    Fixed plurals in state file names.

commit d7d727fcdcaad27026492c5e3061f99062719de8
Author: Jakub Josef <jakub.josef@gmail.com>

    Added python-bcrypt dependency to map.jinja.

commit 3de91af0e07c04d3150d9b07ddbaf33a6aff1d86
Author: Jakub Josef <jakub.josef@gmail.com>

    Implemented jenkins user enforcing by script API from client side

Version 2016.12
=============================

commit e13e2e7b5c11563fc1fce18f922064cbd6b6b89f
Author: Jakub Josef <jakub.josef@gmail.com>

    Fixed credentials enforcing in case of disabled jenkins security

commit 8e7385e2c01c9d601f96d15f0dc77682f939b4b7
Author: Jakub Josef <jakub.josef@gmail.com>

    First version of jenkins credentials enforcing via script API.

commit 2c70a1c6560ed9d4b530ee892098bc4724fe7ce2 (origin/meta, gerrit/meta)
Author: Ales Komarek <ales.komarek@newt.cz>

    jenkins service metadata

commit 65549fc399d3c5e1b713082e8b1d3def3e8ba5b3
Author: Jakub Josef <jakub.josef@gmail.com>

    Improved user enforcing

commit b36808c393fc53ddc9979e15b635e7abd154dc1a
Author: Filip Pytloun <filip@pytloun.cz>

    Fix external generation of users

commit 7088b86fd6f139b9be24f109172c4a832a1e8186
Author: Jakub Josef <jakub.josef@gmail.com>

    Implemented correct bcrypt hashing for jenkins users.

commit a777269818f5aab25c6d8fe21e8987efff84023e
Author: Jakub Josef <jakub.josef@gmail.com>

    Make user api token optional.

commit f00e4538d3597d830551b4ace4093ea4fa6515f6
Author: Jakub Josef <jakub.josef@gmail.com>

    Added API key to jenkins salt module config.

commit 92b1732bcd510218b18d0260efeee02e02cedaa1
Author: Filip Pytloun <filip@pytloun.cz>

    Fix wait for jenkins startup and plugin install for no-auth jenkins

commit 7d79c651637854b5770384e8ed20c97368a9810a
Author: Filip Pytloun <filip@pytloun.cz>

    Fix typos in meta/config.yml

commit 6bc424009e1ecd555d5988464e7e014f72114224
Author: Filip Pytloun <filip@pytloun.cz>

    Fix dependency

commit 41b6b767a9bb88381ee17e10c04372b10fb76289
Author: Filip Pytloun <filip@pytloun.cz>

    Fix no_config option

commit d8e042998dac45243abed3208fcb27fee409138d
Author: Jakub Josef <jakub.josef@gmail.com>

    First version of password hashing for jenkins.

commit 12e45943cdfbb3ae61be45628a70762a17137902
Author: Filip Pytloun <filip@pytloun.cz>

    Support users creation in external config generator

commit 0bfdf47cd4778fb3b31825e0386cd01b3c64610e (origin/config, gerrit/config)
Author: Filip Pytloun <filip@pytloun.cz>

    Fix unwanted space

commit b9b865235e8619c72e3a2f2b7b483b5edbe25fb7
Author: Filip Pytloun <filip@pytloun.cz>

    Add support for external config generation

commit 0c290cf05eded09d96d0ed7a509779719caa5688
Merge: 31883bb cdd4010
Author: Aleš Komárek <mail@newt.cz>

    Merge branch 'master' into 'master'

commit cdd40100458e0bacad2cda77a65f3ac04d3883ee
Author: Jakub Josef <jakub.josef@gmail.com>

    First version of jenkins credentials enforcement.

commit 31883bb1b79cf50fc092d3d42b788ebf83699394
Author: Jakub Josef <jakub.josef@gmail.com>

    Added Java param for disable setup wizard.

commit 2285d450754eb3340c91497f33451d0559cb112c
Author: Jakub Josef <jakub.josef@gmail.com>

    Typo fix.

commit e8d1560bc2e16c3c117c96ee64471927a1357ec2
Author: Jakub Josef <jakub.josef@gmail.com>

    Added basic SMTP settings enforcements.

commit 62b03542cd838005e03711bf6b203a0b1e8b8aea (origin/approved_scripts, gerrit/approved_scripts)
Author: Ales Komarek <ales.komarek@tcpcloud.eu>

    Approved scripts

commit aff292db58918ef2adc11977f379b00c656ff85b
Author: Ales Komarek <ales.komarek@tcpcloud.eu>

    Some unset job parameter handling

commit 737e9b3c5691562f31e90beb7c7211997ad0e90d
Author: Filip Pytloun <filip@pytloun.cz>

    Fix credentialsId position

commit 600aa1d31630e5bead37d42fdbd5883cec3c480d
Author: Filip Pytloun <filip@pytloun.cz>

    Allow using custom credentials id

commit b0a7da7db99f3557d58d59dcc996bd35de6df6f6
Author: Filip Pytloun <filip@pytloun.cz>

    Fix weird issue with submitting complex default

commit f6f9f4c633262f0715af1989e492069287cc598e
Author: Filip Pytloun <filip@pytloun.cz>

    Allow disabling sandbox in workflow job

commit 81d0ffc60c1729948ef79497fa2a9db075656c2f (origin/workflow, gerrit/workflow)
Author: Filip Pytloun <filip@pytloun.cz>

    Start jenkins-slave using systemd on modern systems

commit ebd4d171db705e409544e6384fec050851b72606
Author: Filip Pytloun <filip@pytloun.cz>

    Allow defining workflow-scm type of jobs

commit e7d4cc585cfa2ea69b77dbcd435981de32068786
Author: Filip Pytloun <filip@pytloun.cz>

    Minor jenkins.client enhancements

commit 938d2669f994574bfb91c7ff77371cb749bfd7a9
Author: Filip Pytloun <filip@pytloun.cz>

    Metadata for jenkins.client

commit af967eeaccb562d71282aedda12cce694625b12f
Author: Ales Komarek <ales.komarek@tcpcloud.eu>

    Fixed import groovy, update site parameter

commit 5e3f702a1c918eb82595bf3b62b987b4ba865c32
Author: Ales Komarek <ales.komarek@tcpcloud.eu>

    Fixing the libraries and outputs

commit 5b672fd61e0c2c152c3a71bfb35d760cf9bda4fa
Author: Ales Komarek <ales.komarek@tcpcloud.eu>

    Multiple source repositories and shared libraries

commit 965f9fb7e7bee5a4ea4e6c56fa76e4565814731b
Author: Ales Komarek <ales.komarek@tcpcloud.eu>

    Conditional master credentials

commit daf31f7899a4b4636ac754aee6f8b85aa2f5378f
Author: Ales Komarek <ales.komarek@tcpcloud.eu>

    Load from files

commit e5a1ed6a6f5e0bd04c8b29e1ddc5dfa67077ea57
Author: Ales Komarek <ales.komarek@tcpcloud.eu>

    Jenkins client for job enforcement

commit 07793d5a385ff2ef2c0c99adea8b8b8c28625672
Author: Filip Pytloun <filip@pytloun.cz>

    Option to allow eatmydata in pbuilderrc

commit 3018daa4c19ff5cac9b0f4d035035048b794271d
Merge: cd13e44 9eba909
Author: Filip Pytloun <filip.pytloun@tcpcloud.eu>

    Merge branch 'hotfix/packages' into 'master'

commit 9eba909e263be386bf9d635e2a7a241b24bd28fa
Author: Michael Kutý <6du1ro.n@gmail.com>

    Use shorter if syntax.

commit 26736b5387ac4f33718f120054c3b1ee0cb1051c
Author: Michael Kutý <6du1ro.n@gmail.com>

    Support allow_empty_variables for job builder.
    When expanding strings, by default jenkins-jobs will raise an exception if there’s a key in the string, that has not been declared in the input YAML files. Setting this option to True will replace it with the empty string, allowing you to use those strings without having to define all the keys it might be using.

commit cd13e445a91652568191716657caede763f3b0ae
Merge: 6e0f82c 6c9be58
Author: Filip Pytloun <filip.pytloun@tcpcloud.eu>

    Merge branch 'hotfix/packages' into 'master'

commit 37a359582a5e322b02f4c214bfbc846ec49ad15f
Author: Michael Kutý <6du1ro.n@gmail.com>

    Add missing protocol to readme.

commit 6c9be58aad4af4e24c7c1017aedf2566c9906d2e
Author: Michael Kutý <6du1ro.n@gmail.com>

    Do not force slack package in the defaults.

commit 6e0f82c8754ff6242cd52e87f65dc958408aae1b
Author: Filip Pytloun <filip@pytloun.cz>

    Add metadata.yml

commit 5b93440f4d1f21759397bcf6e6ce4eb3d26244ab
Author: Filip Pytloun <filip@pytloun.cz>

    Add missing Makefile

commit a5f661f96f976d8b4d76e387d8647d358eb39c93
Author: Filip Pytloun <filip@pytloun.cz>

    Add salt-master into build depends

commit 22ab0786f800e3994019c14b09ec8422321a58f5
Author: Filip Pytloun <filip@pytloun.cz>

    Add makefile, run tests during package build

commit f12a506b0d3d4c3454c1ea5375b210e3864488a1
Author: Filip Pytloun <filip@pytloun.cz>

    No sensu so far

commit 5bba731529aad47123dd371f0ac5b4a2ea28fe1c
Author: Filip Pytloun <filip@pytloun.cz>

    Configuration for backupninja support

commit 92083073829df0c5660e9ae25bfa9e06b8baba1a
Merge: 9d149bf 9bb7409
Author: Filip Pytloun <filip.pytloun@tcpcloud.eu>

    Merge branch 'master_service' into 'master'

commit 9bb7409aea3d94942c97aa8c1d7f68e45fbaa39e
Author: Ales Komarek <ales.komarek@tcpcloud.eu>

    Fix updates trying to setup before service does

commit 9d149bf121b983968980ea2f14a231d2260d302e
Author: Filip Pytloun <filip@pytloun.cz>

    Support arm64

commit 1b38503b8eea2bed1be6ca5da3cdc4e3fd67a48d
Author: Filip Pytloun <filip@pytloun.cz>

    Fix cowbuilder base

commit c23be27c7cc84ff305646d55eeb39d684e791b39
Author: Filip Pytloun <filip@pytloun.cz>

    Fix typo

commit c561e90110cb8ef454859972de1a063d4e95dd46
Author: Filip Pytloun <filip@pytloun.cz>

    Support for othermirror

commit 4ed2b9b4d131e803bda3d747b06e8f495ae700a6
Author: Filip Pytloun <filip@pytloun.cz>

    Allow per-os definition in pbuilderrc

commit e240bfa713417f53a754eb4e165637bdb23a2501
Author: Filip Pytloun <filip@pytloun.cz>

    Basic support for cross-compilation using pbuilder

commit a04fae1cfe0af05f6a6d7435c04360c1d3e5c0f2
Author: Filip Pytloun <filip@pytloun.cz>

    Fix default/jenkins

commit 505673cb84a10706598efd813ed0e8282b3265f0
Author: Filip Pytloun <filip@pytloun.cz>

    Fix init script

commit cedc460b1f860dddf4c0e2c43de2d93e80a8fc12
Author: Filip Pytloun <filip@pytloun.cz>

    Fix getting slave.jar with authentication

commit 52b9c2c471cc0d2419a201994d5ec28cee1f08c2
Author: Filip Pytloun <filip@pytloun.cz>

    Allow management of config.xml from UI

commit 7e5efcac78c9b8cdd12726928b6ebaa11fecc75c
Author: Ales Komarek <ales.komarek@tcpcloud.eu>

    slave params

commit 4c0bab1fd6bb6e419f64121bcc2a7fbbce4d064e
Author: Ales Komarek <ales.komarek@tcpcloud.eu>

    doc fixes

commit e5bb098c69424d0efcfc201718091fb2451de1ed
Author: Ales Komarek <ales.komarek@tcpcloud.eu>

    jenkins support files

commit 7b84b48a7347d9fde8c39c7d7ba7b7585efaccd0
Author: Ales Komarek <ales.komarek@tcpcloud.eu>

    Job builder tuning

commit 8aef52bbad14cbd6255a4aedad8520d77f94b7a2
Author: Ales Komarek <ales.komarek@tcpcloud.eu>

    fix to parameters

commit 214a77fb2703b8a563c1b765a60b273d7181c67a
Author: Filip Pytloun <filip@pytloun.cz>

    Set slave agent port

commit 9258ab437e72033339b7f4a3c67ea5fecfea2e09
Author: Alena Holanova <alena.holanova@tcpcloud.eu>

    Add support metadata

Version 0.2
=============================


