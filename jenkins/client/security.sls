{%- from "jenkins/map.jinja" import client with context %}
{%- if client.security.ldap is defined %}
set_jenkins_ldap:
  jenkins_security.ldap:
    - server: {{ client.security.ldap.server }}
    - root_dn: {{ client.security.ldap.get('root_dn','') }}
    - user_search_base: {{ client.security.ldap.get('user_search_base','') }}
    - manager_dn: {{ client.security.ldap.get('manager_dn','') }}
    - manager_password: {{ client.security.ldap.get('manager_password','') }}
    - user_search: {{ client.security.ldap.get('user_search','') }}
    - group_search_base: {{ client.security.ldap.get('group_search_base', '') }}
    - inhibit_infer_root_dn: {{ client.security.ldap.get('inhibit_infer_root_dn', False) }}
    - require:
      - sls: jenkins.client.plugin
{%- endif %}

{%- if client.security.matrix is defined %}
set_jenkins_matrix_security:
  jenkins_security.matrix:
    - strategies: {{ client.security.matrix.permissions }}
    - project_based: {{ client.security.matrix.get('project_based', False) }}
    - require:
      - sls: jenkins.client.plugin
{%- endif %}

{%- if client.security.csrf is defined %}
jenkins_csrf_protection:
  jenkins_security.csrf:
    - enabled: {{ client.security.csrf.get('enabled', False) }}
    - proxy_compat: {{ client.security.csrf.get('proxy_compat', False) }}
{%- endif %}

{%- if client.security.csp is defined %}
jenkins_content_security_policy:
  jenkins_security.csp:
    - policy: {{ client.security.csp }}
{%- endif %}

{%- if client.security.agent2master is defined %}
jenkins_agent2master_security:
  jenkins_security.agent2master:
    - enabled: {{ client.security.agent2master.get('enabled', False) }}
    - whitelisted: |
        {{ client.security.agent2master.get('whitelisted', '')|indent(8) }}
    - file_path_rules: |
        {{ client.security.agent2master.get('file_path_rules', '')|indent(8) }}
{%- endif %}

