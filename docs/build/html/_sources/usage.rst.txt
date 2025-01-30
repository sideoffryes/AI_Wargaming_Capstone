Usage
=====

Installation
------------

To use this project, the are several prerequisites that are necessary. The easiest way to manage these dependencies is using Conda.

If you do not have Conda already, `download and install a release <https://docs.anaconda.com/miniconda/install/>`_ for your OS.

All of the required python packages can be easily installed via the provided configuration files. There are separate files for GPU and CPU dependencies.

CPU
^^^
.. code-block:: console

    (base) $ conda env create -f environment_cpu.yml

GPU
^^^
.. code-block:: console

    (base) $ conda env create -f environment_gpu.yml
