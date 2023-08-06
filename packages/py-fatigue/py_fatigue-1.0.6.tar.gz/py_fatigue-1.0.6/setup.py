# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py_fatigue',
 'py_fatigue.cycle_count',
 'py_fatigue.damage',
 'py_fatigue.geometry',
 'py_fatigue.material',
 'py_fatigue.mean_stress',
 'py_fatigue.stress_range']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.5,<4.0',
 'numba>=0.56,<0.57',
 'numpy>=1.21,<2.0',
 'pandas>=1.4,<2.0',
 'plotly>=5.6,<6.0',
 'pydantic>=1.10.2,<2.0.0']

setup_kwargs = {
    'name': 'py-fatigue',
    'version': '1.0.6',
    'description': 'py-fatigue bundles the main functionality for performing cyclic stress (fatigue) analysis and cycle-counting.',
    'long_description': 'It provides:\n\n- a powerful cycle-counting implementation based on the ASTM E1049-85 rainflow method that retrieves the main class of the package: ``CycleCount``\n- capability of storing the ``CycleCount`` results in a sparse format for storage and memory efficiency\n- easy applicability of multiple mean stress effect correction models\n- implementation of low-frequency fatigue recovery when "summing" multiple ``CycleCount`` instances\n- fatigue analysis through the combination of SN curves and multiple damage accumulation models\n- crack propagation analysis through the combination of the Paris\' law and multiple crack geometries\n- and more...\n\nPy-Fatigue is heavily based on [``numba``](https://numba.pydata.org/), [``numpy``](https://numpy.org/) and [``pandas``](https://pandas.pydata.org/), for the analytical part, and [``matplotlib``](https://matplotlib.org/) for the plotting part.\n\n## To cite Py-Fatigue\n\nIf you use Py-Fatigue in your research, please cite the following paper:\n\n### BibTeX-style\n\n```tex\n@misc{dantuono-2022,\n\tauthor = {given-i=P.D., given=Pietro, family=D\'Antuono and given-i=W.W., given=Wout, family=Weijtjens and given-i=C.D., given=Christof, family=Devriendt},\n\tpublisher = {https://www.owi-lab.be/},\n\ttitle = {{Py-Fatigue}},\n\tyear = {2022},\n\turl = {https://owi-lab.github.io/py_fatigue},\n}\n```\n\n### BibLaTeX-style\n\n```tex\n@software{dantuono-2022,\n\tauthor = {given-i=P.D., given=Pietro, family=D\'Antuono and given-i=W.W., given=Wout, family=Weijtjens and given-i=C.D., given=Christof, family=Devriendt},\n\tdate = {2022},\n\tlanguage = {english},\n\tpublisher = {https://www.owi-lab.be/},\n\ttitle = {Py-Fatigue},\n\ttype = {software},\n\turl = {https://owi-lab.github.io/py_fatigue},\n\tversion = {1.0.3},\n}\n```\n\n### APA 7-style\n\n```\nD’Antuono, P. D., Weijtjens, W. W., & Devriendt, C. D. (2022). Py-Fatigue [Software]. In Github (1.0.3). https://www.owi-lab.be/. https://owi-lab.github.io/py_fatigue\n```\n\n## License\n\nThe package is licensed under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html).\n',
    'author': "Pietro D'Antuono",
    'author_email': 'pietro.dantuono@vub.be',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/owi-lab/py_fatigue',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
