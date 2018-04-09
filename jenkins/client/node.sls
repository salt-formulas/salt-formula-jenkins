{% from "jenkins/map.jinja" import client with context %}
{% for name, node in client.get("node",{}).iteritems() %}
{% if node.get('name', name) == "master" %}
master_configuration:
  jenkins_node.setup_master:
    - num_executors: {{ node.get('num_executors','1') }}
    - node_mode: {{ node.get('node_mode','Normal') }}
    - labels: {{ node.get('labels',[]) }}
{% else %}
node_{{ name }}:
  jenkins_node.present:
    - name: {{ node.get('name', name) }}
    - desc:  {{ node.get('desc','') }}
    - remote_home: {{ node.remote_home }}
    - launcher: {{ node.launcher }}
    - num_executors: {{ node.get('num_executors','1') }}
    - node_mode: {{ node.get('node_mode','Normal') }}
    - ret_strategy: {{ node.get('ret_strategy','Always') }}
    - labels: {{ node.get('labels',[]) }}
{% endif %}
{%- endfor %}
{% for node_name, label in client.get("label",{}).iteritems() %}
label_for_{{ node_name }}:
  jenkins_node.label:
    - name: {{ node_name }}
    - lbl_text: {{ label.lbl_text }}
    - append: {{ label.get('append', False) }}
{% endfor %}
