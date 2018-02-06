import logging

logger = logging.getLogger(__name__)

def __virtual__():
    '''
    Only load if jenkins_common module exist.
    '''
    if 'jenkins_common.call_groovy_script' not in __salt__:
        return (
            False,
            'The jenkins_credentials state module cannot be loaded: '
            'jenkins_common not found')
    return True


def present(name, scope, username, password="", desc="", key=None, secret=None, filename=None, content=None):
    """
    Main jenkins credentials state method

    :param name: credential name
    :param scope: credential scope
    :param username: username (optional)
    :param password: password (optional)
    :param desc: credential description (optional)
    :param key: credential key (optional)
    :param filename: file name for file credential (optional)
    :param content: file content for file credential (optional)
    :returns: salt-specified state dict
    """
    template = __salt__['jenkins_common.load_template'](
         'salt://jenkins/files/groovy/credential.template',
         __env__)
    clazz = ""
    if key:
        clazz = "com.cloudbees.jenkins.plugins.sshcredentials.impl.BasicSSHUserPrivateKey"
        params = 'CredentialsScope.{}, "{}", "{}", new com.cloudbees.jenkins.plugins.sshcredentials.impl.BasicSSHUserPrivateKey.DirectEntryPrivateKeySource(key.trim()), "{}", "{}"'.format(
            scope, name, username, password if password else "", desc if desc else "")
    elif secret:
        clazz = "org.jenkinsci.plugins.plaincredentials.impl.StringCredentialsImpl"
        params = 'CredentialsScope.{}, "{}", "{}"'.format(
            scope, name, desc if desc else "")
    elif filename:
        clazz = "org.jenkinsci.plugins.plaincredentials.impl.FileCredentialsImpl"
        params = 'CredentialsScope.{}, "{}", "{}", "{}", SecretBytes.fromBytes("""{}""".getBytes())'.format(
            scope, name, desc if desc else "", filename, content.encode('unicode_escape'))
    else:
        clazz = "com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl"
        params = 'CredentialsScope.{}, "{}", "{}", "{}", "{}"'.format(
            scope, name, desc if desc else "", username, password)
    return __salt__['jenkins_common.api_call'](name, template,
                    ["CREATED", "EXISTS"],
                    {
                        "scope": scope,
                        "name": name,
                        "username": username if username else "",
                        "password": password if password else "",
                        "clazz": clazz,
                        "params": params,
                        "key": key if key else "",
                        "desc": desc if desc else "",
                        "secret": secret if secret else "",
                        "fileName": filename if filename else "",
                        "content": content.encode('unicode_escape') if content else ""
                    },
                    "Credentials")
