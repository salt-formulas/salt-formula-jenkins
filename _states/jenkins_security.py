import logging

logger = logging.getLogger(__name__)

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


def ldap(name, server, root_dn, user_search_base, manager_dn, manager_password,
         user_search="", group_search_base="", inhibit_infer_root_dn=False):
    """
    Jenkins ldap state method

    :param name: ldap state name
    :param server: ldap server host
    :param root_dn: root domain names
    :param user_search_base:
    :param manager_dn:
    :param manager_password:
    :param user_search: optional, default empty string
    :param group_search_base: optional, default empty string
    :param inhibit_infer_root_dn: optional, default false
    :returns: salt-specified state dict
    """
    if not server.startswith("ldap:") and not server.startswith("ldaps:"):
        server = "ldap://{server}".format(server=server)

    template = __salt__['jenkins_common.load_template'](
        'salt://jenkins/files/groovy/security.ldap.template',
        __env__)
    return __salt__['jenkins_common.api_call'](name, template,
                        ["CHANGED", "EXISTS"],
                        {
                            "name": name,
                            "server": server,
                            "rootDN": root_dn,
                            "userSearchBase": user_search_base if user_search_base else "",
                            "managerDN": manager_dn if manager_dn else "",
                            "managerPassword": manager_password if manager_password else "",
                            "userSearch": user_search if user_search else "",
                            "groupSearchBase": group_search_base if group_search_base else "",
                            "inhibitInferRootDN": "true" if inhibit_infer_root_dn else "false"
                        },
                        "Jenkins LDAP Settings")


def matrix(name, strategies, project_based=False):
    """
    Jenkins matrix security state method

    :param name: ldap state name
    :param strategies: dict with matrix strategies
    :param procect_based: flag if we configuring
        GlobalMatrix security or ProjectMatrix security
    :returns: salt-specified state dict
    """
    template = __salt__['jenkins_common.load_template'](
        'salt://jenkins/files/groovy/security.matrix.template',
        __env__)
    return __salt__['jenkins_common.api_call'](name, template,
                        ["CHANGED", "EXISTS"],
                        {
                            "strategies": _build_strategies(strategies),
                            "matrix_class": "ProjectMatrixAuthorizationStrategy" if project_based else "GlobalMatrixAuthorizationStrategy"},
                        "Jenkins Matrix security setting")

def _build_strategies(permissions):
    strategies_str = ""
    for strategy in _to_strategies_list(
            "strategy.add({},\"{}\")", _to_one_dict(permissions, "")):
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
