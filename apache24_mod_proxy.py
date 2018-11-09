#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2016, Olivier Boukili <boukili.olivier@gmail.com>
#
# This file is part of Ansible.
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: apache2_mod_proxy
author: nikhil zadoo"
version_added: "2.2"
short_description: Set and/or get members' attributes of an Apache httpd 2.4 mod_proxy balancer pool
description:
  - Set and/or get members' attributes of an Apache httpd 2.4 mod_proxy balancer
    pool, using HTTP POST and GET requests. The httpd mod_proxy balancer-member
    status page has to be enabled and accessible, as this module relies on parsing
    this page. This module supports ansible check_mode, and requires BeautifulSoup
    python module.
options:
  balancer_url_suffix:
    default: /balancer-manager/
    description:
      - Suffix of the balancer pool url required to access the balancer pool
        status page (e.g. balancer_vhost[:port]/balancer_url_suffix).
    required: false
  balancer_vhost:
    default: None
    description:
      - (ipv4|ipv6|fqdn):port of the Apache httpd 2.4 mod_proxy balancer pool.
    required: true
  member_host:
    default: None
    description:
      - (ipv4|ipv6|fqdn) of the balancer member to get or to set attributes to.
        Port number is autodetected and should not be specified here.
        If undefined, apache2_mod_proxy module will return a members list of
        dictionaries of all the current balancer pool members' attributes.
    required: false
  state:
    default: None
    description:
      - Desired state of the member host.
        (absent|disabled),drained,hot_standby,ignore_errors can be
        simultaneously invoked by separating them with a comma (e.g. state=drained,ignore_errors).
    required: false
    choices: ["present", "absent", "enabled", "disabled", "drained", "hot_standby", "ignore_errors"]
  tls:
    default: false
    description:
      - Use https to access balancer management page.
    choices: ["true", "false"]
  validate_certs:
    default: true
    description:
      - Validate ssl/tls certificates.
    choices: ["true", "false"]
'''

EXAMPLES = '''
# Get all current balancer pool members' attributes:
- apache2_mod_proxy:
    balancer_vhost: 10.0.0.2

# Get a specific member's attributes:
- apache2_mod_proxy:
    balancer_vhost: myws.mydomain.org
    balancer_suffix: /lb/
    member_host: node1.myws.mydomain.org

# Enable all balancer pool members:
- apache2_mod_proxy:
    balancer_vhost: '{{ myloadbalancer_host }}'
  register: result
- apache2_mod_proxy:
    balancer_vhost: '{{ myloadbalancer_host }}'
    member_host: '{{ item.host }}'
    state: present
  with_items: '{{ result.members }}'

# Gracefully disable a member from a loadbalancer node:
- apache2_mod_proxy:
    balancer_vhost: '{{ vhost_host }}'
    member_host: '{{ member.host }}'
    state: drained
  delegate_to: myloadbalancernode
- wait_for:
    host: '{{ member.host }}'
    port: '{{ member.port }}'
    state: drained
  delegate_to: myloadbalancernode
- apache2_mod_proxy:
    balancer_vhost: '{{ vhost_host }}'
    member_host: '{{ member.host }}'
    state: absent
  delegate_to: myloadbalancernode
'''

RETURN = '''
member:
    description: specific balancer member information dictionary, returned when apache2_mod_proxy module is invoked with member_host parameter.
    type: dict
    returned: success
    sample:
      {"attributes":
            {"Busy": "0",
            "Elected": "42",
            "Factor": "1",
            "From": "136K",
            "Load": "0",
            "Route": null,
            "RouteRedir": null,
            "Set": "0",
            "Status": "Init Ok ",
            "To": " 47K",
            "Worker URL": null
        },
        "balancer_url": "http://10.10.0.2/balancer-manager/",
        "host": "10.10.0.20",
        "management_url": "http://10.10.0.2/lb/?b=mywsbalancer&w=http://10.10.0.20:8080/ws&nonce=8925436c-79c6-4841-8936-e7d13b79239b",
        "path": "/ws",
        "port": 8080,
        "protocol": "http",
        "status": {
            "disabled": false,
            "drained": false,
            "hot_standby": false,
            "ignore_errors": false
        }
      }
