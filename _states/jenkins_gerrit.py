import logging

logger = logging.getLogger(__name__)

def __virtual__():
    '''
    Only load if jenkins_common module exist.
    '''
    if 'jenkins_common.call_groovy_script' not in __salt__:
        return (
            False,
            'The jenkins_gerrit state module cannot be loaded: '
            'jenkins_common not found')
    return True


def present(name, hostname, username, frontendurl, auth_key_file, authkey,
            port="29418", auth_key_file_password=None, email="", proxy=""):
    """
    Jenkins gerrit-trigger state method

    :param name: server name
    :param host: server hostname
    :param username: username
    :param email: trigger email (optional)
    :param port: server ssh port
    :param proxy: proxy url (optional)
    :param frontendurl: server frontend URL
    :param auth_key_file: path to key file
    :param authkey: ssh key
    :param auth_key_file_password: password for keyfile (optional)
    :returns: salt-specified state dict
    """
    template = __salt__['jenkins_common.load_template'](
        'salt://jenkins/files/groovy/gerrit.template',
        __env__)
    return __salt__['jenkins_common.api_call'](name, template,
                        ["CREATED", "EXISTS"],
                        {
                            "name": name,
                            "hostname": hostname,
                            "port": port if port else "29418",
                            "proxy": proxy if proxy else "",
                            "username": username,
                            "email": email if email else "",
                            "frontendurl": frontendurl,
                            "auth_key_file": auth_key_file,
                            "authkey": authkey,
                            "auth_key_file_password": auth_key_file_password if auth_key_file_password else None
                        },
                        "Gerrit server")
