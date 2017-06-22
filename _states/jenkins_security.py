import logging
logger = logging.getLogger(__name__)

set_ldap_groovy = """\
import jenkins.model.*
import hudson.security.*
import org.jenkinsci.plugins.*

def server = 'ldap://{server}'
def rootDN = '{rootDN}'
def userSearchBase = '{userSearchBase}'
def userSearch = '{userSearch}'
def groupSearchBase = '{groupSearchBase}'
def managerDN = '{managerDN}'
def managerPassword = '{managerPassword}'
boolean inhibitInferRootDN = {inhibitInferRootDN}

try{{
ldapRealm = Class.forName("hudson.security.LDAPSecurityRealm").getConstructor(String.class, String.class, String.class, String.class, String.class, String.class, String.class, Boolean.TYPE)
.newInstance(server, rootDN, userSearchBase, userSearch, groupSearchBase, managerDN, managerPassword, inhibitInferRootDN) 
Jenkins.instance.setSecurityRealm(ldapRealm)
Jenkins.instance.save()
print("SUCCESS")
}}catch(ClassNotFoundException e){{
    print("Cannot instantiate LDAPSecurityRealm, maybe ldap plugin not installed")
}}
"""  # noqa

set_matrix_groovy = """\
import jenkins.model.*
import hudson.security.*
import com.cloudbees.plugins.credentials.*

def instance = Jenkins.getInstance()
try{{
def strategy = Class.forName("hudson.security.{matrix_class}").newInstance()
{strategies}
instance.setAuthorizationStrategy(strategy)
instance.save()
print("SUCCESS")
}}catch(ClassNotFoundException e){{
    print("Cannot instantiate {matrix_class}, maybe auth-matrix plugin not installed")
}}
"""  # noqa


def __virtual__():
    '''
    Only load if jenkins_common module exist.
    '''
    if 'jenkins_common.call_groovy_script' not in __salt__:
        return (
            False,
            'The jenkins_security state module cannot be loaded: '
            'jenkins_common not found')
    return True


def ldap(name, server, root_dn, user_search_base, manager_dn, manager_password, user_search="", group_search_base="", inhibit_infer_root_dn=False):
    """
    Jenkins ldap state method

    :param name: ldap state name
    :param server: ldap server host (without ldap://)
    :param root_dn: root domain names
    :param user_search_base:
    :param manager_dn:
    :param manager_password:
    :param user_search: optional, default empty string
    :param group_search_base: optional, default empty string
    :param inhibit_infer_root_dn: optional, default false
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
        ret['comment'] = 'LDAP setup %s %s' % (name, status.lower())
    else:
        call_result = __salt__['jenkins_common.call_groovy_script'](
            set_ldap_groovy, {"name": name, "server": server, "rootDN": root_dn,
                              "userSearchBase": user_search_base if user_search_base else "",
                              "managerDN": manager_dn if manager_dn else "",
                              "managerPassword": manager_password if manager_password else "",
                              "userSearch": user_search if user_search else "",
                              "groupSearchBase": group_search_base if group_search_base else "", 
                              "inhibitInferRootDN": "true" if inhibit_infer_root_dn else "false"})
        if call_result["code"] == 200 and call_result["msg"] == "SUCCESS":
            status = call_result["msg"]
            ret['changes'][name] = status
            ret['comment'] = 'Jenkins LDAP setting %s %s' % (
                name, status.lower())
            result = True
        else:
            status = 'FAILED'
            logger.error(
                "Jenkins security API call failure: %s", call_result["msg"])
            ret['comment'] = 'Jenkins security API call failure: %s' % (call_result[
                "msg"])
    ret['result'] = None if test else result
    return ret


def matrix(name, strategies, project_based=False):
    """
    Jenkins matrix security state method

    :param name: ldap state name
    :param strategies: dict with matrix strategies
    :param procect_based: flag if we configuring
        GlobalMatrix security or ProjectMatrix security
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
        ret['comment'] = 'LDAP setup %s %s' % (name, status.lower())
    else:
        call_result = __salt__['jenkins_common.call_groovy_script'](
            set_matrix_groovy, {"strategies": _build_strategies(strategies),
                                "matrix_class": "ProjectMatrixAuthorizationStrategy" if project_based else "GlobalMatrixAuthorizationStrategy"})
        if call_result["code"] == 200 and call_result["msg"] == "SUCCESS":
            status = call_result["msg"]
            ret['changes'][name] = status
            ret['comment'] = 'Jenkins Matrix security setting %s %s' % (
                name, status.lower())
            result = True
        else:
            status = 'FAILED'
            logger.error(
                "Jenkins security API call failure: %s", call_result["msg"])
            ret['comment'] = 'Jenkins security API call failure: %s' % (call_result[
                "msg"])
    ret['result'] = None if test else result
    return ret


def _build_strategies(permissions):
    strategies_str = ""
    for strategy in _to_strategies_list("strategy.add({},\"{}\")", _to_one_dict(permissions, "")):
        strategies_str += "{}\n".format(strategy)
    return strategies_str


def _to_strategies_list(strategy_format, strategy_dict):
    res = []
    for key, value in strategy_dict.items():
        if isinstance(value, list):
            for user in value:
                res.append(strategy_format.format(key, user))
        else:
            res.append(strategy_format.format(key, value))
    return res


def _to_one_dict(input_dict, input_key):
    res = {}
    for key, value in input_dict.items():
        new_key = key if input_key == "" else "{}.{}".format(input_key, key)
        if isinstance(value, dict):
            res.update(_to_one_dict(value, new_key))
        else:
            res[new_key] = value
    return res
