{% from "jenkins/map.jinja" import client with context %}
{% for approval in client.get("approved_scripts",[]) %}
  approve_jenkins_signature_{{ approval }}:
    jenkins_approval.approved:
      - name: {{ approval }}
      - require:
        - sls: jenkins.client.plugin
{% endfor %}
