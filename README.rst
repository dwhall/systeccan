systeccan
=========

The ``systeccan`` module is a Python wrapper based on the (c) SYSTEC electronic GmbH
USBcanServer wrapper class.

Requires the driver package USB-CANmodul Utility Disk with the USBCAN32.DLL library to
be installed from https://www.systec-electronic.com/en/products/interfaces-gateways/sysworxx-usb-canmodul1

The module exposes base class ``USBCanServer`` which can be subclassed to handle connection
events, message reception events and etc.

Example
-------
.. code:: python

    from systeccan import *

    # create the USB CAN server
    can = USBCanServer()

    # initialize the hardware
    can.init_hardware()

    # initialize channel 0 with bitrate 125000
    can.init_can(channel=Channel.CHANNEL_CH0, BTR=Baudrate.BAUD_125kBit)

    # create standard CAN message
    msg = CanMsg(id=0x12, frame_format=MsgFrameFormat.MSG_FF_STD, data=[0x00, 0x01])

    # write the message
    can.write_can_msg(Channel.CHANNEL_CH0, [msg])

    # shutdown the channels and hardware
    can.shutdown()
