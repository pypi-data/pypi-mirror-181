# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['newgrok',
 'newgrok.cli',
 'newgrok.modules.process_manager',
 'newgrok.modules.telegram']

package_data = \
{'': ['*']}

install_requires = \
['pytelegrambotapi>=4.8.0,<5.0.0',
 'python-dotenv>=0.21.0,<0.22.0',
 'requests>=2.28.1,<3.0.0']

entry_points = \
{'console_scripts': ['chat_id = newgrok.cli.chat:get_chat_id']}

setup_kwargs = {
    'name': 'newgrok',
    'version': '0.4.0',
    'description': 'Keep ngrok free tier alive',
    'long_description': '<p align="center">\n  <a href="https://user-images.githubusercontent.com/101568457/208002599-be7000ca-e05a-4706-99b2-49bc5a35e367.png"><img src="https://user-images.githubusercontent.com/101568457/208002599-be7000ca-e05a-4706-99b2-49bc5a35e367.png" alt="FastAPI"></a>\n</p>\n<p align="center">\n    <em>Keep your ngrok free tier alive, forever</em>\n</p>\n\n---\n<h1>\n! Use this tool for personal use only, for prototyping projects and related things. For commercial or production use consider subscribing to ngrok.\n</h1>\n\n## Prerequisites\n* Ngrok already configured with your key\n* A bot on telegram\n---\n## installation\n\n* With pip\n    ```\n    pip3 newgrok\n    ```\n\n* With poetry:\n\n    ```\n    poetry add newgrok\n    ```\n---\n## Variables\n| Variable  |                                                 |\n|-----------|-------------------------------------------------|\n| app_port  | Port of the application running on your machine |\n| protocol  | Network protocol you want to use                |\n| bot_token | Your bot token in telegram                      |\n| chat_id   | The id of the chat between the bot and you      |\n---\n## Setup\n\n* First you need to set the environment variables, chat_id for later, edit the ```.env``` file\n    ```python\n    app_port=8000\n    protocol=http\n    bot_token=******************************\n    chat_id=\n    ```\n* To get the chat_id, run:\n    ```\n    chat_id\n    ```\n    Now send a message to the bot, and it will reply with the chat_id. Complete the ```.env``` file\n    ```python\n    app_port=8000\n    protocol=http\n    bot_token=******************************\n    chat_id=********\n    ```\n* Now with these 3 lines of code, newgrok is already running, enjoy\n    ```python\n    from newgrok import Newgrok\n\n    ngrok = Newgrok()\n    ngrok.run()\n    ```\n',
    'author': 'Adrien',
    'author_email': 'adrienv.sui@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
