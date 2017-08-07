#!/usr/bin/env python

try:
    import jenkins
    HAS_JENKINS = True
except ImportError:
    HAS_JENKINS = False
import salt.config

def main():
    if not HAS_JENKINS:
        return {}

    output = { "jenkins_plugins" : {} }
    opts = salt.config.minion_config('/etc/salt/minion')
    user = opts['jenkins']['user']
    password = opts['jenkins']['password']
    url = opts['jenkins']['url']

    server = jenkins.Jenkins(url, username=user, password=password)
    plugins = server.get_plugins(depth=1)
    for plugin_name, plugin_dict in plugins.iteritems():
        output["jenkins_plugins"][plugin_name[0]] = {"version" : (plugin_dict["version"] or 0)}
    return output
