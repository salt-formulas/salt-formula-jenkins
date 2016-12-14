import logging
logger = logging.getLogger(__name__)

create_admin_groovy = u"""\
import jenkins.model.*
import hudson.security.*
def instance = Jenkins.getInstance()
def hudsonRealm = new HudsonPrivateSecurityRealm(false)
def result=hudsonRealm.createAccount("{username}","{password}")
instance.setSecurityRealm(hudsonRealm)
def strategy = new hudson.security.FullControlOnceLoggedInAuthorizationStrategy()
strategy.setAllowAnonymousRead(false)
instance.setAuthorizationStrategy(strategy)
instance.save()
print(result)
"""  # noqa


create_user_groovy = u"""\
def result=jenkins.model.Jenkins.instance.securityRealm.createAccount("{username}", "{password}")
print(result)
"""  # noqa

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
        # try to call jenkins script api with given user and password to prove
        # his existence
        user_exists_result = __salt__['jenkins_common.call_groovy_script'](
            "print(\"TEST\")", {"username": username}, username, password,[200, 401])
        user_exists = user_exists_result and user_exists_result[
            "code"] == 200 and user_exists_result["msg"].count("TEST") == 1
        if not user_exists:
            call_result = __salt__['jenkins_common.call_groovy_script'](
                create_admin_groovy if admin else create_user_groovy, {"username": username, "password": password})
            if call_result["code"] == 200 and call_result["msg"].count(username) == 1:
                status = "CREATED" if not admin else "ADMIN CREATED"
                ret['changes'][username] = status
                ret['comment'] = 'User %s %s' % (username, status.lower())
                result = True
            else:
                status = 'FAILED'
                logger.error("Jenkins user API call failure: %s",
                             call_result["msg"])
                ret['comment'] = 'Jenkins user API call failure: %s' % (call_result[
                                                                        "msg"])
        else:
            status = "EXISTS"
            ret['comment'] = 'User %s %s' % (username, status.lower())
            result = True
    ret['result'] = None if test else result
    return ret
