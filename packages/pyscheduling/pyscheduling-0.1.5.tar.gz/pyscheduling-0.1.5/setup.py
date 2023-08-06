# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pyscheduling',
 'pyscheduling.FS',
 'pyscheduling.JS',
 'pyscheduling.PMSP',
 'pyscheduling.SMSP']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.5.2,<4.0.0']

setup_kwargs = {
    'name': 'pyscheduling',
    'version': '0.1.5',
    'description': 'THE python package to solve scheduling problems',
    'long_description': '# pyscheduling\n\nTHE python package to solve scheduling problems\n\n## Installation\n\n```bash\n$ pip install pyscheduling\n```\n\n## Usage\n\n```python\nimport pyscheduling.SMSP.interface as sm\n\nproblem = sm.Problem()\nproblem.add_constraints([sm.Constraints.W,sm.Constraints.D])\nproblem.set_objective(sm.Objective.wiTi)\nproblem.generate_random(jobs_number=20,Wmax=10)\nsolution = problem.solve(problem.heuristics["ACT"])\nprint(solution)\n```\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`pyscheduling` was created by the scheduling-cc organization. CC-BY-NC-ND-4.0.',
    'author': 'Amine ATHMANI',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
