# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nre_dtd']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1,<3.0.0',
 'rich>=12.6.0,<13.0.0',
 'shellingham>=1.5.0,<2.0.0',
 'typer>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['nre-dtd = nre_dtd:app']}

setup_kwargs = {
    'name': 'nre-dtd',
    'version': '1.1.1',
    'description': 'Download data from the NRE DTD',
    'long_description': '# nre-dtd\nA tool for downloading data from the National Rail Enquiries\' data feed.\n\nThis code is licensed under the WTFPL or the CC0 (at your discretion), but its output is not. Any NRE data included in the output of this program is subject to these [terms and conditions](https://opendata.nationalrail.co.uk/terms).\n\n## Useful links\n- [DTD](https://wiki.openraildata.com/index.php?title=DTD) on the Open Rail Data Wiki\n- [Fares and Associated Data Feed Interface Specification](https://www.raildeliverygroup.com/files/Publications/services/rsp/RSPS504502-00FaresandAssociatedDataFeedInterfaceSpecification.pdf) by the Rail Delivery Group\n- [National Routeing Guide Data Feed Specification](https://www.raildeliverygroup.com/files/Publications/services/rsp/RSPS504702-00NationalRoutingGuideDataFeedSpecification.pdf) by the Rail Delivery Group\n- [Timetable Information Data Feed Interface Specification](https://www.raildeliverygroup.com/files/Publications/services/rsp/RSPS5046_timetable_information_data_feed_interface_specification.pdf) by the Rail Delivery Group\n- [How to use the National Routeing Guide](http://datafeeds.rdg.s3.amazonaws.com/RSPS5047/nrg_instructions.pdf) by the Rail Delivery Group (not HTTPS)\n- [The National Routeing Guide in detail](http://datafeeds.rdg.s3.amazonaws.com/RSPS5047/nrg_detail.pdf) by the Rail Delivery Group (not HTTPS)\n\n## Get started\n### Get an account\n- Register for an account on the [National Rail Data Portal](https://opendata.nationalrail.co.uk/).\n- Subscribe to the Fares, Routeing and Timetable feed.\n\n### Use the tool\n#### From PyPI\n- Run `python3 -m pip install nre-dtd`.\n#### From source\n- Run `python3 -m pip install poetry` if you have not got Poetry.\n- Run `poetry init` to set up the environment.\n- Run `poetry shell` to enter the environment.\n- Or, prepend `poetry run --` to every command.\n\n### Examples\n#### Get usage instructions\n```sh\nnre-dtd --help\n```\n\n### Download everything\n```sh\nnre-dtd --fares <filename>.zip --routeing <filename>.zip --timetable <filename>.zip\n```\nThis will ask you for a password. The downloaded files are zipped.\n\n### Supply the username and password on the command line\n```sh\nnre-dtd --username sarah@example.com --password "correct-horse-battery-staple" <...>\n```\n\n![Powered by National Rail Enquiries](powered_by_nre.png)',
    'author': 'Sarah C',
    'author_email': '80788438+gltile-two-electric-boogaloo@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/gltrains/nre-dtd',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
