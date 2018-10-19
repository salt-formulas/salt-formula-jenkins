{#- It's not recommended to call this state explicitly as it requires plugins #}
{% from "jenkins/map.jinja" import client with context %}
{% for approval in client.get("approved_scripts",[]) %}
  approve_jenkins_signature_{{ approval }}:
    jenkins_approval.approved:
      - name: {{ approval }}
{% endfor %}