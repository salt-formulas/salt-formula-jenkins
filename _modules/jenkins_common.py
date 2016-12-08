import bcrypt
import logging
import requests
from salt.exceptions import SaltInvocationError

logger = logging.getLogger(__name__)


def call_groovy_script(script, props):
    """
    Common method for call Jenkins groovy script API

    :param script groovy script template
    :param props groovy script properties
    :returns: HTTP dict {status,code,msg}
    """
    ret = {
        "status": "FAILED",
        "code": 999,
        "msg": ""
    }
    jenkins_url, jenkins_user, jenkins_password = get_jenkins_auth()
    if not jenkins_url:
        raise SaltInvocationError('No Jenkins URL found.')

    token_obj = get_api_crumb(jenkins_url, jenkins_user, jenkins_password)
    req_data = {"script": render_groovy_script(script, props)}
    if token_obj:
        req_data[token_obj["crumbRequestField"]] = token_obj["crumb"]

    logger.debug("Calling Jenkins script API with URL: %s", jenkins_url)
    req = requests.post('%s/scriptText' % jenkins_url,
                        auth=(jenkins_user, jenkins_password),
                        data=req_data)
    ret["code"] = req.status_code
    if req.status_code == 200:
        ret["status"] = "SUCCESS"
        ret["msg"] = req.text
        logger.debug("Jenkins script API call success: %s", ret)
    else:
        logger.error("Jenkins script API call failed. \
            Return code %s. Text: %s", req.status_code, req.text)
    return ret


def render_groovy_script(script, props):
    """
    Helper method for rendering groovy script with props

    :param script: groovy script template
    :param props: groovy script properties
    :returns: generated groovy script
    """
    return script.format(**props)


def get_api_crumb(jenkins_url=None, jenkins_user=None, jenkins_password=None):
    """
    Obtains Jenkins API crumb, if CSRF protection is enabled.
    Jenkins params can be given by params or not, if not,
    params will be get from salt.

    :param jenkins_url: Jenkins URL (optional)
    :param jenkins_user: Jenkins admin username (optional)
    :param jenkins_password: Jenkins admin password (optional)
    :returns: salt-specified state dict
    """
    if not jenkins_url:
        jenkins_url, jenkins_user, jenkins_password = get_jenkins_auth()
    logger.debug("Obtaining Jenkins API crumb for URL: %s", jenkins_url)
    tokenReq = requests.get("%s/crumbIssuer/api/json" % jenkins_url,
                            auth=(jenkins_user, jenkins_password) if jenkins_user else None)
    if tokenReq.status_code == 200:
        return tokenReq.json()
    elif tokenReq.status_code == 404:
        # 404 means CSRF security is disabled, so api crumb is not necessary
        return None
    else:
        raise Exception("Cannot obtain Jenkins API crumb. Status code: %s. Text: %s" %
                        (tokenReq.status_code, tokenReq.text))



def get_jenkins_auth():
    """
    Get jenkins params from salt
    """
    jenkins_url = __salt__['config.get']('jenkins.url') or \
        __salt__['config.get']('jenkins:url') or \
        __salt__['pillar.get']('jenkins.url')

    jenkins_user = __salt__['config.get']('jenkins.user') or \
        __salt__['config.get']('jenkins:user') or \
        __salt__['pillar.get']('jenkins.user')

    jenkins_password = __salt__['config.get']('jenkins.password') or \
        __salt__['config.get']('jenkins:password') or \
        __salt__['pillar.get']('jenkins.password')

    return (jenkins_url, jenkins_user, jenkins_password)


def encode_password(password):
    """
    Hash plaintext password by jenkins bcrypt algorithm
    :param password: plain-text password
    :returns: bcrypt hashed password
    """
    if isinstance(password, str):
        return bcrypt.hashpw(password, bcrypt.gensalt(prefix=b"2a"))
