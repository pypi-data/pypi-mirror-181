# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['omars_analysis']

package_data = \
{'': ['*'], 'omars_analysis': ['data/*']}

install_requires = \
['numpy>=1.23.5,<2.0.0', 'scipy>=1.9.3,<2.0.0']

setup_kwargs = {
    'name': 'omars-analysis',
    'version': '0.1.3',
    'description': '',
    'long_description': "# Documentation for package omars-analysis\n\nThis package has one function 'get_omars_analysis'\n\nFirst run the following:\n\n```python\nfrom omars_analysis.main import get_omars_analysis\n```\n\nRunning the above command will make the function 'get_omars_analysis' available for use.\n\n## Function usage\n\nThe function requires six inputs:\n\n- mat\n  \n  the first input is the design matrix. The design matrix need not be coded, however it must only consist of continuous variables. The function is meant to be used with designs that have all factors either with two levels or three levels. The design should **NOT** consist of headers. The design matrix should not consist of second order effects since this will be built internally in the function.\n- cy\n  \n  This is the response.\n\n- qheredity\n  \n  This is to specify heredity constraints for quadratic effects. The accepted inputs are 'y' or 'n' ('y'- strong heredity, 'n'- no heredity, 'n'- No heredity). The input must be a string in lowercase.\n- iheredity\n  \n  This is to specify heredity constraints for two-factor interaction effects. The accepted inputs are 's', 'w' or 'n' ('s'- strong heredity, 'w'- weak heredity, 'n'- no heredity). The input must be a string in lowercase.\n\n- effects_to_drop\n  \n  This is to specify second order effects that must be excluded from the analysis. The input must be a list of strings. For example: ['1_1', '2_3']. This input specifies that the quadratic effect of the first factor and the interaction effect between factor two and three must be excluded from the second step of the analysis (subset selection).\n\n- full\n  \n  'n' -  analysis is performed on the main effects only\n  \n  'y' - analysis is performed on the main effects and second order effects.\n\n  The default is set to 'y'\n\n## Output\n\nThe function will auttomatically print out the following:\n\n- Initial error degrees of freedom available\n- The initial estimate of the error variance\n- Main effects that are active\n- Updated estimate of the error variance\n- Active interaction effects\n- Active quadratic effects\n\nThe function outputs one return value. This value is the p-value from the last failed F-test during the second order effects selection.\n\n## Example code\n\n```python\noutput = get_omars_analysis(mat=design_matrix, cy=response, qheredity='n', iheredity='n', effects_to_drop=[], full='y')\n```\n",
    'author': 'Mohammed Saif Ismail Hameed',
    'author_email': 'saifismailh@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/saif-ismail/omars_analysis/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
