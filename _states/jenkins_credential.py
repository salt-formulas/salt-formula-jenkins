import logging
logger = logging.getLogger(__name__)

create_credential_groovy = u"""\
import jenkins.*;
import jenkins.model.*;
import hudson.*;
import hudson.model.*;

import com.cloudbees.plugins.credentials.domains.Domain;
import com.cloudbees.plugins.credentials.CredentialsScope;

domain = Domain.global()
store = Jenkins.instance.getExtensionList(
  'com.cloudbees.plugins.credentials.SystemCredentialsProvider'
)[0].getStore()

credentials_new = new {clazz}(
  {params}
)

creds = com.cloudbees.plugins.credentials.CredentialsProvider.lookupCredentials(
      {clazz}.class, Jenkins.instance
);
updated = false;

for (credentials_current in creds) {{
  // Comparison does not compare passwords but identity.
  if (credentials_new == credentials_current) {{
    store.removeCredentials(domain, credentials_current);
    ret = store.addCredentials(domain, credentials_new)
    updated = true;
    println("OVERWRITTEN");
    break;
  }}
}}

if (!updated) {{
  ret = store.addCredentials(domain, credentials_new)
  if (ret) {{
    println("CREATED");
  }} else {{
    println("FAILED");
  }}
}}
"""  # noqa


def present(name, scope, username, password=None, desc="", key=None):
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
        ret['comment'] = 'Credentials ' + status.lower()
    else:
        clazz = ""
        if key:
            clazz = "com.cloudbees.jenkins.plugins.sshcredentials.impl.BasicSSHUserPrivateKey"
            params = 'CredentialsScope.{}, "{}", "{}", "{}"'.format(scope, name, desc, key)
        else:
            clazz = "com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl"
            params = 'CredentialsScope.{}, "{}", "{}", "{}", "{}"'.format(scope, name, desc, username, password)

        call_result = __salt__['jenkins_common.call_groovy_script'](create_credential_groovy, {"clazz": clazz, "params":params})
        if call_result["code"] == 200 and call_result["msg"].strip() in ["CREATED", "OVERWRITTEN"]:
            status = call_result["msg"]
            ret['changes'][name] = status
            ret['comment'] = 'Credentials ' + status.lower()
            result = True
        else:
            status = 'FAILED'
            logger.error("Jenkins credentials API call failure: %s", call_result["msg"])
            ret['comment'] = 'Jenkins credentials API call failure: %s' % (call_result["msg"])
    ret['result'] = None if test else result
    return ret
