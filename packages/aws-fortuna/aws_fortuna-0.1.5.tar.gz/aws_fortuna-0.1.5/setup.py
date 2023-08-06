# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fortuna',
 'fortuna.calib_config',
 'fortuna.calib_model',
 'fortuna.calib_model.calib_config',
 'fortuna.calib_model.predictive',
 'fortuna.calibration',
 'fortuna.conformal',
 'fortuna.data',
 'fortuna.distribution',
 'fortuna.metric',
 'fortuna.model',
 'fortuna.model.model_manager',
 'fortuna.output_calibrator',
 'fortuna.output_calibrator.output_calib_manager',
 'fortuna.prob_model',
 'fortuna.prob_model.calib_config',
 'fortuna.prob_model.fit_config',
 'fortuna.prob_model.joint',
 'fortuna.prob_model.likelihood',
 'fortuna.prob_model.posterior',
 'fortuna.prob_model.posterior.deep_ensemble',
 'fortuna.prob_model.posterior.laplace',
 'fortuna.prob_model.posterior.map',
 'fortuna.prob_model.posterior.normalizing_flow',
 'fortuna.prob_model.posterior.normalizing_flow.advi',
 'fortuna.prob_model.posterior.swag',
 'fortuna.prob_model.predictive',
 'fortuna.prob_model.prior',
 'fortuna.prob_output_layer',
 'fortuna.training',
 'fortuna.utils']

package_data = \
{'': ['*']}

install_requires = \
['flax>=0.6.2,<0.7.0',
 'matplotlib>=3.6.2,<4.0.0',
 'numpy>=1.23.4,<2.0.0',
 'optax>=0.1.3,<0.2.0',
 'tensorflow-cpu>=2.11.0,<3.0.0',
 'tqdm>=4.64.1,<5.0.0']

extras_require = \
{'docs': ['Sphinx>=5.3.0,<6.0.0',
          'sphinx-autodoc-typehints>=1.19.5,<2.0.0',
          'nbsphinx>=0.8.10,<0.9.0',
          'nbsphinx-link>=1.3.0,<2.0.0',
          'sphinx-gallery>=0.11.1,<0.12.0',
          'pydata-sphinx-theme>=0.12.0,<0.13.0',
          'ipython>=8.7.0,<9.0.0']}

