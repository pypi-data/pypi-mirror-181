# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stochvolmodels',
 'stochvolmodels.data',
 'stochvolmodels.pricers',
 'stochvolmodels.pricers.core',
 'stochvolmodels.pricers.logsv',
 'stochvolmodels.tests',
 'stochvolmodels.utils']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.5.2',
 'numba>=0.55',
 'numpy>=1.22.4',
 'pandas>=0.19',
 'scipy>=1.3',
 'seaborn>=0.11.2',
 'statsmodels>=0.13.0']

setup_kwargs = {
    'name': 'stochvolmodels',
    'version': '1.0.4',
    'description': 'Implementation of stochastic volatility models for option pricing',
    'long_description': '# StochVolModels\nImplement pricing analytics and Monte Carlo simulations for stochastic volatility models including log-normal SV model and Heston SV model\nThe analytics for the lognormal is based on the paper\n\n[Log-normal Stochastic Volatility Model with Quadratic Drift: Applications to Assets with Positive Return-Volatility Correlation and to Inverse Martingale Measures](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2522425) by Artur Sepp and Parviz Rakhmonov\n\n\n# Table of contents\n1. [Model Interface](#introduction)\n    1. [Log-normal stochastic volatility model](#logsv)\n    2. [Heston stochastic volatility model](#hestonsv)\n3. [Running log-normal SV pricer](#paragraph1)\n    1. [Computing model prices and vols](#subparagraph1)\n   2. [Running model calibration to sample Bitcoin options data](#subparagraph2)\n   3. [Running model calibration to sample Bitcoin options data](#subparagraph3)\n4. [Analysis and figures for the paper](#paragraph2)\n\n\nRunning model calibration to sample Bitcoin options data\n\n## Model Interface <a name="introduction"></a>\nThe package provides interfaces for a generic volatility model with the following features.\n1) Interface for analytical pricing of vanilla options using Fourier transform with closed-form solution for moment generating function\n2) Interface for Monte-Carlo simulations of model dynamics\n3) Interface for visualization of model implied volatilities\n\nThe model interface is in stochvolmodels/pricers/model_pricer.py\n\n### Log-normal stochastic volatility model <a name="logsv"></a>\n\nImplementation of Lognormal SV model is based on paper https://github.com/ArturSepp/StochVolModels/blob/main/docs/lognormal_stoch_vol_paper.pdf\n\n\nThe dynamics of the log-normal stochastic volatility model:\n\n$$dS_{t}=r(t)S_{t}dt+\\sigma_{t}S_{t}dW^{(0)}_{t}$$\n\n$$d\\sigma_{t}=\\left(\\kappa_{1} + \\kappa_{2}\\sigma_{t} \\right)(\\theta - \\sigma_{t})dt+  \\beta  \\sigma_{t}dW^{(0)}_{t} +  \\varepsilon \\sigma_{t} dW^{(1)}_{t}$$\n\n$$dI_{t}=\\sigma^{2}_{t}dt$$\n\nwhere $r(t)$ is the deterministic risk-free rate; $W^{(0)}_{t}$ and $W^{(1)}_t$  are uncorrelated Brownian motions, $\\beta\\in\\mathbb{R}$ is the volatility beta which measures the sensitivity of the volatility to changes in the spot price, and $\\varepsilon>0$ is the volatility of residual volatility. We denote by $\\vartheta^{2}$, $\\vartheta^{2}=\\beta^{2}+\\varepsilon^{2}$, the total instantaneous variance of the volatility process.\n\n\nImplementation of Lognormal SV model is contained in stochvolmodels/pricers/logsv_pricer.py\n\n\n### Heston stochastic volatility model <a name="hestonsv"></a>\n\nThe dynamics of Heston stochastic volatility model:\n\n$$dS_{t}=r(t)S_{t}dt+\\sqrt{V_{t}}S_{t}dW^{(S)}_{t}$$\n\n$$dV_{t}=\\kappa (\\theta - V_{t})dt+  \\vartheta  \\sqrt{V_{t}}dW^{(V)}_{t}$$\n\nwhere  $W^{(S)}$ and $W^{(V)}$ are correlated Brownian motions with correlation parameter $\\rho$\n\nImplementation of Heston SV model is contained in stochvolmodels/pricers/heston_pricer.py\n\n\n## Running log-normal SV pricer <a name="paragraph1"></a>\n\nBasic features are implemented in examples/run_lognormal_sv_pricer.py\n\n\n### Computing model prices and vols <a name="subparagraph1"></a>\n\n```python \n# instance of pricer\nlogsv_pricer = LogSVPricer()\n\n# define model params    \nparams = LogSvParams(sigma0=1.0, theta=1.0, kappa1=5.0, kappa2=5.0, beta=0.2, volvol=2.0)\n\n# 1. compute ne price\nmodel_price, vol = logsv_pricer.price_vanilla(params=params,\n                                             ttm=0.25,\n                                             forward=1.0,\n                                             strike=1.0,\n                                             optiontype=\'C\')\nprint(f"price={model_price:0.4f}, implied vol={vol: 0.2%}")\n\n# 2. prices for slices\nmodel_prices, vols = logsv_pricer.price_slice(params=params,\n                                             ttm=0.25,\n                                             forward=1.0,\n                                             strikes=np.array([0.9, 1.0, 1.1]),\n                                             optiontypes=np.array([\'P\', \'C\', \'C\']))\nprint([f"{p:0.4f}, implied vol={v: 0.2%}" for p, v in zip(model_prices, vols)])\n\n# 3. prices for option chain with uniform strikes\noption_chain = OptionChain.get_uniform_chain(ttms=np.array([0.083, 0.25]),\n                                            ids=np.array([\'1m\', \'3m\']),\n                                            strikes=np.linspace(0.9, 1.1, 3))\nmodel_prices, vols = logsv_pricer.compute_chain_prices_with_vols(option_chain=option_chain, params=params)\nprint(model_prices)\nprint(vols)\n```\n\n\n### Running model calibration to sample Bitcoin options data  <a name="subparagraph2"></a>\n```python \nbtc_option_chain = chains.get_btc_test_chain_data()\nparams0 = LogSvParams(sigma0=0.8, theta=1.0, kappa1=5.0, kappa2=None, beta=0.15, volvol=2.0)\nbtc_calibrated_params = logsv_pricer.calibrate_model_params_to_chain(option_chain=btc_option_chain,\n                                                                    params0=params0,\n                                                                    constraints_type=ConstraintsType.INVERSE_MARTINGALE)\nprint(btc_calibrated_params)\n\nlogsv_pricer.plot_model_ivols_vs_bid_ask(option_chain=btc_option_chain,\n                               params=btc_calibrated_params)\n```\n![image info](docs/figures/btc_fit.PNG)\n\n\n\n### Comparision of model prices vs MC  <a name="subparagraph2"></a>\n```python \nbtc_option_chain = chains.get_btc_test_chain_data()\nuniform_chain_data = OptionChain.to_uniform_strikes(obj=btc_option_chain, num_strikes=31)\nbtc_calibrated_params = LogSvParams(sigma0=0.8327, theta=1.0139, kappa1=4.8609, kappa2=4.7940, beta=0.1988, volvol=2.3694)\nlogsv_pricer.plot_comp_mma_inverse_options_with_mc(option_chain=uniform_chain_data,\n                                                  params=btc_calibrated_params,\n                                                  nb_path=400000)\n                                           \n```\n![image info](docs/figures/btc_mc_comp.PNG)\n\n\n## Analysis and figures for the paper <a name="paragraph3"></a>\n\nAll figures shown in the paper can be reproduced using py scripts in examples/plots_for_paper\n',
    'author': 'Artur Sepp',
    'author_email': 'artursepp@gmail.com',
    'maintainer': 'Artur Sepp',
    'maintainer_email': 'artursepp@gmail.com',
    'url': 'https://github.com/ArturSepp/StochVolModels',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
