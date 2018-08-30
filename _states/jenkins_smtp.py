import logging
import json

logger = logging.getLogger(__name__)

def __virtual__():
    '''
    Only load if jenkins_common module exist.
    '''
    if 'jenkins_common.call_groovy_script' not in __salt__:
        return (
            False,
            'The jenkins_smtp state module cannot be loaded: '
            'jenkins_common not found')
    return True


def config(name, host, username, password, reply_to=None,
           port=25, ssl=False, charset="UTF-8"):
    """
    Jenkins SMTP server config state method

    :param name: configuration name
    :param host: SMTP host
    :param username: SMTP username
    :param password: SMTP password
    :param reply_to: sent emails ReplyTo header (optional)
    :param port: SMTP port (optional, default 25)
    :param ssl: use SSL for SMTP (optional, default False)
    :param charset: SMTP charset (optional, default UTF-8)
    :returns: salt-specified state dict
    """

    template = __salt__['jenkins_common.load_template'](
        'salt://jenkins/files/groovy/smtp.template',
        __env__)

    return __salt__['jenkins_common.api_call'](name, template,
                        ['CHANGED', 'EXISTS'],
                        {'params': json.dumps({
                            'username': username,
                            'password': password,
                            'host': host,
                            'useReplyTo': True if reply_to else False,
                            'replyTo': reply_to,
                            'port': port if port else 25,
                            'ssl': True if ssl else False,
                            'charset': charset if charset else 'UTF-8'
                            })
                        },
                        'SMTP config')


def admin_email(name, email):
    """
    Jenkins Admin user email config state method

    :param name: jenkins admin email
    :returns: salt-specified state dict
    """

    template = __salt__['jenkins_common.load_template'](
        'salt://jenkins/files/groovy/admin_email.template',
        __env__)

    return __salt__['jenkins_common.api_call'](name, template,
                        ['CHANGED', 'EXISTS'],
                        {'email': email},
                        'Admin email config')
