import logging
logger = logging.getLogger(__name__)

config_global_libs_groovy = """\
import org.jenkinsci.plugins.workflow.libs.SCMSourceRetriever;
import org.jenkinsci.plugins.workflow.libs.LibraryConfiguration;
import jenkins.plugins.git.GitSCMSource;

def globalLibsDesc = Jenkins.getInstance().getDescriptor("org.jenkinsci.plugins.workflow.libs.GlobalLibraries")
def existingLib = globalLibsDesc.get().getLibraries().find{{
  (!it.retriever.class.name.equals("org.jenkinsci.plugins.workflow.libs.SCMSourceRetriever") || 
   it.retriever.scm.remote.equals("{url}") &&
   it.retriever.scm.credentialsId.equals("{credential_id}")) &&
   it.name.equals("{lib_name}") &&
   it.defaultVersion.equals("{branch}") &&
   it.implicit == true
}}
if(existingLib){{
    print("EXISTS")
}}else{{
    SCMSourceRetriever retriever = new SCMSourceRetriever(new GitSCMSource(
        "{lib_name}",
        "{url}",
        "{credential_id}",
        "*",
        "",
        false))
    LibraryConfiguration library = new LibraryConfiguration("{lib_name}", retriever)
    library.setDefaultVersion("{branch}")
    library.setImplicit({implicit})
    if(globalLibsDesc.get().getLibraries().isEmpty()){{
      globalLibsDesc.get().setLibraries([library])
    }}else{{
      globalLibsDesc.get().getLibraries().removeIf{{ it.name.equals("{lib_name}")}}
      globalLibsDesc.get().getLibraries().add(library)
    }}
    print("SUCCESS")
}}
""" # noqa

remove_global_libs_groovy = """\
def globalLibsDesc = Jenkins.getInstance().getDescriptor("org.jenkinsci.plugins.workflow.libs.GlobalLibraries")
def existingLib = globalLibsDesc.get().getLibraries().removeIf{{it.name.equals("{lib_name}")}}
if(existingLib){{
    print("DELETED")
}}else{{
    print("NOT PRESENT")
}}
"""

def present(name, url, branch="master", credential_id="", implicit=True, **kwargs):
    """
    Jenkins Global pipeline library present state method

    :param name: pipeline library name
    :param url: url to remote repo
    :param branch: remote branch
    :param credential_id: credential id for repo
    :param implicit: implicit load boolean switch
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
        ret['comment'] = 'Jenkins pipeline lib config %s %s' % (name, status.lower())
    else:
        call_result = __salt__['jenkins_common.call_groovy_script'](
            config_global_libs_groovy, {"lib_name":name,
                                  "url": url,
                                  "branch": branch,
                                  "credential_id": credential_id if credential_id else "",
                                  "implicit": "true" if implicit else "false"
                                  })
        if call_result["code"] == 200 and call_result["msg"] in ["SUCCESS", "EXISTS"]:
            status = call_result["msg"]
            if status == "SUCCESS":
                ret['changes'][name] = status
            ret['comment'] = 'Jenkins pipeline lib config %s %s' % (name, status.lower())
            result = True
        else:
            status = 'FAILED'
            logger.error(
                "Jenkins pipeline lib API call failure: %s", call_result["msg"])
            ret['comment'] = 'Jenkins pipeline lib API call failure: %s' % (call_result[
                                                                           "msg"])
    ret['result'] = None if test else result
    return ret


def absent(name, **kwargs):
    """
    Jenkins Global pipeline library absent state method

    :param name: pipeline library name
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
        ret['comment'] = 'Jenkins pipeline lib config %s %s' % (name, status.lower())
    else:
        call_result = __salt__['jenkins_common.call_groovy_script'](
            remove_global_libs_groovy, {"lib_name":name})
        if call_result["code"] == 200 and call_result["msg"] in ["DELETED", "NOT PRESENT"]:
            status = call_result["msg"]
            if status == "DELETED":
                ret['changes'][name] = status
            ret['comment'] = 'Jenkins pipeline lib config %s %s' % (name, status.lower())
            result = True
        else:
            status = 'FAILED'
            logger.error(
                "Jenkins pipeline lib API call failure: %s", call_result["msg"])
            ret['comment'] = 'Jenkins pipeline lib API call failure: %s' % (call_result[
                                                                           "msg"])
    ret['result'] = None if test else result
    return ret
