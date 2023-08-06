# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ndcc']

package_data = \
{'': ['*'], 'ndcc': ['data/*']}

install_requires = \
['pandas>=1.4.3,<2.0.0',
 'prompt-toolkit>=3.0.30,<4.0.0',
 'rich>=12.5.1,<13.0.0']

entry_points = \
{'console_scripts': ['ndcc = ndcc.main:main']}

setup_kwargs = {
    'name': 'ndcc',
    'version': '0.2.0',
    'description': 'tba',
    'long_description': '# ndcc - NFL Draft Capital Comparator\n\nA simple CLI App\n to compare the value\n of up to 32 NFL draft pick collections\n with one another.\n This can be useful when trying to determine\n which team in the draft has the most draft capital,\n or by how much a team increased\n or decreased their capital\n with their draft day (pick) trades.\n The most obvious use case however is to determine\n who won a pick trade according to different value charts.\n\nFor now,\n these are the charts one can choose between to determine value:\n\n* [Jimmy Johnson](https://www.drafttek.com/nfl-trade-value-chart.asp)\n* [Rich Hill](https://www.drafttek.com/NFL-Trade-Value-Chart-Rich-Hill.asp)\n* [Fitzgerald/Spielberger](https://overthecap.com/draft-trade-value-chart/)\n* [Kevin Meers (Harvard Sports Analysis)](https://harvardsportsanalysis.wordpress.com/2011/11/30/how-to-value-nfl-draft-picks/)\n* [PFF WAR](https://www.pff.com/news/draft-pff-data-study-breaking-down-every-nfl-teams-draft-capital-jacksonville-jaguars)\n* [Michael Lopez (blended curve)](https://statsbylopez.netlify.app/post/rethinking-draft-curve/)\n* [Chase Stuart](http://www.footballperspective.com/draft-value-chart/)\n\nTo account for drafts with a lot of compensatory picks,\n each chart is "prolonged" to 270 picks,\n using estimates on what the remaining values would be.\n\n## installation\n\n```sh\npip install ndcc\n```\n\n## usage\n\n```sh\npython -m ndcc\n```\n\n## adding charts\n\nTo add another chart,\n simply add a column in charts.csv,\n fill in the values\n and add the column name\n and chart name\n you want to be presented with\n to the values\n (and default_values,\n if you want the chart to be selected by default)\n of the checkboxlist_dialog\n in input.get_selected_charts().\n',
    'author': 'iron3oxide',
    'author_email': 'jason.hottelet@tuta.io',
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
