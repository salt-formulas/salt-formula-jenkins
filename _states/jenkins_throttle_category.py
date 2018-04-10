import json
import logging

logger = logging.getLogger(__name__)

create_throttle_groovy = u"""\
import jenkins.model.*
import hudson.plugins.throttleconcurrents.ThrottleJobProperty
import net.sf.json.JSONObject

String categoryName = '${categoryName}'
Integer maxPerNode = ${maxPerNode}
Integer maxTotal = ${maxTotal}
String labels = '${labels}'

Boolean categoryExists = true
Boolean pairsExists = true

def descriptor = Jenkins.getInstance().getDescriptorByType(
        ThrottleJobProperty.DescriptorImpl.class)

def categories = descriptor.getCategories()

def category = categories.find {it.categoryName == categoryName}

if (! category) {
    categoryExists = false
    category = new ThrottleJobProperty.ThrottleCategory(
        categoryName, maxPerNode, maxTotal, null)
    categories.add(category)
}

if ((category.maxConcurrentPerNode != maxPerNode) ||
    (category.maxConcurrentTotal != maxTotal)) {
    categoryExists = false
    category.maxConcurrentPerNode = maxPerNode
    category.maxConcurrentTotal == maxTotal
}

if (labels) {
    def nodeLabeledPairs = category.getNodeLabeledPairs()
    def _pairs = JSONObject.fromObject(labels)
    _pairs.each{ key, val ->
        _pair = nodeLabeledPairs.find{
            it.throttledNodeLabel == key
        }
        if (! _pair) {
            pairsExists = false
            nodeLabeledPairs.add(new ThrottleJobProperty.NodeLabeledPair(
                key, val));
        } else if (_pair.maxConcurrentPerNodeLabeled != val) {
            pairsExists = false
            _pair.maxConcurrentPerNodeLabeled = val
        }
    }
}

if (categoryExists && pairsExists) {
    print("EXISTS")
} else {
    descriptor.save()
    print("CREATED")
}
"""

remove_throttle_groovy = """
import jenkins.model.*
import hudson.plugins.throttleconcurrents.ThrottleJobProperty

String categoryName = '${categoryName}'
Integer index = -1

def descriptor = Jenkins.getInstance().getDescriptorByType(
        ThrottleJobProperty.DescriptorImpl.class)

def categories = descriptor.getCategories()

categories.eachWithIndex {it, id ->
    if (it.categoryName == categoryName) {
        index = id
    }
}

if ( index == -1) {
    print("NOT PRESENT")
} else {
    categories.remove(index)
    descriptor.save()
    print("REMOVED")
}
"""

def __virtual__():
    '''
    Only load if jenkins_common module exist.
    '''
    if 'jenkins_common.call_groovy_script' not in __salt__:
        return (
            False,
            'The jenkins_plugin state module cannot be loaded: '
            'jenkins_common not found')
    return True

def present(name, max_total, max_per_node, labels=[]):
    """
    Jenkins Throttle Category state method

    :param name: category name
    :param max_total: maximum total concurrent builds
    :param max_per_node: maximum concurrent builds per node
    :param labels: maximum per labeled node dict
    :returns: salt-specified state dict
    """

    return _plugin_call(name, create_throttle_groovy,
                        ["CREATED", "EXISTS"],
                        {"categoryName": name,
                        "maxPerNode": max_per_node if max_per_node else 0,
                        "maxTotal": max_total if max_total else 0,
                        "labels": json.dumps(labels) if labels else ""})

def absent(name):
    """
    Jenkins Throttle Category absence state method

    :param name: category name
    :returns: salt-specified state dict
    """
    return _plugin_call(name, remove_throttle_groovy,
                        ["REMOVED", "NOT PRESENT"],
                        {"categoryName": name})

def _plugin_call(name, template, success_msgs, params):
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
        ret['comment'] = 'Throttle Category "%s" %s' % (name, status.lower())
    else:
        call_result = __salt__['jenkins_common.call_groovy_script'](
            template, params)
        if call_result["code"] == 200 and call_result["msg"] in success_msgs:
            status = call_result["msg"]
            if status == success_msgs[0]:
                ret['changes'][name] = status
            ret['comment'] = 'Throttle Category "%s" %s' % (name, status.lower())
            result = True
        else:
            status = 'FAILED'
            logger.error(
                'Jenkins API call failure: %s', call_result["msg"])
            ret['comment'] = 'Jenkins API call failure: %s' % (call_result[
                "msg"])
    ret['result'] = None if test else result
    return ret
