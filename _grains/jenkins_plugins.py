#!/usr/bin/env python

import jenkins
import salt.config

def main():
    output = { "jenkins_plugins" : {} }
    opts = salt.config.minion_config('/etc/salt/minion')
    user = opts['jenkins']['user']
    password = opts['jenkins']['password']
    url = opts['jenkins']['url']

    server = jenkins.Jenkins(url, username=user, password=password)
    plugins = server.get_plugins(depth=1)
    for plugin_name, plugin_dict in plugins.iteritems():
        output["jenkins_plugins"][plugin_name[0]] = {"version" : (plugin_dict["backupVersion"] or 0)}
    return output
