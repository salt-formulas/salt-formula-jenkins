def __virtual__():
    '''
    Only load if jenkins_common module exist.
    '''
    if 'jenkins_common.call_groovy_script' not in __salt__:
        return (
            False,
            'The jenkins_node state module cannot be loaded: '
            'jenkins_common not found')
    return True


def label(name, lbl_text, append=False):
    """
    Jenkins node label state method

    :param name: node name
    :param lbl_text: label text
    :returns: salt-specified state dict
    """
    template = __salt__['jenkins_common.load_template'](
        'salt://jenkins/files/groovy/node_label.template',
        __env__)
    return __salt__['jenkins_common.api_call'](name, template,
                        ["CREATED", lbl_text],
                        {
                            'name': name,
                            'lbl_text': lbl_text,
                            'append': "true" if append else "false"
                        },
                        'Node Label')


def present(name, remote_home, launcher, num_executors="1",
            node_mode="Normal", desc="", labels=[], ret_strategy="Always"):
    """
    Jenkins node state method

    :param name: node name
    :param remote_home: node remote home path
    :param launcher: launcher dict with type, name, port, username, password
    :param num_executors: number of node executurs (optional, default 1)
    :param node_mode: node mode (optional, default Normal)
    :param desc: node description (optional)
    :param labels: node labels list (optional)
    :param ret_strategy: node retention strategy from RetentionStrategy class
    :returns: salt-specified state dict
    """
    template = __salt__['jenkins_common.load_template'](
        'salt://jenkins/files/groovy/node.template',
        __env__)

    label_string = " ".join(labels)
    launcher_string = "new hudson.slaves.JNLPLauncher()"
    tunnel_string = ""
    jvmopts_string = ""
    if "jvmopts" in launcher:
        jvmopts_string = launcher["jvmopts"]
    if launcher:
        if launcher["type"] == "ssh":
            launcher_string = 'new hudson.plugins.sshslaves.SSHLauncher("{}",{},"{}","{}","","{}","","","")'.format(
                launcher["host"], launcher["port"], launcher["username"],
                launcher["password"], jvmopts_string)
        elif launcher["type"] == "jnlp":
            if "tunnel" in launcher:
                tunnel_string = launcher["tunnel"]
            launcher_string = 'new hudson.slaves.JNLPLauncher("{}","{}")'.format(
                tunnel_string, jvmopts_string)

    return __salt__['jenkins_common.api_call'](name, template,
        ["CREATED", "EXISTS"],
        {
            "name": name,
            "desc": desc if desc else "",
            "label": label_string if label_string else "",
            "remote_home": remote_home if remote_home else "",
            "num_executors": num_executors if num_executors else "1",
            "launcher": launcher_string,
            "tunnel": tunnel_string,
            "jvmopts": jvmopts_string,
            "node_mode": node_mode.upper(),
            "ret_strategy": ret_strategy if ret_strategy else "Always"
        },
        'Node')

def setup_master(name, num_executors="1", node_mode="Normal", labels=[]):
    """
    Jenkins setup master state method

    :param name: node name (master)
    :param num_executors: number of executors (optional, default 1)
    :param node_mode: Node mode (Normal or Exclusive)
    :param labels: array of labels
    :returns: salt-specified state dict
    """
    template = __salt__['jenkins_common.load_template'](
        'salt://jenkins/files/groovy/master_node.template',
        __env__)
    return __salt__['jenkins_common.api_call'](name, template,
        ["CREATED", "EXISTS"],
        {
            'num_executors': num_executors,
            'labels': " ".join(labels),
            'node_mode': node_mode.upper()
        },
        'Master node configuration')

