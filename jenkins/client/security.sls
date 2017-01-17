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
{%- endif %}

{%- if client.security.matrix is defined %}
set_jenkins_matrix_security:
  jenkins_security.matrix:
    - strategies: {{ client.security.matrix.permissions }}
    - project_based: {{ client.security.matrix.get('project_based', False) }}
{%- endif %}