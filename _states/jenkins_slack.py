import logging

logger = logging.getLogger(__name__)

config_slack_groovy = """\
jenkins = jenkins.model.Jenkins.getInstance()
try{
slack = jenkins.getDescriptorByType(jenkins.plugins.slack.SlackNotifier.DescriptorImpl)
if(slack.teamDomain.equals("${team_domain}") &&
   slack.token.equals("${token}") &&
   slack.tokenCredentialId.equals("${token_credential_id}") &&
   slack.room.equals("${room}") &&
   slack.sendAs.equals("${send_as}")){
        print("EXISTS")
}else{
    slack.teamDomain = "${team_domain}"
    slack.token = "${token}"
    slack.tokenCredentialId = "${token_credential_id}"
    slack.room = "${room}"
    slack.sendAs = "${send_as}"
    slack.save()
    print("SUCCESS")
}
}catch(all){
    print("Cannot instantiate Jenkins Slack plugin, maybe plugin is not installed")
}
"""  # noqa


def __virtual__():
    '''
    Only load if jenkins_common module exist.
    '''
    if 'jenkins_common.call_groovy_script' not in __salt__:
        return (
            False,
            'The jenkins_slack state module cannot be loaded: '
            'jenkins_common not found')
    return True


def config(name, team_domain, token,
           token_credential_id="", room="", send_as=None):
    """
    Jenkins Slack config state method

    :param name: configuration name
    :param team_domain: slack team domain
    :param token: slack token
    :param token_credential_id: slack token credential id
    :param room: slack room
    :param send_as: slack send as param
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
        status = "SUCCESS"
        ret['changes'][name] = status
        ret['comment'] = 'Jenkins Slack config %s %s' % (name, status.lower())
    else:
        call_result = __salt__['jenkins_common.call_groovy_script'](
            config_slack_groovy, {"team_domain": team_domain,
                                  "token": token,
                                  "token_credential_id": token_credential_id if token_credential_id else "",
                                  "room": room if room else "",
                                  "send_as": send_as if send_as else ""})
        if call_result["code"] == 200 and call_result["msg"] in [
                "SUCCESS", "EXISTS"]:
            status = call_result["msg"]
            if status == "SUCCESS":
                ret['changes'][name] = status
            ret['comment'] = 'Jenkins Slack config %s %s' % (
                name, status.lower())
            result = True
        else:
            status = 'FAILED'
            logger.error(
                "Jenkins slack API call failure: %s", call_result["msg"])
            ret['comment'] = 'Jenkins slack API call failure: %s' % (call_result[
                "msg"])
    ret['result'] = None if test else result
    return ret
