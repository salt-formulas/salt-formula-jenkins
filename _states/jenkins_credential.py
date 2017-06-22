import logging
logger = logging.getLogger(__name__)

create_credential_groovy = u"""\
import com.cloudbees.plugins.credentials.domains.Domain;
import com.cloudbees.plugins.credentials.CredentialsScope;

def creds = com.cloudbees.plugins.credentials.CredentialsProvider.lookupCredentials(
        com.cloudbees.plugins.credentials.common.StandardUsernameCredentials.class,
        Jenkins.instance
    )
def key = \"\"\"{key}
\"\"\"

def result = creds.find{{
  (it instanceof com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl &&
    it.username == "{username}" &&
    it.id == "{name}" &&
    it.description == "{desc}" &&
    it.password.toString() == "{password}") ||
  (it instanceof com.cloudbees.jenkins.plugins.sshcredentials.impl.BasicSSHUserPrivateKey &&
    it.username == "{username}" &&
    it.id == "{name}" &&
    ("{password}" == "" || it.passphrase.toString() == "{password}") &&
    it.description == "{desc}" &&
    it.privateKeySource.privateKey.equals(key.trim()))
}}

if(result){{
    print("EXISTS")
}}else{{
    domain = Domain.global()
    store = Jenkins.instance.getExtensionList(
      'com.cloudbees.plugins.credentials.SystemCredentialsProvider'
    )[0].getStore()

    credentials_new = new {clazz}(
      {params}
    )
    // remove credentails with same if before created new one, if exists
    def existingCreds = com.cloudbees.plugins.credentials.CredentialsProvider.lookupCredentials(
        com.cloudbees.plugins.credentials.common.StandardUsernameCredentials.class,
        Jenkins.instance).find{{it -> it.id.equals("{name}")}}
    if(existingCreds){{
        store.removeCredentials(domain, existingCreds)
    }}
    ret = store.addCredentials(domain, credentials_new)
    if (ret) {{
      print("CREATED");
    }} else {{
        print("FAILED");
    }}
}}
"""  # noqa


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


def present(name, scope, username, password="", desc="", key=None):
    """
    Main jenkins credentials state method

    :param name: credential name
    :param scope: credential scope
    :param username: username
    :param password: password (optional)
    :param desc: credential description (optional)
    :param key: credential key (optional)
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
        status = 'CREATED'
        ret['changes'][name] = status
        ret['comment'] = 'Credentials %s %s' % (name, status.lower())
    else:
        clazz = ""
        if key:
            clazz = "com.cloudbees.jenkins.plugins.sshcredentials.impl.BasicSSHUserPrivateKey"
            params = 'CredentialsScope.{}, "{}", "{}", new com.cloudbees.jenkins.plugins.sshcredentials.impl.BasicSSHUserPrivateKey.DirectEntryPrivateKeySource(key.trim()), "{}", "{}"'.format(
                scope, name, username, password if password else "", desc if desc else "")
        else:
            clazz = "com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl"
            params = 'CredentialsScope.{}, "{}", "{}", "{}", "{}"'.format(
                scope, name, desc if desc else "", username, password)

        call_result = __salt__['jenkins_common.call_groovy_script'](
            create_credential_groovy, {"name": name, "username": username, "password": password if password else "", "clazz": clazz, "params": params, "key": key if key else "", "desc": desc if desc else ""})
        if call_result["code"] == 200 and call_result["msg"] in ["CREATED", "EXISTS"]:
            status = call_result["msg"]
            if call_result["msg"] == "CREATED":
                ret['changes'][name] = status
            ret['comment'] = 'Credentials %s %s' % (name, status.lower())
            result = True
        else:
            status = 'FAILED'
            logger.error(
                "Jenkins credentials API call failure: %s", call_result["msg"])
            ret['comment'] = 'Jenkins credentials API call failure: %s' % (call_result[
                                                                           "msg"])
    ret['result'] = None if test else result
    return ret
