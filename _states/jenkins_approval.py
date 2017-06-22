import logging
logger = logging.getLogger(__name__)

approve_signature_groovy = """\
import org.jenkinsci.plugins.scriptsecurity.scripts.ScriptApproval
import org.jenkinsci.plugins.scriptsecurity.scripts.languages.GroovyLanguage
import org.jenkinsci.plugins.scriptsecurity.scripts.ApprovalContext
def signature = '{signature}'
def scriptApproval = ScriptApproval.get()
def approvedSignatures = Arrays.asList(scriptApproval.approvedSignatures)
if(approvedSignatures.contains(signature)){{
    print("EXISTS")
}}else{{
    try{{
        scriptApproval.pendingSignatures.add(new ScriptApproval.PendingSignature(signature, false, ApprovalContext.create()))
        scriptApproval.approveSignature(signature)
        if(Arrays.asList(scriptApproval.approvedSignatures).contains(signature)){{
            print("SUCCESS")
        }}else{{
            print("FAILED")
        }}
    }}catch(e){{
        print(e)
    }}
}}
""" # noqa

deny_signature_groovy = """\
import org.jenkinsci.plugins.scriptsecurity.scripts.ScriptApproval
import org.jenkinsci.plugins.scriptsecurity.scripts.languages.GroovyLanguage
import org.jenkinsci.plugins.scriptsecurity.scripts.ApprovalContext
def signature = '{signature}'
def scriptApproval = ScriptApproval.get()
def approvedSignatures = Arrays.asList(scriptApproval.approvedSignatures)
if(approvedSignatures.contains(signature)){{
    try{{
        scriptApproval.denySignature(signature)
        if(!scriptApproval.approvedSignatures.contains(signature)){{
            print("SUCCESS")
        }}else{{
            print("FAILED")
        }}
    }}catch(e){{
        print(e)
    }}
}}else{{
    print("NOT PRESENT")
}}


"""


def __virtual__():
    '''
    Only load if jenkins_common module exist.
    '''
    if 'jenkins_common.call_groovy_script' not in __salt__:
        return (
            False,
            'The jenkins_approval state module cannot be loaded: '
            'jenkins_common not found')
    return True


def approved(name):
    """
    Jenkins Script approval approve state method

    :param name: signature to approve
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
        status = "SUCCESS"
        ret['changes'][name] = status
        ret['comment'] = 'Jenkins script approval config %s %s' % (name, status.lower())
    else:
        call_result = __salt__['jenkins_common.call_groovy_script'](
            approve_signature_groovy, {"signature":name})
        if call_result["code"] == 200 and call_result["msg"] in ["SUCCESS", "EXISTS"]:
            status = call_result["msg"]
            if status == "SUCCESS":
                ret['changes'][name] = status
            ret['comment'] = 'Jenkins script approval config %s %s' % (name, status.lower())
            result = True
        else:
            status = 'FAILED'
            logger.error(
                "Jenkins script approval API call failure: %s", call_result["msg"])
            ret['comment'] = 'Jenkins script approval API call failure: %s' % (call_result[
                                                                           "msg"])
    ret['result'] = None if test else result
    return ret


def denied(name):
    """
    Jenkins Script approval deny state method

    :param name: signature to deny
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
        status = "SUCCESS"
        ret['changes'][name] = status
        ret['comment'] = 'Jenkins script approval config %s %s' % (name, status.lower())
    else:
        call_result = __salt__['jenkins_common.call_groovy_script'](
            deny_signature_groovy, {"signature":name})
        if call_result["code"] == 200 and call_result["msg"] in ["SUCCESS", "NOT PRESENT"]:
            status = call_result["msg"]
            if status == "SUCCESS":
                ret['changes'][name] = status
            ret['comment'] = 'Jenkins script approval config %s %s' % (name, status.lower())
            result = True
        else:
            status = 'FAILED'
            logger.error(
                "Jenkins script approval API call failure: %s", call_result["msg"])
            ret['comment'] = 'Jenkins script approval lib API call failure: %s' % (call_result[
                                                                           "msg"])
    ret['result'] = None if test else result
    return ret
