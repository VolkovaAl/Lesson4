#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.basic import AnsibleModule
import requests

DOCUMENTATION = r'''
---
module: healthcheck
author: Pupkin V.
short_description: healthcheck of site
description:
  - healthcheck of site with or without TLS
version_added: 1.0.0
requirements:
  - requests
  - python >= 3.6
options:
  addr:
    description:
      - Address of site we want to check
      - This is a required parameter
    type: str
  tls:
    description:
      - Whether site using certificates or not
      - Default value is 'True'
    type: bool
'''

EXAMPLES = r'''
- name: Check availability of site
  healthcheck:
    addr: mysite.example
  connection: local

- name: Check availability of site without certs
  healthcheck:
    addr: mysite.example
    tls: false
  connection: local
'''

RETURN = r'''
msg:
  description: Errors if occured
  returned: always
  type: str
  sample: ""
site_status:
  description: State status
  returned: always
  type: str
  sample: Available
rc:
  description: Return code
  returned: always
  type: int
  sample: 200
'''

def return_status(str1,str2):
    failed = False
    msg = "Status checked successfully"
    try:
        if str2 == False:
            site_status = requests.head("http://" + str1).reason
            rc = requests.head("http://" + str1).status_code
            if rc != 200:
                failed = True
                msg = "The check was executed with an error"
        else: 
            site_status = requests.head("https://" + str1,verify=False).reason
            rc = requests.head("https://" + str1,verify=False).status_code
            if rc != 200:
                failed = True
                msg = "The check was executed with an error"
    except requests.exceptions.RequestException as e:
        failed = True
        msg = "The IP address is incorrectly formatted or unreachable"
        rc = 0
        site_status = " "
    

    return(failed, site_status, rc, msg)

def main():
    # Аргументы для модуля
    arguments = dict(
        addr=dict(required=True, type='str'),
        tls=dict(type='bool', default="True")
    )
    # Создаем объект - модуль
    module = AnsibleModule(
        argument_spec=arguments,
        supports_check_mode=False
    )
    # Получаем аргументы
    addr = module.params["addr"]
    tls = module.params["tls"]
    # Вызываем нашу функцию
    lc_return = return_status(addr,tls)
    # Если задача зафейлилась
    if lc_return[0]:
        module.fail_json(changed=False,
                         failed=lc_return[0],
                         site_status=lc_return[1],
                         rc=lc_return[2],
                         msg=lc_return[3])
    # Если задача успешно завершилась
    else:
        module.exit_json(changed=False,
                         failed=lc_return[0],
                         site_status=lc_return[1],
                         rc=lc_return[2],
                         msg=lc_return[3])


if __name__ == "__main__":
    main()