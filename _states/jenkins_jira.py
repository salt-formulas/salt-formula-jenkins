import json
import logging

logger = logging.getLogger(__name__)

def __virtual__():
    '''
    Only load if jenkins_common module exist.
    '''
    if 'jenkins_common.call_groovy_script' not in __salt__:
        return (
            False,
            'The jenkins_jira state module cannot be loaded: '
            'jenkins_common not found')
    return True

def present (name, sites, **kwargs):
    """
    Jenkins Jira instance state method

    :param name: ID name
    :param sites:Jira sites dict
    :
    :sites[name] params:
    :param link_url: root URL of JIRA installation for "normal" access
    :param http_auth: connect to JIRA using HTTP Basic Authentication
    :param use_wiki_notation: enable if JIRA supports Wiki notation
    :param record_scm: record scm changes in JIRAA
    :param disable_changelog: do not create JIRA hyperlinks in the changeset
    :param issue_pattern: custom pattern to search for JIRA issue ids
    :param any_build_result: update issues on any build result
    :param user: JIRA user name
    :param password: JIRA user password
    :param conn_timeout: connection timeout for JIRA REST API calls
    :param visible_for_group: allow to read comments for JIRA group
    :param visible_for_project: allow to read comments for JIRA project
    :param timestamps: enable SCM change date and time entries
    :param timestamp_format: timestamp format
    :
    :returns: salt-specified state dict
    """

    template = __salt__['jenkins_common.load_template'](
        'salt://jenkins/files/groovy/jira.template',
        __env__)
    return __salt__['jenkins_common.api_call'](name, template,
                        ["CREATED", "EXISTS"],
                        {
                            'sites': json.dumps(sites),
                            'absent': False
                        },
                        'JIRA server')

def absent(name):
    """
    Jenkins Jira instance absence state method

    :param name: ID name
    :returns: salt-specified state dict
    """
    template = __salt__['jenkins_common.load_template'](
        'salt://jenkins/files/groovy/jira.template',
        __env__)
    return __salt__['jenkins_common.api_call'](name, template,
                        ["REMOVED", "NOT PRESENT"],
                        {
                            'sites': '{}',
                            'absent': True
                        },
                        'JIRA server')