members:
    description: list of member (defined above) dictionaries, returned when apache2_mod_proxy is invoked with no member_host and state args.
    returned: success
    type: list
    sample:
      [{"attributes": {
            "Busy": "0",
            "Elected": "42",
            "Factor": "1",
            "From": "136K",
            "Load": "0",
            "Route": null,
            "RouteRedir": null,
            "Set": "0",
            "Status": "Init Ok ",
            "To": " 47K",
            "Worker URL": null
        },
        "balancer_url": "http://10.10.0.2/balancer-manager/",
        "host": "10.10.0.20",
        "management_url": "http://10.10.0.2/lb/?b=mywsbalancer&w=http://10.10.0.20:8080/ws&nonce=8925436c-79c6-4841-8936-e7d13b79239b",
        "path": "/ws",
        "port": 8080,
        "protocol": "http",
        "status": {
            "disabled": false,
            "drained": false,
            "hot_standby": false,
            "ignore_errors": false
        }
        },
        {"attributes": {
            "Busy": "0",
            "Elected": "42",
            "Factor": "1",
            "From": "136K",
            "Load": "0",
            "Route": null,
            "RouteRedir": null,
            "Set": "0",
            "Status": "Init Ok ",
            "To": " 47K",
            "Worker URL": null
        },
        "balancer_url": "http://10.10.0.2/balancer-manager/",
        "host": "10.10.0.21",
        "management_url": "http://10.10.0.2/lb/?b=mywsbalancer&w=http://10.10.0.21:8080/ws&nonce=8925436c-79c6-4841-8936-e7d13b79239b",
        "path": "/ws",
        "port": 8080,
        "protocol": "http",
        "status": {
            "disabled": false,
            "drained": false,
            "hot_standby": false,
            "ignore_errors": false}
        }
      ]
