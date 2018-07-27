import json
import logging
import time


log = logging.getLogger(__name__)


def __virtual__():
    '''
    Only load if jenkins_common module exist.
    '''
    if 'jenkins_common.call_groovy_script' not in __salt__:
        return (
            False,
            'The jenkins_node state module cannot be loaded: '
            'jenkins_common not found')
    return True

def managed(name, plugins, remove_unwanted=False, force_remove=False):
    """
    Manage jenkins plugins

    :param name: salt resource name (usually 'jenkins_plugin_manage')
    :param plugins: map containing plugin names and parameters
    :param remove_unwanted: whether to remove not listed plugins
    :param force_remove: force removing plugins recursively with all dependent plugins
    :returns: salt-specified state dict
    """
    log.info('Managing jenkins plugins')
    template = __salt__['jenkins_common.load_template'](
        'salt://jenkins/files/groovy/plugin.template',
        __env__)
    result = __salt__['jenkins_common.api_call'](name, template,
                        [ 'UPDATED', 'NO CHANGES' ],
                        {
                            'plugin_list': json.dumps(plugins),
                            'clean_unwanted': remove_unwanted,
                            'force_remove': force_remove
                        },
                        'Manage Jenkins plugins')
    log.debug('Got result: ' + json.dumps(result))

    log.info('Checking if restart is required...')
    # While next code is successful, we should wait for jenkins shutdown
    # either:
    #   - false returned by isQuietingDown()
    #   - any error meaning that jenkins is unavailable (restarting)
    wait = { 'result': True }
    while (wait['result']):
        wait = __salt__['jenkins_common.api_call']('jenkins_restart_wait',
                'println Jenkins.instance.isQuietingDown()', [ 'true' ], {},
                'Wait for jenkins restart')
        if (wait['result']):
            log.debug('Jenkins restart is required. Waiting...')
        time.sleep(5)

    return result
