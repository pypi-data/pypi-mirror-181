PyGyverLamp2
--------

This is a simple multifunctional library to control GyverLamp2 by AlexGyver.
https://github.com/AlexGyver/GyverLamp2

parsing.ino https://drive.google.com/file/d/14PXY9VrPZEMcn3YUO5z4RqbVFl8M89Sb/view?usp=sharing

Installing
----------

**Python 3.9 or higher is required**

To install the library without full voice support, you can just run the following command:

.. code:: sh

    # Linux/macOS
    python3 -m pip install -U PyGyverLamp2

    # Windows
    py -3 -m pip install -U PyGyverLamp2


Optional Package
~~~~~~~~~~~~~~~~~~

* `Flask <https://pypi.org/project/flask/>`__ (To create a local server)

Quick Example
~~~~~~~~~~~~~

.. code:: python

    from PyGyverLamp2 import Lamp
    from time import sleep

    lamp = Lamp(key='GL', ip='192.168.1.237', port=61197, group_id=1)

    lamp.turn_on()
    slee(0.5)
    lamp.next_mode()


You can find more examples in the `examples directory <https://github.com/KirillMonster/PyGyverLamp2/tree/main/examples/>`_.
