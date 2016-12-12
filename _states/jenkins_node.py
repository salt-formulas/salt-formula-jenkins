import logging
logger = logging.getLogger(__name__)


create_node_groovy = u"""\
import jenkins.model.*
import hudson.model.*
import hudson.slaves.*
import hudson.plugins.sshslaves.*
import java.util.ArrayList;
import hudson.slaves.EnvironmentVariablesNodeProperty.Entry;

  Slave slave = new DumbSlave(
                    "{name}",
                    "{desc}",
                    "{remote_home}",
                    "{num_executors}",
                    Node.Mode.{node_mode},
                    "{label}",
                    {launcher},
                    new RetentionStrategy.{ret_strategy}(),
                    new LinkedList())
  Jenkins.instance.addNode(slave)
  print "{name}"
"""  # noqa

create_lbl_groovy = u"""\
hudson = hudson.model.Hudson.instance
updated = false
hudson.slaves.find {{ slave -> slave.nodeName.equals("{name}")
  if({append}){{
    slave.labelString = slave.labelString + " " + "{lbl_text}"
  }}else{{
    slave.labelString = "{lbl_text}"
  }}
  updated = true
  print "{lbl_text}"
}}
if(!updated){{
    print "FAILED"
}}
hudson.save()
"""  # noqa


def label(name, lbl_text, append=False):
    """
    Jenkins node label state method

    :param name: node name
    :param lbl_text: label text
    :returns: salt-specified state dict
    """
    test = __opts__['test']  # noqa
    ret = {
        'name': name,
        'changes': {},
        'result': False,
        'comment': '',
    }
    result = False
    if test:
        status = 'CREATED'
        ret['changes'][name] = status
        ret['comment'] = 'Label %s %s' % (name, status.lower())
    else:
        call_result = __salt__['jenkins_common.call_groovy_script'](
            create_lbl_groovy, {'name': name, 'lbl_text': lbl_text, 'append': "true" if append else "false"})
        if call_result["code"] == 200 and call_result["msg"].strip() == lbl_text:
            status = "CREATED"
            ret['changes'][name] = status
            ret['comment'] = 'Label %s %s ' % (name, status.lower())
            result = True
        else:
            status = 'FAILED'
            logger.error(
                "Jenkins label API call failure: %s", call_result["msg"])
            ret['comment'] = 'Jenkins label API call failure: %s' % (
                call_result["msg"])
    ret['result'] = None if test else result
    return ret


def present(name, remote_home, launcher, num_executors="1", node_mode="Normal", desc="", label="", ret_strategy="Always"):
    """
    Jenkins node state method

    :param name: node name
    :param remote_home: node remote home path
    :param launcher: launcher dict with type, name, port, username, password
    :param num_executors: number of node executurs (optional, default 1)
    :param node_mode: node mode (optional, default Normal)
    :param ret_strategy: node retention strategy from RetentionStrategy class
    :returns: salt-specified state dict
    """
    test = __opts__['test']  # noqa
    ret = {
        'name': name,
        'changes': {},
        'result': False,
        'comment': '',
    }
    result = False
    if test:
        status = 'CREATED'
        ret['changes'][name] = status
        ret['comment'] = 'Node %s %s' % (name, status.lower())
    else:
        launcher_string = "new JNLPLauncher()"
        if launcher:
            if launcher["type"] == "ssh":
                launcher_string = 'new SSHLauncher("{}",{},"{}","{}","","","","","")'.format(
                    launcher["host"], launcher["port"], launcher["username"], launcher["password"])
            elif launcher["type"] == "jnlp":
                launcher_string = "new JNLPLauncher()"

        call_result = __salt__['jenkins_common.call_groovy_script'](
            create_node_groovy,
            {"name": name,
                "desc": desc,
                "label": label,
                "remote_home": remote_home,
                "num_executors": num_executors,
                "launcher": launcher_string,
                "node_mode": node_mode.upper(),
                "ret_strategy": ret_strategy})
        if call_result["code"] == 200 and call_result["msg"].strip() == name:
            status = "CREATED"
            ret['changes'][name] = status
            ret['comment'] = 'Node %s %s' % (name, status.lower())
            result = True
        else:
            status = 'FAILED'
            logger.error(
                "Jenkins node API call failure: %s", call_result["msg"])
            ret['comment'] = 'Jenkins node API call failure: %s' % (
                call_result["msg"])
    ret['result'] = None if test else result
    return ret
