|travis-badge|_

.. |travis-badge| image:: https://travis-ci.com/IBM/pycloudmessenger.svg?branch=master
.. _travis-badge: https://travis-ci.com/IBM/pycloudmessenger/

========================
pycloudmessenger
========================

The purpose of this project is to provide sample code for interacting with various messaging based cloud platforms provided by IBM Research Europe - Dublin.


Prerequisites
---------------------------------

It is assumed that all development takes place in Python, using at least version 3.6.


Testing
---------------------------------

Unit tests are contained in the `tests <tests>`_ directory.

To run the unit tests, a local RabbitMQ container is launched automatically. Settings and credentials to match the latest RabbitMQ docker image are also provided. To run the test:

.. code-block:: bash

	creds=local.json make test 


Examples
---------------------------------

Sample code for basic messaging as well as federated learning and castor are contained in the `examples <examples>`_ directory. To run various samples, invoke the appropriate make target, as follows.

.. code-block:: bash

	# The basic messaging sample
	creds=local.json make basic

.. code-block:: bash

	# The federated learning sample (online, requires cloud credentials)

	python -m examples.ffl.register --credentials=<CLOUDCREDENTIALS> --user=<USER> --password=<PASSWORD> > credentials.json
	python -m examples.ffl.sample --credentials=credentials.json
	python -m examples.ffl.deregister --credentials=credentials.json

.. code-block:: bash

	# The castor sample
	creds=credentials.json make castor

**Note:** For online platforms, **<CLOUDCREDENTIALS>** must be available. Please request from the IBM team.


References 
---------------------------------

* [IBM Research Blog](https://www.ibm.com/blogs/research/2018/11/forecasts-iot/)
* [Castor: Contextual IoT Time Series Data and Model Management at Scale](https://arxiv.org/abs/1811.08566) Bei Chen, Bradley Eck, Francesco Fusco, Robert Gormally, Mark Purcell, Mathieu Sinn, Seshu Tirupathi. 2018 IEEE International Conference on Data Mining (ICDM workshops).


This project has received funding from the European Union’s Horizon 2020 research and innovation programme under grant agreement No 824988. https://musketeer.eu/

.. image:: /EU.png
