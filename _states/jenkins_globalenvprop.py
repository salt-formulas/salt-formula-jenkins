import logging

logger = logging.getLogger(__name__)

add_prop_groovy = """\
instance = Jenkins.getInstance()
globalNodeProperties = instance.getGlobalNodeProperties()
envVarsNodePropertyList = globalNodeProperties.getAll(hudson.slaves.EnvironmentVariablesNodeProperty.class)

newEnvVarsNodeProperty = null
envVars = null

if ( envVarsNodePropertyList == null || envVarsNodePropertyList.size() == 0 ) {
  newEnvVarsNodeProperty = new hudson.slaves.EnvironmentVariablesNodeProperty();
  globalNodeProperties.add(newEnvVarsNodeProperty)
  envVars = newEnvVarsNodeProperty.getEnvVars()
} else {
  envVars = envVarsNodePropertyList.get(0).getEnvVars()
}
if(!envVars.containsKey("${key}") || !envVars.get("${key}").equals("${value}")){
  envVars.put("${key}", "${value}")
  instance.save()
  print("ADDED/CHANGED")
}else{
  print("EXISTS")
}
"""  # noqa

remove_prop_groovy = """\
instance = Jenkins.getInstance()
globalNodeProperties = instance.getGlobalNodeProperties()
envVarsNodePropertyList = globalNodeProperties.getAll(hudson.slaves.EnvironmentVariablesNodeProperty.class)

newEnvVarsNodeProperty = null
envVars = null

if ( envVarsNodePropertyList == null || envVarsNodePropertyList.size() == 0 ) {
  print("NOT PRESENT")
} else {
  envVars = envVarsNodePropertyList.get(0).getEnvVars()
  if(envVars.containsKey("${key}"){
    envVars.remove("${key}")
    print("REMOVED")
    instance.save()
  }else{
    print("NOT PRESENT")
  }
}
"""  # noqa


def __virtual__():
    '''
    Only load if jenkins_common module exist.
    '''
    if 'jenkins_common.call_groovy_script' not in __salt__:
        return (
            False,
            'The jenkins_globalenvprop state module cannot be loaded: '
            'jenkins_common not found')
    return True


def present(name, value, **kwargs):
    """
    Jenkins global env property present state method

    :param name: global env property name
    :param value: env property velue
    :returns: salt-specified state dict
    """
    return _plugin_call(name, value, add_prop_groovy, [
                        "ADDED/CHANGED", "EXISTS"], **kwargs)


def absent(name, **kwargs):
    """
    Jenkins global env property absent state method

    :param name: global env property name
    :returns: salt-specified state dict
    """
    return _plugin_call(name, None, remove_prop_groovy, [
                        "REMOVED", "NOT PRESENT"], **kwargs)


def _plugin_call(name, value, template, success_msgs, **kwargs):
    test = __opts__['test']  # noqa
    ret = {
        'name': name,
        'changes': {},
        'result': False,
        'comment': '',
    }
    result = False
    if test:
        status = success_msgs[0]
        ret['changes'][name] = status
        ret['comment'] = 'Jenkins global enviroment property %s %s' % (name, status.lower())
    else:
        call_result = __salt__['jenkins_common.call_groovy_script'](
            template, {"key": name, "value": value})
        if call_result["code"] == 200 and call_result["msg"] in success_msgs:
            status = call_result["msg"]
            if status == success_msgs[0]:
                ret['changes'][name] = status
            ret['comment'] = 'Jenkins global enviroment property %s %s' % (name, status.lower())
            result = True
        else:
            status = 'FAILED'
            logger.error(
                "Jenkins global enviroment property API call failure: %s", call_result["msg"])
            ret['comment'] = 'Jenkins global enviroment property API call failure: %s' % (call_result[
                "msg"])
    ret['result'] = None if test else result
    return ret