setup_kwargs = {
    'name': 'aws-fortuna',
    'version': '0.1.5',
    'description': 'A Library for Uncertainty Quantification.',
    'long_description': 'Fortuna\n#######\n\n.. image:: https://img.shields.io/pypi/status/Fortuna\n    :target: https://img.shields.io/pypi/status/Fortuna\n    :alt: PyPI - Status\n.. image:: https://img.shields.io/pypi/dm/aws-fortuna\n    :target: https://pypistats.org/packages/aws-fortuna\n    :alt: PyPI - Downloads\n.. image:: https://img.shields.io/pypi/v/aws-fortuna\n    :target: https://img.shields.io/pypi/v/aws-fortuna\n    :alt: PyPI - Version\n.. image:: https://img.shields.io/github/license/awslabs/Fortuna\n    :target: https://github.com/awslabs/Fortuna/blob/main/LICENSE\n    :alt: License\n.. image:: https://readthedocs.org/projects/aws-fortuna/badge/?version=latest\n    :target: https://aws-fortuna.readthedocs.io\n    :alt: Documentation Status\n\nA Library for Uncertainty Quantification\n========================================\nProper estimation of predictive uncertainty is fundamental in applications that involve critical decisions.\nUncertainty can be used to assess reliability of model predictions, trigger human intervention,\nor decide whether a model can be safely deployed in the wild.\n\nFortuna is a library for uncertainty quantification that makes it easy for users to run benchmarks and bring uncertainty to production systems.\nFortuna provides calibration and conformal methods starting from pre-trained models written in any framework,\nand it further supports several Bayesian inference methods starting from deep learning models written in `Flax <https://flax.readthedocs.io/en/latest/index.html>`_.\nThe language is designed to be intuitive for practitioners unfamiliar with uncertainty quantification,\nand is highly configurable.\n\nCheck the `documentation <https://aws-fortuna.readthedocs.io/en/latest/>`_ for a quickstart, examples and references.\n\nUsage modes\n===========\nFortuna offers three different usage modes:\n`From uncertainty estimates <https://github.com/awslabs/fortuna#from-uncertainty-estimates>`_,\n`From model outputs <https://github.com/awslabs/fortuna#from-model-outputs>`_ and\n`From Flax models <https://github.com/awslabs/fortuna#from-flax-models>`_.\nThese serve users according to the constraints dictated by their own applications.\nTheir pipelines are depicted in the following figure, each starting from one of the green panels.\n\n.. image:: https://github.com/awslabs/fortuna/raw/main/docs/source/_static/pipeline.png\n    :target: https://github.com/awslabs/fortuna/raw/main/docs/source/_static/pipeline.png\n\nFrom uncertainty estimates\n---------------------------\nStarting from uncertainty estimates has minimal compatibility requirements and it is the quickest level of interaction with the library.\nThis usage mode offers conformal prediction methods for both classification and regression.\nThese take uncertainty estimates in input,\nand return rigorous sets of predictions that retain a user-given level of probability.\nIn one-dimensional regression tasks, conformal sets may be thought as calibrated versions of confidence or credible intervals.\n\nMind that if the uncertainty estimates that you provide in inputs are inaccurate,\nconformal sets might be large and unusable.\nFor this reason, if your application allows it,\nplease consider the `From model outputs <https://github.com/awslabs/fortuna#from-model-outputs>`_ and\n`From Flax models <https://github.com/awslabs/fortuna#from-flax-models>`_ usage modes.\n\n**Example.** Suppose you want to calibrate credible intervals with coverage error :code:`error`,\neach corresponding to a different test input variable.\nWe assume that credible intervals are passed as arrays of lower and upper bounds,\nrespectively :code:`test_lower_bounds` and :code:`test_upper_bounds`.\nYou also have lower and upper bounds of credible intervals computed for several validation inputs,\nrespectively :code:`val_lower_bounds` and :code:`val_upper_bounds`.\nThe corresponding array of validation targets is denoted by :code:`val_targets`.\nThe following code produces *conformal prediction intervals*,\ni.e. calibrated versions of you test credible intervals.\n\n.. code-block:: python\n\n from fortuna.conformal.regression import QuantileConformalRegressor\n conformal_intervals = QuantileConformalRegressor().conformal_interval(\n      val_lower_bounds=val_lower_bounds, val_upper_bounds=val_upper_bounds,\n      test_lower_bounds=test_lower_bounds, test_upper_bounds=test_upper_bounds,\n      val_targets=val_targets, error=error)\n\nFrom model outputs\n------------------\nStarting from model outputs assumes you have already trained a model in some framework,\nand arrive to Fortuna with model outputs in :code:`numpy.ndarray` format for each input data point.\nThis usage mode allows you to calibrate your model outputs, estimate uncertainty,\ncompute metrics and obtain conformal sets.\n\nCompared to the `From uncertainty estimates <https://github.com/awslabs/fortuna#from-uncertainty-estimates>`_ usage mode,\nthis one offers better control,\nas it can make sure uncertainty estimates have been appropriately calibrated.\nHowever, if the model had been trained with classical methods,\nthe resulting quantification of model (a.k.a. epistemic) uncertainty may be poor.\nTo mitigate this problem, please consider the `From Flax models <https://github.com/awslabs/fortuna#from-flax-models>`_\nusage mode.\n\n**Example.**\nSuppose you have validation and test model outputs,\nrespectively :code:`val_outputs` and :code:`test_outputs`.\nFurthermore, you have some arrays of validation and target variables,\nrespectively :code:`val_targets` and :code:`test_targets`.\nThe following code provides a minimal classification example to get calibrated predictive entropy estimates.\n\n.. code-block:: python\n\n  from fortuna.calib_model import CalibClassifier\n  calib_model = CalibClassifier()\n  status = calib_model.calibrate(outputs=val_outputs, targets=val_targets)\n  test_entropies = calib_model.predictive.entropy(outputs=test_outputs)\n\nFrom Flax models\n--------------------------\nStarting from Flax models has higher compatibility requirements than the\n`From uncertainty estimates <https://github.com/awslabs/fortuna#from-uncertainty-estimates>`_\nand `From model outputs <https://github.com/awslabs/fortuna#from-model-outputs>`_ usage modes,\nas it requires deep learning models written in `Flax <https://flax.readthedocs.io/en/latest/index.html>`_.\nHowever, it enables you to replace standard model training with scalable Bayesian inference procedures,\nwhich may significantly improve the quantification of predictive uncertainty.\n\n**Example.** Suppose you have a Flax classification deep learning model :code:`model` from inputs to logits, with output\ndimension given by :code:`output_dim`. Furthermore,\nyou have some training, validation and calibration TensorFlow data loader :code:`train_data_loader`, :code:`val_data_loader`\nand :code:`test_data_loader`, respectively.\nThe following code provides a minimal classification example to get calibrated probability estimates.\n\n.. code-block:: python\n\n  from fortuna.data import DataLoader\n  train_data_loader = DataLoader.from_tensorflow_data_loader(train_data_loader)\n  calib_data_loader = DataLoader.from_tensorflow_data_loader(val_data_loader)\n  test_data_loader = DataLoader.from_tensorflow_data_loader(test_data_loader)\n\n  from fortuna.prob_model import ProbClassifier\n  prob_model = ProbClassifier(model=model)\n  status = prob_model.train(train_data_loader=train_data_loader, calib_data_loader=calib_data_loader)\n  test_means = prob_model.predictive.mean(inputs_loader=test_data_loader.to_inputs_loader())\n\n\nInstallation\n============\n**NOTE:** Before installing Fortuna, you are required to `install JAX <https://github.com/google/jax#installation>`_ in your virtual environment.\n\nYou can install Fortuna by typing\n\n.. code-block::\n\n    pip install aws-fortuna\n\nAlternatively, you can build the package using `Poetry <https://python-poetry.org/docs/>`_.\nIf you choose to pursue this way, first install Poetry and add it to your PATH\n(see `here <https://python-poetry.org/docs/#installation>`_). Then type\n\n.. code-block::\n\n    poetry install\n\nAll the dependecies will be installed at their required versions.\nIf you also want to install the optional Sphinx dependencies to build the documentation,\nadd the flag :code:`-E docs` to the command above.\nFinally, you can either access the virtualenv that Poetry created by typing :code:`poetry shell`,\nor execute commands within the virtualenv using the :code:`run` command, e.g. :code:`poetry run python`.\n\nExamples\n========\nSeveral usage examples are found in the\n`/examples <https://github.com/awslabs/fortuna/tree/main/examples>`_\ndirectory.\n\nContributing\n============\nIf you wish to contribute to the project, please refer to our `contribution guidelines <https://github.com/awslabs/fortuna/blob/main/CONTRIBUTING.md>`_.\n\n\nLicense\n=======\nThis project is licensed under the Apache-2.0 License.\nSee `LICENSE <https://github.com/awslabs/fortuna/blob/main/LICENSE>`_ for more information.\n',
    'author': 'Gianluca Detommaso',
    'author_email': 'gianluca.detommaso@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
