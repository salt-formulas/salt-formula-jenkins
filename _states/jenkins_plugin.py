import logging

logger = logging.getLogger(__name__)

install_plugin_groovy = """\
import jenkins.model.*
import java.util.logging.Logger

def logger = Logger.getLogger("")
def installed = false
def exists = false
def pluginName="${plugin}"
def instance = Jenkins.getInstance()
def pm = instance.getPluginManager()
def uc = instance.getUpdateCenter()
def needUpdateSites(maxOldInSec = 1800){
  long oldestTs = 0
  for (UpdateSite s : Jenkins.instance.updateCenter.siteList) {
    if(oldestTs == 0 || s.getDataTimestamp()<oldestTs){
       oldestTs = s.getDataTimestamp()
    }
  }
   return (System.currentTimeMillis()-oldestTs)/1000 > maxOldInSec
}

if (!pm.getPlugin(pluginName)) {
  if(needUpdateSites()) {
     uc.updateAllSites()
  }
  def plugin = uc.getPlugin(pluginName)
  if (plugin) {
    plugin.deploy()
    installed = true
  }
}else{
    exists = true
    print("EXISTS")
}
if (installed) {
  instance.save()
  if(${restart}){
      instance.doSafeRestart()
   }
  print("INSTALLED")
}else if(!exists){
  print("FAILED")
}
"""  # noqa

remove_plugin_groovy = """
import jenkins.model.*
import java.util.logging.Logger

def logger = Logger.getLogger("")
def installed = false
def initialized = false

def pluginName="${plugin}"
def instance = Jenkins.getInstance()
def pm = instance.getPluginManager()

def actPlugin = pm.getPlugin(pluginName)
if (!actPlugin) {
   def pluginToInstall = Jenkins.instance.updateCenter.getPlugin(pluginName)
   if(!pluginToInstall){
      print("FAILED")
   }else{
      print("NOT PRESENT")
   }
} else {
   actPlugin.disable()
   actPlugin.archive.delete()
   if({restart}){
      instance.doSafeRestart()
   }
   print("REMOVED")
}
"""  # noqa


def __virtual__():
    '''
    Only load if jenkins_common module exist.
    '''
    if 'jenkins_common.call_groovy_script' not in __salt__:
        return (
            False,
            'The jenkins_plugin state module cannot be loaded: '
            'jenkins_common not found')
    return True


def present(name, restart=False):
    """
    Jenkins plugin present state method, for installing plugins

    :param name: plugin name
    :param restart: do you want to restart jenkins after plugin install?
    :returns: salt-specified state dict
    """
    return _plugin_call(name, restart, install_plugin_groovy, [
                        "INSTALLED", "EXISTS"])


def absent(name, restart=False):
    """
    Jenkins plugin absent state method, for removing plugins

    :param name: plugin name
    :param restart: do you want to restart jenkins after plugin remove?
    :returns: salt-specified state dict
    """
    return _plugin_call(name, restart, remove_plugin_groovy, [
                        "REMOVED", "NOT PRESENT"])


def _plugin_call(name, restart, template, success_msgs):
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
        ret['comment'] = 'Jenkins plugin %s %s' % (name, status.lower())
    else:
        call_result = __salt__['jenkins_common.call_groovy_script'](
            template, {"plugin": name, "restart": "true" if restart else "false"})
        if call_result["code"] == 200 and call_result["msg"] in success_msgs:
            status = call_result["msg"]
            if status == success_msgs[0]:
                ret['changes'][name] = status
            ret['comment'] = 'Jenkins plugin %s %s%s' % (name, status.lower(
            ), ", jenkins restarted" if status == success_msgs[0] and restart else "")
            result = True
        else:
            status = 'FAILED'
            logger.error(
                "Jenkins plugin API call failure: %s", call_result["msg"])
            ret['comment'] = 'Jenkins plugin API call failure: %s' % (call_result[
                "msg"])
    ret['result'] = None if test else result
    return ret
