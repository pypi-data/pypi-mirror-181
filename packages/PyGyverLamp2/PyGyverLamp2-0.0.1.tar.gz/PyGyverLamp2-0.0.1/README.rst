PyGyverLamp2
--------

This is a simple multifunctional library to control GyverLamp2 by AlexGyver


Installing
----------

**Python 3.9 or higher is required**

To install the library without full voice support, you can just run the following command:

.. code:: sh

    # Linux/macOS
    python3 -m pip install -U pygyverlamp2

    # Windows
    py -3 -m pip install -U pygyverlamp2


Optional Package
~~~~~~~~~~~~~~~~~~

* `Flask <https://pypi.org/project/flask/>`__ (To create a local server)

Quick Example
~~~~~~~~~~~~~

.. code:: python

    from pygyverlamp2 import Lamp

    lamp = Lamp(key='GL', ip='192.168.1.237', port=61197, group_id=1)

    lamp.turn_on()

    lamp.next_mode()


You can find more examples in the `examples directory <https://github.com/KirillMonster/1/blob/stable/examples/>`_.
