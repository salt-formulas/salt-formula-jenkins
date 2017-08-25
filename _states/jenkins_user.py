import logging

logger = logging.getLogger(__name__)

create_admin_groovy = u"""\
import jenkins.model.*
import hudson.security.*
def instance = Jenkins.getInstance()
if(hudson.model.User.getAll().find{u->u.fullName.equals("${username}")}){
    print("EXISTS")
}else{
    def hudsonRealm = new HudsonPrivateSecurityRealm(false)
    def result=hudsonRealm.createAccount("${username}","${password}")
    instance.setSecurityRealm(hudsonRealm)
    def strategy = new hudson.security.FullControlOnceLoggedInAuthorizationStrategy()
    strategy.setAllowAnonymousRead(false)
    instance.setAuthorizationStrategy(strategy)
    instance.save()
    if(result.toString().equals("${username}")){
        print("SUCCESS")
    }else{
        print("FAILED")
    }
}
"""  # noqa


create_user_groovy = u"""\
if(hudson.model.User.getAll().find{u->u.fullName.equals("${username}")}){
    print("EXISTS")
}else{
    def result=jenkins.model.Jenkins.instance.securityRealm.createAccount("${username}", "${password}")
    if(result.toString().equals("${username}")){
        print("SUCCESS")
    }else{
        print("FAILED")
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
            'The jenkins_user state module cannot be loaded: '
            'jenkins_common not found')
    return True


def present(name, username, password, admin=False):
    """
    Main jenkins users state method

    :param username: user name
    :param password: user password
    :param admin:  is admin user flag (username will be always admin)
    :returns: salt-specified state dict
    """
    test = __opts__['test']  # noqa
    ret = {
        'name': username,
        'changes': {},
        'result': False,
        'comment': '',
    }

    result = False
    if test:
        status = 'CREATED'
        ret['changes'][username] = status
        ret['comment'] = 'User %s %s' % (username, status.lower())
    else:
        call_result = __salt__['jenkins_common.call_groovy_script'](
            create_admin_groovy if admin else create_user_groovy, {"username": username, "password": password})
        if call_result["code"] == 200 and call_result["msg"] in [
                "SUCCESS", "EXISTS"]:
            if call_result["msg"] == "SUCCESS":
                status = "CREATED" if not admin else "ADMIN CREATED"
                ret['changes'][username] = status
            else:
                status = "EXISTS"
            ret['comment'] = 'User %s %s' % (username, status.lower())
            result = True
        else:
            status = 'FAILED'
            logger.error("Jenkins user API call failure: %s",
                         call_result["msg"])
            ret['comment'] = 'Jenkins user API call failure: %s' % (call_result[
                                                                    "msg"])
    ret['result'] = None if test else result
    return ret
