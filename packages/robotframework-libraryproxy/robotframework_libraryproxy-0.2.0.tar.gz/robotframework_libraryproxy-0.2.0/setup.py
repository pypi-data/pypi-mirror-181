# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['robotlibraryproxy']

package_data = \
{'': ['*']}

install_requires = \
['robotframework']

setup_kwargs = {
    'name': 'robotframework-libraryproxy',
    'version': '0.2.0',
    'description': 'Call RobotFramework keywords from Python',
    'long_description': '# robotframework-libraryproxy\n\nSimple library for calling RobotFramework keywords from Python, with the possibility to log them in the output.\n\nExample Python library:\n\n```python\nfrom Browser import Browser\nfrom robotlibraryproxy import library_proxy\n\ndef do_something_in_browser(self):\n    with library_proxy(Browser) as browser:\n        browser.new_browser(headless=False)\n        browser.new_page("https://example.com")\n        browser.click("text=More Information...")\n\n```\n\nor another way as python descriptor:\n\n```python\nfrom Browser import Browser\nfrom robotlibraryproxy import library_proxy\n\n\nclass Dummy:\n\n    browser: Browser = library_proxy()\n\n    def do_something_in_browser(self):\n        self.browser.new_browser(headless=False)\n        self.browser.new_page("https://example.com")\n        self.browser.click("text=More Information...")\n\n```\n\nExample Test case that uses this library:\n\n```robotframework\n*** Settings ***\n\nLibrary    Dummy.py\n\n# Library    Browser\n\n*** Test Cases ***\n\na simple test\n    Do Something In Browser\n\n```\n\nAn excerpt from the Robot log:\n\n\n![Example from robot log](doc/example_screenshot.png)\n\nmore comming soon...\n',
    'author': 'Daniel Biehl',
    'author_email': 'dbiehl@live.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/d-biehl/robotframework-libraryproxy',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