'''

import re

try:
    from bs4 import BeautifulSoup
except ImportError:
    HAS_BEAUTIFULSOUP = False
else:
    HAS_BEAUTIFULSOUP = True

# balancer member attributes extraction regexp:
EXPRESSION = r"(b=([\w\.\-]+)&w=(https?|ajp|wss?|ftp|[sf]cgi)://([\w\.\-]+):?(\d*)([/\w\.\-]*)&?[\w\-\=]*)"
# Apache2 server version extraction regexp:
APACHE_VERSION_EXPRESSION = r"Server Version: Apache/([\d.]+) \((.*)?\)"

def regexp_extraction(string, _regexp, groups=1):
    """ Returns the capture group (default=1) specified in the regexp, applied to the string """
    regexp_search = re.search(string=str(string), pattern=str(_regexp))
    if regexp_search:
        if regexp_search.group(groups) != '':
            return str(regexp_search.group(groups))
    return None

class BalancerMember(object):
    """ Apache 2.4 mod_proxy LB balancer member.
    attributes:
        read-only:
            host -> member host (string),
            management_url -> member management url (string),
            protocol -> member protocol (string)
            port -> member port (string),
            path -> member location (string),
            balancer_url -> url of this member's parent balancer (string),
            attributes -> whole member attributes (dictionary)
            module -> ansible module instance (AnsibleModule object).
        writable:
            status -> status of the member (dictionary)
    """
    from ansible.module_utils.basic import AnsibleModule
    global_module = AnsibleModule(
        argument_spec=dict(
            balancer_vhost=dict(required=True, default=None, type='str'),
            balancer_url_suffix=dict(default="/balancer-manager/", type='str'),
            member_host=dict(type='str'),
            state=dict(type='str'),
            tls=dict(default=False, type='bool'),
            validate_certs=dict(default=True, type='bool'),
            url_username=dict(default=None, required=False),
            url_password=dict(default=None, no_log=True)
        ),
        supports_check_mode=True
    )

    def __init__(self, management_url, balancer_url, module, soup):
        self.host = regexp_extraction(management_url, str(EXPRESSION), 4)
        self.management_url = str(management_url)
        self.protocol = regexp_extraction(management_url, EXPRESSION, 3)
        self.port = regexp_extraction(management_url, EXPRESSION, 5)
        self.path = regexp_extraction(management_url, EXPRESSION, 6)
        self.balancer_url = str(balancer_url)
        self.module = module
	self.soup = soup
	BalancerMember.global_module = module
	if self.module.params['member_host'] is None:
	    self.attributes = self.get_member_attributes()
	#print "in balancer mamber object"

    def get_member_attributes(self):
        """ Returns a dictionary of a balancer member's attributes."""
	balancer_member_page = fetch_url(self.module, self.management_url)
        try:
            assert balancer_member_page[1]['status'] == 200
        except AssertionError:
            self.module.fail_json(msg="Could not get balancer_member_page, check for connectivity! " + balancer_member_page[1])
        else:
            try:
		if self.soup is None:
		    soup = BeautifulSoup(balancer_member_page[0], "lxml")
		else:
		    soup = self.soup
	#soup = BeautifulSoup(balancer_member_page)
            except TypeError:
                self.module.fail_json(msg="Cannot parse balancer_member_page HTML! " + str(soup))
            else:
        	subsoup1 = soup.find_all('tr')
        	keys = subsoup1[2].find_all('th')
        	subsoup = soup.find_all('tr')
        	for line in subsoup:
            	    line1 = line.find_all('td')
            	    if re.search(pattern="</a></td>, <td>" + self.host, string=str(line1)):
                	return dict((keys[x].string, line1[x].string) for x in range(0, len(keys)))

    def get_member_status(self):
        """ Returns a dictionary of a balancer member's status attributes."""
        status_mapping = {'disabled':'Dis',
                          'drained':'Drn',
                          'hot_standby':'Stby',
                          'ignore_errors':'Ign'}
        status = {}
        actual_status = str(self.attributes['Status'])
        for mode in status_mapping.keys():
            if re.search(pattern=status_mapping[mode], string=actual_status):
                status[mode] = True
            else:
                status[mode] = False
        return status

    def set_member_status(self, values):
        """ Sets a balancer member's status attributes amongst pre-mapped values."""
        values_mapping = {'disabled':'&w_status_D',
                          'drained':'&w_status_N',
                          'hot_standby':'&w_status_H',
                          'ignore_errors':'&w_status_I'}
        request_body = regexp_extraction(self.management_url, EXPRESSION, 1)
        for k in values_mapping.keys():
            if values[str(k)]:
                request_body = request_body + str(values_mapping[k]) + '=1'
            else:
                request_body = request_body + str(values_mapping[k]) + '=0'
        response = fetch_url(self.module, self.management_url, data=str(request_body))
        try:
            assert response[1]['status'] == 200
        except AssertionError:
            self.module.fail_json(msg="Could not set the member status! " + self.host + " " + response[1]['status'])

    if global_module.params['member_host'] is not None:
	attributes = property(get_member_attributes)
    #attributes = get_member_attributes()
    #status = property(get_member_status)
    status = property(get_member_status, set_member_status)


class Balancer(object):
    """ Apache httpd 2.4 mod_proxy balancer object"""
    def __init__(self, host, suffix, module, members=None, tls=False):
        if tls:
            self.base_url = str(str('https://') + str(host))
            self.url = str(str('https://') + str(host) + str(suffix))
        else:
            self.base_url = str(str('http://') + str(host))
            self.url = str(str('http://') + str(host) + str(suffix))
        self.module = module
        self.page = self.fetch_balancer_page()
        if members is None:
            self._members = []

    def fetch_balancer_page(self):
        """ Returns the balancer management html page as a string for later parsing."""
        page = fetch_url(self.module, str(self.url))
        try:
            assert page[1]['status'] == 200
        except AssertionError:
            self.module.fail_json(msg="Could not get balancer page! HTTP status response: " + str(page[1]['status']))
        else:
            content = page[0].read()
            apache_version = regexp_extraction(content, APACHE_VERSION_EXPRESSION, 1)
            if not re.search(pattern=r"2\.4\.[\d]*", string=str(apache_version)):
                self.module.fail_json(msg="This module only acts on an Apache2 2.4+ instance, current Apache2 version: " + str(apache_version))
            return content

    def get_balancer_members(self):
        """ Returns members of the balancer as a generator object for later iteration."""
        try:
            soup = BeautifulSoup(self.page, "lxml")
	    #Balancer.global_soup = soup
        except TypeError:
            self.module.fail_json(msg="Cannot parse balancer page HTML! " + str(self.page))
        else:
	    subsoup = soup.find_all(href=True)
            for element in subsoup[1::1]:
                balancer_member_suffix_tmp = str(element.get('href'))
                if re.search('http',str(balancer_member_suffix_tmp)):
		    balancer_member_suffix = balancer_member_suffix_tmp
                    try:
                        assert balancer_member_suffix is not ''
                    except AssertionError:
                        self.module.fail_json(msg="Argument 'balancer_member_suffix' is empty!")
                    else:
                        if self.module.params['member_host'] is None:
                            yield BalancerMember(str(self.base_url + balancer_member_suffix), str(self.url),self.module, soup)
                        else:
                            if re.search(pattern=str(self.module.params['member_host']),string=str(balancer_member_suffix)):
                                yield BalancerMember(str(self.base_url + balancer_member_suffix), str(self.url), self.module, soup=None)

    members = property(get_balancer_members)

def main():
    """ Initiates module."""
    module = AnsibleModule(
        argument_spec=dict(
            balancer_vhost=dict(required=True, default=None, type='str'),
            balancer_url_suffix=dict(default="/balancer-manager/", type='str'),
            member_host=dict(type='str'),
            state=dict(type='str'),
            tls=dict(default=False, type='bool'),
            validate_certs=dict(default=True, type='bool'),
            url_username=dict(default=None, required=False),
            url_password=dict(default=None, no_log=True)
        ),
        supports_check_mode=True
    )

    if HAS_BEAUTIFULSOUP is False:
        module.fail_json(msg="python module 'BeautifulSoup' is required!")

    if module.params['state'] is not None:
        states = module.params['state'].split(',')
        if (len(states) > 1) and (("present" in states) or ("enabled" in states)):
            module.fail_json(msg="state present/enabled is mutually exclusive with other states!")
        else:
	    if module.params['member_host'] is None:
	        module.fail_json(msg="Exactly one member_host should be provided for which state needs to be set. else please use parameters without 'state' to query all members")
            for _state in states:
                if _state not in ['present', 'absent', 'enabled', 'disabled', 'drained', 'hot_standby', 'ignore_errors']:
                    module.fail_json(msg="State can only take values amongst 'present', 'absent', 'enabled', 'disabled', 'drained', 'hot_standby', 'ignore_errors'.")
    else:
        states = ['None']

    mybalancer = Balancer(module.params['balancer_vhost'],
                          module.params['balancer_url_suffix'],
                          module=module,
                          tls=module.params['tls'])

    if module.params['member_host'] is None:
        json_output_list = []
        for member in mybalancer.members:
            json_output_list.append({
                "host": member.host,
                "status": member.status,
                "protocol": member.protocol,
                "port": member.port,
                "path": member.path,
                "attributes": member.attributes,
                "management_url": member.management_url,
                "balancer_url": member.balancer_url
            })
        module.exit_json(
            changed=False,
            members=json_output_list
        )
    else:
        changed = False
        member_exists = False
        member_status = {'disabled': False, 'drained': False, 'hot_standby': False, 'ignore_errors':False}
        for mode in member_status.keys():
            for state in states:
                if mode == state:
                    member_status[mode] = True
                elif mode == 'disabled' and state == 'absent':
                    member_status[mode] = True

        for member in mybalancer.members:
            if str(member.host) == str(module.params['member_host']):
                member_exists = True
                if module.params['state'] is not None:
                    member_status_before = member.status
                    if not module.check_mode:
                        member_status_after = member.status = member_status
                    else:
                        member_status_after = member_status
                    if member_status_before != member_status_after:
                        changed = True
                json_output = {
                    "host": member.host,
                    "status": member.status,
                    "protocol": member.protocol,
                    "port": member.port,
                    "path": member.path,
                    "attributes": member.attributes,
                    "management_url": member.management_url,
                    "balancer_url": member.balancer_url
                }
        if member_exists:
            module.exit_json(
                changed=changed,
                member=json_output
                )
        else:
            module.fail_json(msg=str(module.params['member_host']) + ' is not a member of the balancer ' + str(module.params['balancer_vhost']) + '!')

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url
if __name__ == '__main__':
    main()
