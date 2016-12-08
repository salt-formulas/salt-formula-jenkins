{% from "jenkins/map.jinja" import client with context %}

{% for name, user in client.get('user',{}).iteritems() %}
user_{{ name }}:
  jenkins_user.present:
  - username: {{ name }}
  - password: {{ user.password }}
  - admin: {{ user.get('admin', False) }}
{% endfor %}