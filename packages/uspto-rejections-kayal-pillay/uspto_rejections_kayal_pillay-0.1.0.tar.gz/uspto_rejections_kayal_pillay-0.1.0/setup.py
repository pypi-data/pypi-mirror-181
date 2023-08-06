# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['src', 'src.uspto_rejections_kayal_pillay', 'uspto_rejections_kayal_pillay']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'uspto-rejections-kayal-pillay',
    'version': '0.1.0',
    'description': 'Package to interact with the USPTO Rejections API',
    'long_description': '# uspto_rejections_kayal_pillay\n\nPackage to interact with the USPTO Rejections API (https://developer.uspto.gov/api-catalog/uspto-office-action-rejection-api)\n\n## Installation\n\n```bash\n$ pip install uspto_rejections_kayal_pillay\n```\n\n## Usage\n\nPresently existing packages for the US Patents and Trademarks Office (USPTO) deal with data involving accepted patents - e.g., https://pypi.org/project/pypatent/. This package specifically deals with patents that were rejected so that those intending to file future patents are well-informed. \n\nThe following functions can be found within this package:\na) all_patents: Returns Pandas DataFrame containing all patent information in API, including details such as rejection reason for each patent by default. User can request lower number of rows.\nb) year_seperator: Returns cleaned dataframe to be used in further analysis after splitting submission date (ddmmyyy + timezone) into a separate clean year column for data analysis.\nc) patent_reject: Returns dataframe showing all rejection details of that particular patent, including submission date and rejection reason, which is useful as in the API, some patent application numbers have numerous entries. Dataframe comes with clean submission year column.\nd) rejection_filter: Returns Pandas DataFrame containing all patent information for those patents rejected for reason in filter, with clean submission year column.\ne) rejection_graph: Returns line graph showing number of patents rejected for a particular reason over the years. \nf) type_rejections_crosstab: Returns Pandas DataFrame containing crosstab of the proportion of final rejections ("CTFR") and non-final rejections ("CTNF") in a given year. Allows user to customise whether they want crosstab normalised (in proportions) or in raw numbers.\ng) type_rejections_overall: Returns Pandas DataFrame containing crosstab of the proportion of final rejections ("CTFR") and non-final rejections ("CTNF") for all years in API, with breakdown of proportion per year. Allows user to customise whether they want crosstab normalised (in proportions) or in raw numbers.\nh) actiontype_bycategory: Returns Pandas DataFrame compiling all the entries for the requested action type category, as presently the API data has several variations in spelling for same category. This also has a clean year column based on submission date.\ni) actiontype_clean: Returns clean Pandas DataFrame changing all the entries for the action type to standardise forms, as presently the API data has several variations in spelling for same category. This also has a clean year column based on submission date.\n\nBelow is a 1:1 mapping of the various rejection terms used in the rejection reasons in the API, and their meaning:\n                    "headerMissing",                   :    does not include standard headings or contains no headings\n                    "formParagraphMissing",            :    does not contain the form paragraph(s) for the rejection(s) raised\n                    "rejectFormMissmatch",             :    form paragraph(s) do not match the rejection(s) raised in  action sentence(s)\n                    "closingMissing",                  :    examiner is to provide specific contact information at end - missing here\n                    "hasRej101",                       :    Title 35 of the United States Code, section 101 (35 U.S.C. §101) rejection \n                    "hasRejDP",                        :    non-statutory double patenting rejection\n                    "hasRej102",                       :    35 U.S.C. §102 rejection\n                    "hasRej103",                       :    35 U.S.C. §103 rejection\n                    "hasRej112",                       :    35 U.S.C. §112 rejection\n                    "hasObjection",                    :    whether an objection is raised\n                    "cite102GT1",                      :    Greater than One Citation in 102 Rejection\n                    "cite103GT3",                      :    Greater than Three Citations in 103 Rejection\n                    "cite103EQ1",                      :    One Citation in 103 Rejection\n                    "cite103Max"                       :    Maximum Citations in 103 Rejection\n\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`uspto_rejections_kayal_pillay` was created by Kayal Pillay (mmp2227). It is licensed under the terms of the MIT license.\n\n## Credits\n\n`uspto_rejections_kayal_pillay` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Kayal Pillay (mmp2227)',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/KayalPillay/uspto_rejections_kayal_pillay',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
