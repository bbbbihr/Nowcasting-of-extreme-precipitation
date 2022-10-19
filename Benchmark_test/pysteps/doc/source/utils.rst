.. _pysteps.utils:

Miscellaneous utility functions (:mod:`pysteps.utils`)
******************************************************

Utility functions for converting data values to/from different units, 
manipulating the dimensions of precipitation fields and computing the FFT.

pysteps\.utils\.conversion
--------------------------

.. currentmodule:: pysteps.utils.conversion

.. autosummary::
    to_rainrate
    to_raindepth
    to_reflectivity

.. automodule:: pysteps.utils.conversion
    :members:

pysteps\.utils\.dimension
-------------------------

.. currentmodule:: pysteps.utils.dimension

.. autosummary::
    aggregate_fields_time
    aggregate_fields_space
    aggregate_fields
    clip_domain
    square_domain

.. automodule:: pysteps.utils.dimension
    :members:

pysteps\.utils\.fft
-------------------

.. currentmodule:: pysteps.utils.fft

.. autosummary::
    get_method

.. automodule:: pysteps.utils.fft
    :members:

pysteps\.utils\.interface
-------------------------

.. automodule:: pysteps.utils.interface
    :members:

pysteps\.utils\.transformation
------------------------------

.. currentmodule:: pysteps.utils.transformation

.. autosummary::
    dB_transform
    boxcox_transform
    boxcox_transform_test_lambdas
    NQ_transform
    sqrt_transform

.. automodule:: pysteps.utils.transformation
    :members:
