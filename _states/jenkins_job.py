# -*- coding: utf-8 -*-

# Import Python libs
from __future__ import absolute_import
import difflib
import logging

# Import Salt libs
import salt.ext.six as six
import salt.utils

# Import XML parser
import xml.etree.ElementTree as ET
import hashlib

# Jenkins
try:
  import jenkins
  HAS_JENKINS = True
except ImportError:
  HAS_JENKINS = False

log = logging.getLogger(__name__)


def __virtual__():
    '''
    Only load if jenkins_common module exist.
    '''
    if HAS_JENKINS and 'jenkins_common.call_groovy_script' not in __salt__:
        return (
            False,
            'The jenkins_job state module cannot be loaded: '
            'jenkins_common not found')
    return True


def _elements_equal(e1, e2):
    return hashlib.md5(e1).hexdigest() == hashlib.md5(e2).hexdigest()


def present(name,
            config=None,
            **kwargs):
    '''
    Ensure the job is present in the Jenkins
    configured jobs
    name
        The unique name for the Jenkins job
    config
        The Salt URL for the file to use for
        configuring the job.
    '''
    test = __opts__['test']
    ret = {'name': name,
           'result': True,
           'changes': {},
           'comment': ['Job {0} is up to date.'.format(name)]}
    if test:
        status = 'CREATED'
        ret['changes'][name] = status
        ret['comment'] = 'Job %s %s' % (name, status.lower())
    else:
        _current_job_config = ''
        _job_exists = True
        try:
            _current_job_config = __salt__['jenkins.get_job_config'](name)
        except salt.exceptions.SaltInvocationError as e:
            if 'does not exists.' in str(e):
                _job_exists = False
            else:
                raise e


        if _job_exists:
            buf = six.moves.StringIO(_current_job_config)
            oldXMLstring = buf.read()

            cached_source_path = __salt__['cp.cache_file'](config, __env__)
            with salt.utils.fopen(cached_source_path) as _fp:
                newXMLstring = _fp.read()
            if not _elements_equal(oldXMLstring.strip(), newXMLstring.strip()):
                oldXML = ET.fromstring(oldXMLstring)
                newXML = ET.fromstring(newXMLstring)
                diff = difflib.unified_diff(
                    ET.tostringlist(oldXML, encoding='utf8', method='xml'),
                    ET.tostringlist(newXML, encoding='utf8', method='xml'), lineterm='')
                __salt__['jenkins.update_job'](name, config, __env__)
                ret['changes'][name] = ''.join(diff)
                ret['comment'] = 'Job {0} updated.'.format(name)

        else:
            cached_source_path = __salt__['cp.cache_file'](config, __env__)
            with salt.utils.fopen(cached_source_path) as _fp:
                new_config_xml = _fp.read()

            __salt__['jenkins.create_job'](name, config, __env__)

            buf = six.moves.StringIO(new_config_xml)
            diff = difflib.unified_diff('', buf.readlines(), lineterm='')
            ret['changes'][name] = ''.join(diff)
            ret['comment'].append('Job {0} added.'.format(name))

        ret['comment'] = '\n'.join(ret['comment'])
    return ret


def absent(name,
           **kwargs):
    '''
    Ensure the job is present in the Jenkins
    configured jobs

    name
        The name of the Jenkins job to remove.

    '''
    test = __opts__['test']
    ret = {'name': name,
           'result': True,
           'changes': {},
           'comment': []}
    if test:
        status = 'DELETED'
        ret['changes'][name] = status
        ret['comment'] = 'Node %s %s' % (name, status.lower())
    else:
        _job_exists = __salt__['jenkins.job_exists'](name)

        if _job_exists:
            __salt__['jenkins.delete_job'](name)
            ret['comment'] = 'Job {0} deleted.'.format(name)
        else:
            ret['comment'] = 'Job {0} already absent.'.format(name)
    return ret


def cleanup(name, jobs, **kwargs):
    '''
    Perform a cleanup - uninstall any installed job absents in given jobs list

    name
        The name of the Jenkins job to remove.
    jobs
        List of jobs which may NOT be uninstalled

    '''
    test = __opts__['test']
    ret = {'name': name,
           'result': True,
           'changes': {},
           'comment': "Cleanup not necessary"}
    list_jobs_groovy = """\
        print(Jenkins.instance.items.collect{{it -> it.name}})
    """
    deleted_jobs = []
    if test:
        status = 'CLEANED'
        ret['changes'][name] = status
        ret['comment'] = 'Jobs %s' % status.lower()
    else:
        call_result = __salt__['jenkins_common.call_groovy_script'](list_jobs_groovy,{})
        if call_result["code"] == 200:
            existing_jobs = call_result["msg"]
            if existing_jobs:
                for job in existing_jobs[1:-1].split(","):
                    if job:
                        job = job.strip()
                        if job not in jobs:
                            __salt__['jenkins.delete_job'](job)
                            deleted_jobs.append(job)
            else:
                log.error("Cannot get existing jobs list from Jenkins")
            if len(deleted_jobs) > 0:
                for del_job in deleted_jobs:
                    ret['changes'][del_job] = "removed"
                ret['comment'] = 'Jobs {} deleted.'.format(deleted_jobs)
        else:
            status = 'FAILED'
            log.error(
                "Jenkins jobs API call failure: %s", call_result["msg"])
            ret['comment'] = 'Jenkins jobs API call failure: %s' % (
                call_result["msg"])
    return ret
