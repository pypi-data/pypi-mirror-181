# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['byproxy']

package_data = \
{'': ['*']}

install_requires = \
['requests==2.28.1']

setup_kwargs = {
    'name': 'byproxy',
    'version': '0.1.2',
    'description': 'ByProxy is a library to generate proxy dictionaries from a list of urls and gain information about the proxies.',
    'long_description': "# ByProxy\n\nByProxy is a simple package contains simple tools for proxy management and usage. You can generate proxy dictionaries from a list of urls and gain information about the proxies.\n\n- It has two main classes:\n  - ProxyChecker:\n    - It requires Session object to make requests.\n    - It helps us to gain information about our proxies.\n    - check_my_ip is a method which basically sends a requests to the httpbin.org/ip and returns a dictionary.\n    - target_ip_details is a method that sends requests to demo.ip-api.com to check the details of the target ip.\n      - Be carefull when using this method, I aim no harm to the ip-api's servers. It's just a helper method for me to find out the details of the target ip. If you are going to use this method frequently, please consider purchasing a subscription from ip-api. I am not responsible for any damage caused by using this method.\n    - check_target_url is a method that sends a get request to the target url to check if the proxy is working with the target url.\n  - ProxyMaker:\n    - It doesn't require any arguments.\n    - It helps us to prepare the proxy dictionary.\n- Todos:\n  - [x] Implement a ProxyChecker class to check the proxies.\n    - [x] Implement a check_my_ip method to verify the ip of the proxy.\n    - [x] Implement a check_target_url method to verify if the proxy is working with the target url.\n    - [x] Implement a target_ip_details method to get more information about the target ip.\n  - [x] Implement a ProxyMaker class to prepare the proxy dictionary.\n    - [x] Implement a read_lines method to read the lines from a file with given path and returns a list.\n    - [x] Implement a split_lines method to split the lines from the list. It takes two arguments, lines and separator. It returns a list of lists.\n    - [x] Implement a lines_to_dict method to convert the list of lists to a dictionary. It takes two arguments, lines and keys.\n    - [x] Implement a make_proxies method to make the proxy dictionary. It takes three arguments, lines, type and password_enabled. It returns a dictionary of proxies which you can use with requests.Session object.\n",
    'author': 'uykusuz',
    'author_email': 'vimevim@gmail.com',
    'maintainer': 'uykusuz',
    'maintainer_email': 'vimevim@gmail.com',
    'url': 'https://github.com/vimevim/byproxy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '==3.8.8',
}


setup(**setup_kwargs)
