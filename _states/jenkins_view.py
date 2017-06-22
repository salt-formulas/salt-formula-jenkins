import logging
from json import dumps
logger = logging.getLogger(__name__)

add_view_groovy = """\
import java.util.stream.Collectors
import org.jenkinsci.plugins.categorizedview.CategorizedJobsView
import org.jenkinsci.plugins.categorizedview.GroupingRule
view = Jenkins.instance.getView("{view_name}")
if(view){{
  if(view.getClass().getName().equals("hudson.model.ListView")){{
    include_regex="{include_regex}"
    if(include_regex != "" && !view.getIncludeRegex().equals(include_regex)){{
        view.setIncludeRegex(include_regex)
        print("ADDED/CHANGED")
    }}else{{
        print("EXISTS")
    }}
  }}else if(view.getClass().getName().equals("org.jenkinsci.plugins.categorizedview.CategorizedJobsView")){{
    def jsonSlurper = new groovy.json.JsonSlurper()
    def inputCategories = jsonSlurper.parseText('{categories_string}')
    def groupRegexes = inputCategories.stream().map{{e -> e["group_regex"]}}.collect(Collectors.toList())
    def namingRules = inputCategories.stream().map{{e -> e["naming_rule"]}}.collect(Collectors.toList())
    def actualCategories = view.categorizationCriteria
    def equals = !actualCategories.isEmpty()
    def include_regex="{include_regex}"
    if(include_regex != "" && !view.getIncludeRegex().equals(include_regex)){{
        view.setIncludeRegex(include_regex)
        equals = false
    }}
    for(int i=0;i<actualCategories.size();i++){{
      if(!groupRegexes.contains(actualCategories[i].groupRegex) || !namingRules.contains(actualCategories[i].namingRule)){{
        equals = false
      }}
    }}
    if(!equals){{
      view.categorizationCriteria.clear()
      for(int i=0;i<inputCategories.size();i++){{
        view.categorizationCriteria.add(new GroupingRule(inputCategories[i].group_regex,inputCategories[i].naming_rule))
      }}
      print("ADDED/CHANGED")
    }}else{{
      print("EXISTS")
    }}
  }}else{{
    print("EXISTS")
  }}
}}else{{
  try{{
    {view_def}
    Jenkins.instance.addView(view)
    print("ADDED/CHANGED")
  }}catch(Exception e){{
    print("FAILED")
  }}
}}
"""  # noqa

remove_view_groovy = """\
view = Jenkins.instance.getView("{view_name}")
if(view){{
  try{{
    Jenkins.instance.deleteView(view)
    print("REMOVED")
  }}catch(Exception e){{
    print("FAILED")
  }}
}}else{{
  print("NOT PRESENT")
}}
"""  # noqa


def __virtual__():
    '''
    Only load if jenkins_common module exist.
    '''
    if 'jenkins_common.call_groovy_script' not in __salt__:
        return (
            False,
            'The jenkins_view state module cannot be loaded: '
            'jenkins_common not found')
    return True


def present(name, type="ListView", **kwargs):
    """
    Jenkins view present state method

    :param name: view name
    :param type: view type (default ListView)
    :returns: salt-specified state dict
    """
    return _plugin_call(name, type, add_view_groovy, ["ADDED/CHANGED", "EXISTS"], **kwargs)


def absent(name, **kwargs):
    """
    Jenkins view absent state method

    :param name: view name
    :returns: salt-specified state dict
    """
    return _plugin_call(name, None, remove_view_groovy, ["REMOVED", "NOT PRESENT"], **kwargs)


def _plugin_call(name, type, template, success_msgs, **kwargs):
    test = __opts__['test']  # noqa
    ret = {
        'name': name,
        'changes': {},
        'result': False,
        'comment': '',
    }
    result = False
    if test:
        status = success_msgs[0]
        ret['changes'][name] = status
        ret['comment'] = 'Jenkins view %s %s' % (name, status.lower())
    else:
        view_def = "view = new {}(\"{}\")".format(type, name)
        # handle view specific params
        include_regex = kwargs.get('include_regex')
        categories_string = ""
        if type == "ListView":
            if include_regex:
                view_def += "\nview.setIncludeRegex(\"{}\")".format(
                    include_regex)
        if type == "CategorizedJobsView":
            # add imports for categorized views
            if include_regex:
                view_def += "\nview.setIncludeRegex(\"{}\")".format(
                    include_regex)
            categories = kwargs.get('categories', [])
            for category in categories:
                view_def += "\nview.categorizationCriteria.add(new GroupingRule(\"{}\", \"{}\"))".format(
                    category["group_regex"], category["naming_rule"])
            # create catogories string readable in groovy
            categories_string = dumps(categories)

        call_result = __salt__['jenkins_common.call_groovy_script'](
            template, {"view_def": view_def, "view_name": name, "type": type if type else "", "include_regex": include_regex if include_regex else "", "categories_string": categories_string if categories_string else ""})
        if call_result["code"] == 200 and call_result["msg"] in success_msgs:
            status = call_result["msg"]
            if status == success_msgs[0]:
                ret['changes'][name] = status
            ret['comment'] = 'Jenkins view %s %s' % (name, status.lower())
            result = True
        else:
            status = 'FAILED'
            logger.error(
                "Jenkins view API call failure: %s", call_result["msg"])
            ret['comment'] = 'Jenkins view API call failure: %s' % (call_result[
                "msg"])
    ret['result'] = None if test else result
    return ret
