# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sphinx_modeling',
 'sphinx_modeling.modeling',
 'sphinx_modeling.modeling.work_in_progress']

package_data = \
{'': ['*']}

install_requires = \
['docutils>=0.18.1',
 'pydantic>=1.9.2,<2.0.0',
 'sphinx-needs>=1.0.1',
 'sphinx>=5.0',
 'sphinxcontrib-plantuml>=0.24,<0.25']

extras_require = \
{':python_version >= "3.7" and python_version < "3.8"': ['typing-extensions>=4.3.0,<5.0.0']}

setup_kwargs = {
    'name': 'sphinx-modeling',
    'version': '0.2.0',
    'description': 'Sphinx extension to enable modeling and set constraints for sphinx-needs',
    'long_description': '**Complete documentation**: https://sphinx-modeling.useblocks.com/\n\nIntroduction\n============\n\n``Sphinx-Modeling`` allows the definition of models and constraints for objects defined with\n`Sphinx-Needs <https://github.com/useblocks/sphinx-needs>`_. They can be validated during the Sphinx build.\n\n`pydantic <https://github.com/pydantic/pydantic>`_ is used under the hood to validate all models.\n\nArbitrary constraints can be enforced such as:\n\n- value constraints for need options\n- multiplicity of need link options\n- typed fields (string, regex, int, enums)\n- allow or disallow additional options\n- outgoing links must target specific need types or union of types\n- need type must be nested within another need type (via ``parent_need``)\n- need type must be part of a specific document or chapter/section\n- custom validators\n\n.. warning:: This Sphinx extension is in an early stage and subject to breaking changes.\n\nMotivation\n==========\n\nRequirements management with ``Sphinx-Needs`` and docs-as-code traditionally comes at the cost of complete freedom for developers. ``need_types``, ``needs_extra_options`` and ``needs_extra_links`` are global and all ``need_types`` can\nuse all ``needs_extra_options``/``needs_extra_links`` by default.\n\nThis is a problem for organizations that want to enforce well defined (UML) standards on objects.\nEspecially when migrating parts of the requirements management system to ``Sphinx-Needs`` it is crucial to be\nconsistent with existing solutions. Doing so enables technological interoperability.\n\nMore reasons to use sphinx-modeling are:\n\n* defining model constraints (typed links, multiplicity, allowed attributes, allowed values etc) as part of your model\n  definition (and not as `need_warnings`). This leaves `need_warnings` with the load of doing only data relevant checks\n  later. That is, reduce glue and duplication as much as possible.\n* automatic visualization of typed model (planned feature)\n* self contained need definitions which does not leave types, options, links and warnings scattered (planned feature)\n* user-documentation of meta-model (automatically create readable textual documentation on the types, its allowed\n  values etc. Can be combined with additional docstring documentation as part of model definition if needed)\n* possibility to use the typed model in external tools (VsCode Extension, Linter etc.)\n* possibility to auto-generate\n  `needs_ide_directive_snippets <https://sphinxcontrib-needs.readthedocs.io/en/latest/configuration.html#needs-ide-directive-snippets>`_ (planned feature)\n\n\nPlanned features\n================\n\n* Generation of the following ``Sphinx-Needs`` configurations from a model configuration:\n\n  * ``needs_types``\n  * ``needs_extra_options``\n  * ``needs_extra_links``\n\n* Visualization of the model (e.g. with PlantUML)\n* Use the model as source for IDE extensions\n\nInstallation\n============\n\nUsing poetry\n------------\n::\n\n    poetry add sphinx-modeling\n\n\nUsing pip\n---------\n::\n\n    pip install sphinx-modeling\n\nUsing sources\n-------------\n::\n\n    git clone https://github.com/useblocks/sphinx-modeling\n    cd sphinx-modeling\n    pip install .\n\nActivation\n----------\n\nAdd **sphinx_modeling** to your extensions::\n\n    extensions = ["sphinx_needs", "sphinx_modeling", ]\n',
    'author': 'team useblocks',
    'author_email': 'info@useblocks.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'http://github.com/useblocks/sphinx-modeling',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.2,<3.11',
}


setup(**setup_kwargs)
