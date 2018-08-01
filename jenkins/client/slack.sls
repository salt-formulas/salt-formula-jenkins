{%- from "jenkins/map.jinja" import client with context %}
{%- if client.slack is defined %}
config_jenkins_slack:
  jenkins_slack.config:
    - team_domain: {{ client.slack.team_domain }}
    - token: {{ client.slack.token }}
    - token_credential_id: {{ client.slack.get('token_credential_id','') }}
    - send_as: {{ client.slack.get('send_as','') }}
    - room: {{ client.slack.get('room', '') }}
{%- endif %}
