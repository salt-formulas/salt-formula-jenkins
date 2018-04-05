import logging
logger = logging.getLogger(__name__)

set_theme_groovy = """\
try{
    if(Class.forName("org.codefirst.SimpleThemeDecorator")){
        def state;
        for (pd in PageDecorator.all()) {
          if (pd instanceof org.codefirst.SimpleThemeDecorator) {
            if(!pd.cssUrl.equals("${css_url}") || !pd.jsUrl.equals("${js_url}")){
                pd.cssUrl = "${css_url}"
                pd.jsUrl = "${js_url}"
                pd.save()
                state="SUCCESS"
            }else{
                state="EXISTS"
            }
          }
        }
        print(state)
    }
}catch(ClassNotFoundException e){
    print("Cannot user SimpleThemeDecorator, maybe Simple Theme Plugin not installed")
}
"""  # noqa


def __virtual__():
    '''
    Only load if jenkins_common module exist.
    '''
    if 'jenkins_common.call_groovy_script' not in __salt__:
        return (
            False,
            'The jenkins_theme state module cannot be loaded: '
            'jenkins_common not found')
    return True


def config(name, css_url, js_url):
    """
    Jenkins theme config state method

    :param name: configuration name
    :param css_url: URL to theme CSS
    :param js_url: URL to theme JS
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
        ret['comment'] = 'Jenkins Theme config %s %s' % (name, status.lower())
    else:
        call_result = __salt__['jenkins_common.call_groovy_script'](
            set_theme_groovy, {"css_url": css_url, "js_url": js_url})
        if call_result["code"] == 200 and call_result["msg"] in [
                "SUCCESS", "EXISTS"]:
            status = call_result["msg"]
            if status == "SUCCESS":
                ret['changes'][name] = status
            ret['comment'] = 'Jenkins theme config %s %s' % (
                name, status.lower())
            result = True
        else:
            status = 'FAILED'
            logger.error(
                "Jenkins theme API call failure: %s", call_result["msg"])
            ret['comment'] = 'Jenkins theme API call failure: %s' % (call_result[
                "msg"])
    ret['result'] = None if test else result
    return ret
