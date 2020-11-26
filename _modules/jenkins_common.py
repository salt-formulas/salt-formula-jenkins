import logging

from salt.exceptions import SaltInvocationError
from string import Template

try:
    import bcrypt
    HAS_BCRYPT = True
except ImportError:
    HAS_BCRYPT = False

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

logger = logging.getLogger(__name__)


def __virtual__():
    '''
    Only load if bcrypt and requests libraries exist.
    '''
    if not HAS_BCRYPT:
        return (
            False,
            'Can not load module jenkins_common: bcrypt library not found')
    if not HAS_REQUESTS:
        return (
            False,
            'Can not load module jenkins_common: requests library not found')
    return True


def call_groovy_script(script, props, username=None,
                       password=None, success_status_codes=[200]):
    """
    Common method for call Jenkins groovy script API

    :param script: groovy script template
    :param props: groovy script properties
    :param username: jenkins username (optional,
            if missing creds from sall will be used)
    :param password: jenkins password (optional,
            if missing creds from sall will be used)
    :param success_status_codes: success response status code
            (optional) in some cases we want to declare error call as success
    :returns: HTTP dict {status,code,msg}
    """
    ret = {
        "status": "FAILED",
        "code": 999,
        "msg": ""
    }
    jenkins_url, jenkins_user, jenkins_password = get_jenkins_auth()
    if username:
        jenkins_user = username
    if password:
        jenkins_password = password

    if not jenkins_url:
        raise SaltInvocationError('No Jenkins URL found.')

    token_obj = get_api_crumb(jenkins_url, jenkins_user, jenkins_password)
    req_data = {"script": render_groovy_script(script, props)}
    headers = {}
    if token_obj:
        headers[token_obj["crumbRequestField"]] = token_obj["crumb"]

    logger.debug("Calling Jenkins script API with URL: %s", jenkins_url)
    req = requests.post('%s/scriptText' % jenkins_url,
                        auth=(jenkins_user, jenkins_password) if jenkins_user else None,
                        data=req_data, headers=headers)
    ret["code"] = req.status_code
    ret["msg"] = req.text
    if req.status_code in success_status_codes:
        ret["status"] = "SUCCESS"
        logger.debug("Jenkins script API call success: %s", ret)
    else:
        logger.error("Jenkins script API call failed. \
            Return code %s. Text: %s", req.status_code, req.text)
    return ret


def render_groovy_script(script_template, props):
    """
    Helper method for rendering groovy script with props

    :param script_template: groovy script template
    :param props: groovy script properties
    :returns: generated groovy script
    """
    template = Template(script_template)
    return template.safe_substitute(props)


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
        logger.debug("Got Jenkins API crumb: %s", tokenReq.json())
        return tokenReq.json()
    elif tokenReq.status_code in [404, 401, 502, 503]:
        # 404 means CSRF security is disabled, so api crumb is not necessary,
        # 401 means unauthorized
        # 50x means jenkins is unavailabe - fail in call_groovy_script, but
        #     not here, to handle exception in state
        logger.debug("Got error %s: %s", str(tokenReq.status_code), tokenReq.reason)
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
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(prefix=b"2a"))

def load_template(salt_url, env):
    """
       Return content of file `salt_url`
    """

    template_path = __salt__['cp.cache_file'](salt_url, env)
    with open(template_path, 'r') as template_file:
        template = template_file.read()

    return template

def api_call(name, template, success_msgs, params, display_name):
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
        ret['comment'] = '%s "%s" %s' % (display_name, name, status.lower())
    else:
        call_result = call_groovy_script(template, params)
        if call_result["code"] == 200 and call_result["msg"].strip() in success_msgs:
            status = call_result["msg"]
            if status == success_msgs[0]:
                ret['changes'][name] = status
            ret['comment'] = '%s "%s" %s' % (display_name, name, status.lower())
            result = True
        else:
            status = 'FAILED'
            logger.error(
                'Jenkins API call failure: %s', call_result["msg"])
            ret['comment'] = 'Jenkins API call failure: %s' % (call_result[
                "msg"])
    ret['result'] = None if test else result
    return ret
