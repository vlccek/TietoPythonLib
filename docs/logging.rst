Logging
*********

if you don´t want to log to default logging file (`fabric.log`) you can use custom logging logger

.. code::

    from loguru import logger

    logger.add(sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO")


.. note::
    more information in loguru documenatation.
    https://loguru.readthedocs.io/en/stable

.. warning:: 
    this don´t remove old logger. They will work both. 
    for remove use:

    .. code::

        logger.remove()

