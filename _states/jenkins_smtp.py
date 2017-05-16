import logging
logger = logging.getLogger(__name__)

set_smtp_groovy = """\
def result = ""
for(desc in [Jenkins.getInstance().getDescriptor("hudson.plugins.emailext.ExtendedEmailPublisher"),Jenkins.getInstance().getDescriptor("hudson.tasks.Mailer")]){{
    if(desc.getSmtpServer().equals("{host}") &&
       desc.getSmtpAuthUsername().equals("{username}") &&
       desc.getSmtpAuthPassword().toString().equals("{password}") &&
       desc.getSmtpPort().equals("{port}") &&
       desc.getUseSsl() == {ssl} &&
       desc.getCharset().equals("{charset}") &&
       (!{reply_to_exists} || desc.getReplyAddress().equals("{reply_to}"))){{
            result = "EXISTS"
    }}else{{
        desc.setSmtpAuth("{username}", "{password}")
        desc.setUseSsl({ssl})
        if(desc instanceof hudson.plugins.emailext.ExtendedEmailPublisherDescriptor){{
            desc.setSmtpServer("{host}")
        }}else{{
            desc.setSmtpHost("{host}")
        }}
        desc.setSmtpPort("{port}")
        desc.setCharset("{charset}")
        if({reply_to_exists}){{
            desc.setReplyToAddress("{reply_to}")
        }}
        desc.save()
        result = "SUCCESS"
    }}
}}
print(result)
""" # noqa

set_admin_email_groovy = """
def jenkinsLocationConfiguration = JenkinsLocationConfiguration.get()
if(jenkinsLocationConfiguration.getAdminAddress().equals("{email}")){{
    print("EXISTS")
}}else{{
    jenkinsLocationConfiguration.setAdminAddress("{email}")
    jenkinsLocationConfiguration.save()
    print("SUCCESS")
}}
""" # noqa

def config(name, host, username, password, reply_to=None, port=25, ssl=False, charset="UTF-8"):
    """
    Jenkins SMTP server config state method

    :param name: configuration name
    :param host: SMTP host
    :param username: SMTP username
    :param password: SMTP password
    :param reply_to: sent emails ReplyTo header (optional)
    :param port: SMTP port (optional, default 25)
    :param ssl: use SSL for SMTP (optional, default False)
    :param charset: SMTP charset (optional, default UTF-8)
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
        ret['comment'] = 'Jenkins SMTP config %s %s' % (name, status.lower())
    else:
        call_result = __salt__['jenkins_common.call_groovy_script'](
            set_smtp_groovy, {"username": username, "password": password, "host": host, 
                              "reply_to_exists": "true" if reply_to else "false",
                              "reply_to": reply_to,
                              "port": port if port else 25,
                              "ssl": "true" if ssl else "false",
                              "charset": charset if charset else "UTF-8"})
        if call_result["code"] == 200 and call_result["msg"] in ["SUCCESS", "EXISTS"]:
            status = call_result["msg"]
            if status == "SUCCESS":
                ret['changes'][name] = status
            ret['comment'] = 'Jenkins smtp config %s %s' % (name, status.lower())
            result = True
        else:
            status = 'FAILED'
            logger.error(
                "Jenkins smtp API call failure: %s", call_result["msg"])
            ret['comment'] = 'Jenkins smtp API call failure: %s' % (call_result[
                                                                           "msg"])
    ret['result'] = None if test else result
    return ret


def admin_email(name, email):
    """
    Jenkins Admin user email config state method

    :param name: jenkins admin email
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
        ret['comment'] = 'Jenkins admin email config %s %s' % (name, status.lower())
    else:
        call_result = __salt__['jenkins_common.call_groovy_script'](
            set_admin_email_groovy, {"email": email})
        if call_result["code"] == 200 and call_result["msg"] in ["SUCCESS", "EXISTS"]:
            status = call_result["msg"]
            if status == "SUCCESS":
                ret['changes'][name] = status
            ret['comment'] = 'Jenkins admin email config %s %s' % (name, status.lower())
            result = True
        else:
            status = 'FAILED'
            logger.error(
                "Jenkins admin email API call failure: %s", call_result["msg"])
            ret['comment'] = 'Jenkins admin email API call failure: %s' % (call_result[
                                                                           "msg"])
    ret['result'] = None if test else result
    return ret
