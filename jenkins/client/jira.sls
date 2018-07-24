{% from "jenkins/map.jinja" import client with context %}
{% if client.jira.get('enabled', True) %}
jenkins_jira_enable:
  jenkins_jira.present:
    - sites: {
      {% for name, site in client.jira.get('sites',[]).iteritems() %}
      '{{ name }}': {
        link_url: '{{ site.get('link_url', name) }}',
        http_auth: {{ site.get('http_auth', false) }},
        use_wiki_notation: {{ site.get('use_wiki_notation', false) }},
        record_scm: {{ site.get('record_scm', false) }},
        disable_changelog: {{ site.get('disable_changelog', false) }},
        issue_pattern: '{{ site.get('issue_pattern', '') }}',
        any_build_result: {{ site.get('any_build_result', false) }},
        user: '{{ site.get('user', '') }}',
        password: '{{ site.get('password', '') }}',
        conn_timeout: {{ site.get('conn_timeout', 10) }},
        visible_for_group: '{{ site.get('visible_for_group', '') }}',
        visible_for_project: '{{ site.get('visible_for_project', '') }}',
        timestamps: {{ site.get('timestamps', false) }},
        timestamp_format: '{{ site.get('timestamp_format', '') }}'
        },
      {% endfor %}
      }
    - require:
      - sls: jenkins.client.plugin
{% else %}
jenkins_jira_disable:
  jenkins_jira.absent
{% endif %}

