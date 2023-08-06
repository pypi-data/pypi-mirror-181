# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wildboottest']

package_data = \
{'': ['*']}

install_requires = \
['numba==0.56.3',
 'numpy>=1.18,<1.22',
 'pandas>=1.4,<2.0',
 'pytest>=3.0,<4.0',
 'statsmodels>=0.13,<0.14',
 'tabulate>=0.9.0,<0.10.0']

setup_kwargs = {
    'name': 'wildboottest',
    'version': '0.1.6',
    'description': 'Wild Cluster Bootstrap Inference for Linear Models in Python',
    'long_description': '## wildboottest\n\n![PyPI](https://img.shields.io/pypi/v/wildboottest?label=pypi%20package)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/wildboottest)\n\n`wildboottest` implements multiple fast wild cluster\nbootstrap algorithms as developed in [Roodman et al\n(2019)](https://econpapers.repec.org/paper/qedwpaper/1406.htm) and\n[MacKinnon, Nielsen & Webb\n(2022)](https://www.econ.queensu.ca/sites/econ.queensu.ca/files/wpaper/qed_wp_1485.pdf).\n\nIt has similar, but more limited functionality than Stata\'s [boottest](https://github.com/droodman/boottest), R\'s [fwildcusterboot](https://github.com/s3alfisc/fwildclusterboot) or Julia\'s [WildBootTests.jl](https://github.com/droodman/WildBootTests.jl). It supports\n\n-   The wild cluster bootstrap for OLS ([Cameron, Gelbach & Miller 2008](https://direct.mit.edu/rest/article-abstract/90/3/414/57731/Bootstrap-Based-Improvements-for-Inference-with),\n    [Roodman et al (2019)](https://econpapers.repec.org/paper/qedwpaper/1406.htm)).\n-   Multiple new versions of the wild cluster bootstrap as described in\n    [MacKinnon, Nielsen & Webb (2022)](https://www.econ.queensu.ca/sites/econ.queensu.ca/files/wpaper/qed_wp_1485.pdf), including the WCR13, WCR31, WCR33,\n    WCU13, WCU31 and WCU33.\n-   CRV1 and CRV3 robust variance estimation, including the CRV3-Jackknife as \n    described in [MacKinnon, Nielsen & Webb (2022)](https://arxiv.org/pdf/2205.03288.pdf).\n    \nAt the moment, `wildboottest` only computes wild cluster bootstrapped *p-values*, and no confidence intervals. \n\nOther features that are currently not supported: \n\n- The (non-clustered) wild bootstrap for OLS ([Wu, 1986](https://projecteuclid.org/journals/annals-of-statistics/volume-14/issue-4/Jackknife-Bootstrap-and-Other-Resampling-Methods-in-Regression-Analysis/10.1214/aos/1176350142.full)).\n-   The subcluster bootstrap ([MacKinnon and Webb 2018](https://academic.oup.com/ectj/article-abstract/21/2/114/5078969?login=false)).\n-   Confidence intervals formed by inverting the test and iteratively\n    searching for bounds.\n-   Multiway clustering.\n\n\nDirect support for [statsmodels](https://github.com/statsmodels/statsmodels) and \n[linearmodels](https://github.com/bashtage/linearmodels) is work in progress.\n\nIf you\'d like to cooperate, either send us an \n[email](alexander-fischer1801@t-online.de) or comment in the issues section!\n\n## Installation \n\nYou can install `wildboottest` from [PyPi](https://pypi.org/project/wildboottest/) by running \n\n```\npip install wildboottest\n```\n\n## Example \n\n```python\nfrom wildboottest.wildboottest import wildboottest\nimport statsmodels.api as sm\nimport numpy as np\nimport pandas as pd\n\n# create data\nnp.random.seed(12312312)\nN = 1000\nk = 10\nG = 25\nX = np.random.normal(0, 1, N * k).reshape((N,k))\nX = pd.DataFrame(X)\nX.rename(columns = {0:"X1"}, inplace = True)\nbeta = np.random.normal(0,1,k)\nbeta[0] = 0.005\nu = np.random.normal(0,1,N)\nY = 1 + X @ beta + u\ncluster = np.random.choice(list(range(0,G)), N)\n\n# estimation\nmodel = sm.OLS(Y, X)\n\nwildboottest(model, param = "X1", cluster = cluster, B = 9999, bootstrap_type = "11")\n#   param              statistic   p-value\n# 0    X1  [-1.0530803154504016]  0.308831\n\nwildboottest(model, param = "X1", cluster = cluster, B = 9999, bootstrap_type = "31")\n#   param              statistic   p-value\n# 0    X1  [-1.0530803154504016]  0.307631\n\nwildboottest(model, param = "X1", cluster = cluster, B = 9999, bootstrap_type = "33")\n#   param              statistic   p-value\n# 0    X1  [-1.0394791020434824]  0.294286\n\n\nwildboottest(model, cluster = cluster, B = 9999)\n#   param              statistic   p-value\n# 0    X1  [-1.0530803154504016]  0.315132\n# 1     1    [-18.5149486170657]  0.000000\n# 2     2    [7.831855813581191]  0.000000\n# 3     3   [-16.85188951397906]  0.000000\n# 4     4  [-12.721095348008182]  0.000000\n# 5     5    [1.200524160940055]  0.243624\n# 6     6    [6.870946666836135]  0.000000\n# 7     7   [-31.31653422266621]  0.000000\n# 8     8    [10.26443257212472]  0.000000\n# 9     9  [-20.650361366939535]  0.000000\n```\n',
    'author': 'Alexander Fischer',
    'author_email': 'alexander-fischer1801@t-online.de',
    'maintainer': 'Aleksandr Michuda',
    'maintainer_email': 'amichuda@gmail.com',
    'url': 'https://github.com/s3alfisc/wildboottest',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
