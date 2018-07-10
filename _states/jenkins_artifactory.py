import logging

logger = logging.getLogger(__name__)

add_artifactory_groovy = u"""\
import jenkins.model.*
import org.jfrog.*
import org.jfrog.hudson.*
def inst = Jenkins.getInstance()
def desc = inst.getDescriptor("org.jfrog.hudson.ArtifactoryBuilder")
if (! desc.useCredentialsPlugin ) {
    desc.useCredentialsPlugin = true
}
// empty artifactory servers is not empty list but null, but find can be called on null
def server =  desc.getArtifactoryServers().find{it -> it.name.equals("${name}")}
if(server &&
   server.getName().equals("${name}") &&
   server.getUrl().equals("${serverUrl}") &&
   (server.getDeployerCredentialsConfig() == null || server.getDeployerCredentialsConfig().getCredentialsId().equals("${credentialsId}")) &&
   (server.getResolverCredentialsConfig() == null || server.getResolverCredentialsConfig().getCredentialsId().equals("${credentialsId}"))){
        print("EXISTS")
}else{
    // we must care about null here
    if(desc.getArtifactoryServers() != null && !desc.getArtifactoryServers().isEmpty()){
        desc.getArtifactoryServers().removeIf{it -> it.name.equals("${name}")}
    }else{
        desc.setArtifactoryServers([])
    }
    def newServer = new ArtifactoryServer(
      "${name}",
      "${serverUrl}",
      new CredentialsConfig("", "", "${credentialsId}"),
      new CredentialsConfig("", "", "${credentialsId}"),
      300,
      false,
      null)
    desc.getArtifactoryServers().add(newServer)
    desc.save()
    print("ADDED/CHANGED")
}
"""  # noqa

delete_artifactory_groovy = u"""\
def inst = Jenkins.getInstance()
def desc = inst.getDescriptor("org.jfrog.hudson.ArtifactoryBuilder")
if(desc.getArtifactoryServers().removeIf{it -> it.name.equals("${name}")}){
    print("REMOVED")
}else{
    print("NOT PRESENT")
}
"""  # noqa


def __virtual__():
    '''
    Only load if jenkins_common module exist.
    '''
    if 'jenkins_common.call_groovy_script' not in __salt__:
        return (
            False,
            'The jenkins_artifactory state module cannot be loaded: '
            'jenkins_common not found')
    return True


def present(name, url, credential_id, **kwargs):
    """
    Jenkins artifactory present state method

    :param name: artifactory server name
    :param url: artifactory server url
    :param credential_id: artifactory server credential id
    :returns: salt-specified state dict
    """
    return _plugin_call(name, url, credential_id, add_artifactory_groovy, [
                        "ADDED/CHANGED", "EXISTS"], **kwargs)


def absent(name, **kwargs):
    """
    Jenkins artifactory present state method

    :param name: artifactory server name
    :returns: salt-specified state dict
    """
    return _plugin_call(name, None, None, delete_artifactory_groovy, [
                        "REMOVED", "NOT PRESENT"], **kwargs)


def _plugin_call(name, url, credentialsId, template, success_msgs, **kwargs):
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
        ret['comment'] = 'Jenkins artifactory server %s %s' % (
            name, status.lower())
    else:
        call_result = __salt__['jenkins_common.call_groovy_script'](
            template, {"name": name, "serverUrl": url, "credentialsId": credentialsId})
        if call_result["code"] == 200 and call_result["msg"] in success_msgs:
            status = call_result["msg"]
            if status == success_msgs[0]:
                ret['changes'][name] = status
            ret['comment'] = 'Jenkins artifactory server %s %s' % (
                name, status.lower())
            result = True
        else:
            status = 'FAILED'
            logger.error(
                "Jenkins artifactory API call failure: %s", call_result["msg"])
            ret['comment'] = 'Jenkins artifactory API call failure: %s' % (call_result[
                "msg"])
    ret['result'] = None if test else result
    return ret
