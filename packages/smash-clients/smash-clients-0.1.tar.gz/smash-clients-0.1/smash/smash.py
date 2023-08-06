# pylint:
#
"""
Smash client code.  All in one for now.
"""

import requests
from . import config

state_colours = {
    'okay': 'green',
    'unknown': 'gray',
    'warning': 'orange',
    'error': 'red',
    'unusable': 'black'
}

state_icons = {
    'okay': '',
    'unknown': ':question:',
    'warning': ':grimacing:',
    'error': ':cry:',
    'unusable': ':dizzy_face:'
}

state_totals = {
    'okay': 0,
    'unknown': 0,
    'warning': 0,
    'error': 0,
    'unusable': 0,
    'all': 0
}


def overall_state(totals):
    """ Determines overall state of a set to be the worst occurring, given
    totals for each possible state in the set, and a short string summary.
    """
    summary_parts = []
    overall = None
    if totals['unusable'] > 0:
        summary_parts.append(f"{totals['unusable']}U")
        overall = 'unusable'
    if totals['error'] > 0:
        summary_parts.append(f"{totals['error']}E")
        overall = overall or 'error'
    if totals['warning'] > 0:
        summary_parts.append(f"{totals['warning']}w")
        overall = overall or 'warning'
    if totals['unknown'] > 0:
        summary_parts.append(f"{totals['unknown']}?")
        overall = overall or 'unknown'
    if totals['okay'] > 0:
        overall = overall or 'okay'
    if summary_parts:
        summary = " ".join(summary_parts) + f" of {totals['all']}"
    else:
        summary = f"All {totals['all']} ok"
    return(overall, summary)

def load_nodes(api_url, timeout):
    """ Loads nodes from Smash server and their statuses.
    """
    nodes = requests.get(api_url + '/nodes/', timeout=timeout).json()
    for node in nodes:

        node['totals'] = {
            'okay': 0,
            'unknown': 0,
            'warning': 0,
            'error': 0,
            'unusable': 0,
            'all': 0
        }

        # request status
        node['statuses'] = requests.get(
            f"{api_url}/nodes/{node['node']}/status/", timeout=timeout
        ).json()
        for status in node['statuses']:
            state = status['state']
            state_totals[state] += 1
            state_totals['all'] += 1
            node['totals'][state] += 1
            node['totals']['all'] += 1
            status['message'] = status['message'].replace('\n','; ')

    return nodes

def xbar():
    """ Interpret Smash node and status information as menus for xbar.
    """
    # load configuration
    # pylint: disable=invalid-name,broad-except
    try:
        conf = config.xbar()
        conf.merge()
    except Exception as e:
        print(f"{config.APP_TAG} | color={state_colours['unknown']}")
        print("---")
        print(f"Could not load Smash configuration: {e}")
        return

    api_url = conf['server'] + '/api'
    timeout = conf['request_timeout']

    # load node and status information
    try:
        nodes = load_nodes(api_url, timeout)
    except requests.exceptions.ConnectionError:
        print(f"{config.APP_TAG} | color={state_colours['unknown']}")
        print("---")
        print("Could not connect to Smash server")
        return

    # now do the BitBar/xbar stuff
    # determine and present the overall status in menu bar
    (overall, summary) = overall_state(state_totals)
    colour = state_colours[overall]
    print(f"{config.APP_TAG} | color={colour}")
    print("---")

    # create menu entries for each node and its status items
    for node in nodes:

        # determine overall node status
        (overall, summary) = overall_state(node['totals'])

        # present menu entry for node
        if overall == 'okay':
            print(node['node'])
        else:
            colour = state_colours[overall]
            print(f"{node['node']} {state_icons[overall]} {summary} | color={colour}")

        # build menu of node statuses
        for status in node['statuses']:
            state = status['state']
            colour = state_colours[state]
            print(f"--{state_icons[state]} {status['test']} "
                  f"{state} {status['message']} | color={colour}")

if __name__ == '__main__':
    xbar()
