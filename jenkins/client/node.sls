{% from "jenkins/map.jinja" import client with context %}
{% for name, node in client.get("node",{}).iteritems() %}
node_{{ name }}:
  jenkins_node.present:
    - name: {{ name }}
    - desc:  {{ node.get('desc','') }}
    - remote_home: {{ node.remote_home }}
    - launcher: {{ node.launcher }}
    - num_executors: {{ node.get('num_executors','1') }}
    - node_mode: {{ node.get('node_mode','Normal') }}
    - ret_strategy: {{ node.get('ret_strategy','Always') }}
    - label: {{ node.get('label','') }}
{% endfor %}

{% for node_name, label in client.get("label",{}).iteritems() %}
label_for_{{ node_name }}:
  jenkins_node.label:
    - name: {{ node_name }}
    - lbl_text: {{ label.lbl_text }}
    - append: {{ label.get('append', False) }}
{% endfor %}