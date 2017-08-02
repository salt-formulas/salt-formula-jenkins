#!/usr/bin/env python

import json

def main():
    output = { "jenkins_plugins" : {} }

    list_plugin_groovy = """\
        pluginList = []
        Jenkins.instance.pluginManager.plugins.each{ pluginList << ("'${it.shortName}@${it.version}'")}
        print pluginList
    """
    call_result = __salt__['jenkins_common.call_groovy_script'](list_plugin_groovy, [])

    plugins = json.loads(call_result)

    for plugin in plugins:
        plugin_fields = plugin.split('@')
        output["jenkins_plugins"][plugin_fields[0]] = {"version": plugin_fields[1]}

    if output:
        return output
    else:
        return None
