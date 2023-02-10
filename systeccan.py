#!/usr/bin/env python

from ctypes import Structure, WINFUNCTYPE, POINTER, WinDLL, byref, sizeof, c_ubyte
from ctypes.wintypes import WORD, DWORD, BOOL, LPVOID, PWCHAR, PDWORD
import logging
import os
import sys

__author__ = "Daniel Igaz"
__copyright__ = "Copyright 2018"

__license__ = "GPL-3.0"
__version__ = "0.0.0"
__email__ = "daniel.igaz.86@gmail.com"
__status__ = "Development"

__all__ = ['Baudrate', 'BaudrateEx', 'MsgFrameFormat', 'CanStatus', 'UsbStatus', 'OutputControl', 'Channel',
           'ResetFlags', 'ProductCode', 'CyclicFlags', 'PendingFlags', 'CanMsg', 'Status', 'Mode', 'HardwareInfoEx',
           'HardwareInitInfo', 'ChannelInfo', 'MsgCountInfo', 'VersionType', 'USBCanException', 'USBCanError',
           'USBCanCmdError', 'USBCanWarning', 'USBCanServer', 'MAX_MODULES', 'MAX_INSTANCES',
           'ANY_MODULE', 'AMR_ALL', 'ACR_ALL', 'MAX_CYCLIC_CAN_MSG']

BYTE = c_ubyte
PBYTE = POINTER(BYTE)


logger = logging.getLogger(__name__)


#: Maximum number of modules that are supported.
MAX_MODULES = 64

#: Maximum number of applications that can use the USB-CAN-library.
MAX_INSTANCES = 64

#: With the method :meth:`USBCanServer.init_can` the module is used, which is detected at first.
#: This value only should be used in case only one module is connected to the computer.
ANY_MODULE = 255

#: No valid USB-CAN Handle (only used internally).
INVALID_HANDLE = 0xFF


class Baudrate(WORD):
    """
    Specifies pre-defined baud rate values for GW-001, GW-002 and all systec USB-CANmoduls.

    .. seealso::

       :meth:`USBCanServer.init_can`

       :meth:`USBCanServer.set_baudrate`

       :meth:`USBCanServer.get_baudrate_message`

       :class:`BaudrateEx`
    """

    #: 1000 kBit/sec
    BAUD_1MBit = 0x14
    #: 800 kBit/sec
    BAUD_800kBit = 0x16
    #: 500 kBit/sec
    BAUD_500kBit = 0x1C
    #: 250 kBit/sec
    BAUD_250kBit = 0x11C
    #: 125 kBit/sec
    BAUD_125kBit = 0x31C
    #: 100 kBit/sec
    BAUD_100kBit = 0x432F
    #: 50 kBit/sec
    BAUD_50kBit = 0x472F
    #: 20 kBit/sec
    BAUD_20kBit = 0x532F
    #: 10 kBit/sec
    BAUD_10kBit = 0x672F
    #: Uses pre-defined extended values of baudrate for all systec USB-CANmoduls.
    BAUD_USE_BTREX = 0x0
    #: Automatic baud rate detection (not implemented in this version).
    BAUD_AUTO = -1


class BaudrateEx(DWORD):
    """
    Specifies pre-defined baud rate values for all systec USB-CANmoduls.

    These values cannot be used for GW-001 and GW-002! Use values from enum :class:`Baudrate` instead.

    .. seealso::

       :meth:`USBCanServer.init_can`

       :meth:`USBCanServer.set_baudrate`

       :meth:`USBCanServer.get_baudrate_ex_message`

       :class:`Baudrate`
    """

    #: G3: 1000 kBit/sec
    BAUDEX_1MBit = 0x20354
    #: G3: 800 kBit/sec
    BAUDEX_800kBit = 0x30254
    #: G3: 500 kBit/sec
    BAUDEX_500kBit = 0x50354
    #: G3: 250 kBit/sec
    BAUDEX_250kBit = 0xB0354
    #: G3: 125 kBit/sec
    BAUDEX_125kBit = 0x170354
    #: G3: 100 kBit/sec
    BAUDEX_100kBit = 0x170466
    #: G3: 50 kBit/sec
    BAUDEX_50kBit = 0x2F0466
    #: G3: 20 kBit/sec
    BAUDEX_20kBit = 0x770466
    #: G3: 10 kBit/sec (half CPU clock)
    BAUDEX_10kBit = 0x80770466
    #: G3: 1000 kBit/sec Sample Point: 87,50%
    BAUDEX_SP2_1MBit = 0x20741
    #: G3: 800 kBit/sec Sample Point: 86,67%
    BAUDEX_SP2_800kBit = 0x30731
    #: G3: 500 kBit/sec Sample Point: 87,50%
    BAUDEX_SP2_500kBit = 0x50741
    #: G3: 250 kBit/sec Sample Point: 87,50%
    BAUDEX_SP2_250kBit = 0xB0741
    #: G3: 125 kBit/sec Sample Point: 87,50%
    BAUDEX_SP2_125kBit = 0x170741
    #: G3: 100 kBit/sec Sample Point: 87,50%
    BAUDEX_SP2_100kBit = 0x1D1741
    #: G3: 50 kBit/sec Sample Point: 87,50%
    BAUDEX_SP2_50kBit = 0x3B1741
    #: G3: 20 kBit/sec Sample Point: 85,00%
    BAUDEX_SP2_20kBit = 0x771772
    #: G3: 10 kBit/sec Sample Point: 85,00% (half CPU clock)
    BAUDEX_SP2_10kBit = 0x80771772

    #: G4: 1000 kBit/sec Sample Point: 83,33%
    BAUDEX_G4_1MBit = 0x406F0000
    #: G4: 800 kBit/sec Sample Point: 80,00%
    BAUDEX_G4_800kBit = 0x402A0001
    #: G4: 500 kBit/sec Sample Point: 83,33%
    BAUDEX_G4_500kBit = 0x406F0001
    #: G4: 250 kBit/sec Sample Point: 83,33%
    BAUDEX_G4_250kBit = 0x406F0003
    #: G4: 125 kBit/sec Sample Point: 83,33%
    BAUDEX_G4_125kBit = 0x406F0007
    #: G4: 100 kBit/sec Sample Point: 83,33%
    BAUDEX_G4_100kBit = 0x416F0009
    #: G4: 50 kBit/sec Sample Point: 83,33%
    BAUDEX_G4_50kBit = 0x416F0013
    #: G4: 20 kBit/sec Sample Point: 84,00%
    BAUDEX_G4_20kBit = 0x417F002F
    #: G4: 10 kBit/sec Sample Point: 84,00% (half CPU clock)
    BAUDEX_G4_10kBit = 0x417F005F
    #: Uses pre-defined values of baud rates of :class:`Baudrate`.
    BAUDEX_USE_BTR01 = 0x0
    #: Automatic baud rate detection (not implemented in this version).
    BAUDEX_AUTO = 0xFFFFFFFF


class MsgFrameFormat(BYTE):
    """
    Specifies values for the frame format of CAN messages for member :attr:`CanMsg.m_bFF` in structure
    :class:`CanMsg`. These values can be combined.

    .. seealso:: :class:`CanMsg`
    """

    #: standard CAN data frame with 11 bit ID (CAN2.0A spec.)
    MSG_FF_STD = 0x0
    #: transmit echo
    MSG_FF_ECHO = 0x20
    #: CAN remote request frame with
    MSG_FF_RTR = 0x40
    #: extended CAN data frame with 29 bit ID (CAN2.0B spec.)
    MSG_FF_EXT = 0x80


class ReturnCode(BYTE):
    """
    Specifies all return codes of all methods of this class.
    """

    #: no error
    SUCCESSFUL = 0x0
    # start of error codes coming from USB-CAN-library
    ERR = 0x1
    # start of error codes coming from command interface between host and USB-CANmodul
    ERRCMD = 0x40
    # start of warning codes
    WARNING = 0x80
    # start of reserved codes which are only used internally
    RESERVED = 0xC0

    #: could not created a resource (memory, handle, ...)
    ERR_RESOURCE = 0x1
    #: the maximum number of opened modules is reached
    ERR_MAXMODULES = 0x2
    #: the specified module is already in use
    ERR_HWINUSE = 0x3
    #: the software versions of the module and library are incompatible
    ERR_ILLVERSION = 0x4
    #: the module with the specified device number is not connected (or used by an other application)
    ERR_ILLHW = 0x5
    #: wrong USB-CAN-Handle handed over to the function
    ERR_ILLHANDLE = 0x6
    #: wrong parameter handed over to the function
    ERR_ILLPARAM = 0x7
    #: instruction can not be processed at this time
    ERR_BUSY = 0x8
    #: no answer from module
    ERR_TIMEOUT = 0x9
    #: a request to the driver failed
    ERR_IOFAILED = 0xA
    #: a CAN message did not fit into the transmit buffer
    ERR_DLL_TXFULL = 0xB
    #: maximum number of applications is reached
    ERR_MAXINSTANCES = 0xC
    #: CAN interface is not yet initialized
    ERR_CANNOTINIT = 0xD
    #: USB-CANmodul was disconnected
    ERR_DISCONECT = 0xE
    #: the needed device class does not exist
    ERR_NOHWCLASS = 0xF
    #: illegal CAN channel
    ERR_ILLCHANNEL = 0x10
    #: reserved
    ERR_RESERVED1 = 0x11
    #: the API function can not be used with this hardware
    ERR_ILLHWTYPE = 0x12

    #: the received response does not match to the transmitted command
    ERRCMD_NOTEQU = 0x40
    #: no access to the CAN controller
    ERRCMD_REGTST = 0x41
    #: the module could not interpret the command
    ERRCMD_ILLCMD = 0x42
    #: error while reading the EEPROM
    ERRCMD_EEPROM = 0x43
    #: reserved
    ERRCMD_RESERVED1 = 0x44
    #: reserved
    ERRCMD_RESERVED2 = 0x45
    #: reserved
    ERRCMD_RESERVED3 = 0x46
    #: illegal baud rate value specified in BTR0/BTR1 for systec USB-CANmoduls
    ERRCMD_ILLBDR = 0x47
    #: CAN channel is not initialized
    ERRCMD_NOTINIT = 0x48
    #: CAN channel is already initialized
    ERRCMD_ALREADYINIT = 0x49
    #: illegal sub-command specified
    ERRCMD_ILLSUBCMD = 0x4A
    #: illegal index specified (e.g. index for cyclic CAN messages)
    ERRCMD_ILLIDX = 0x4B
    #: cyclic CAN message(s) can not be defined because transmission of cyclic CAN messages is already running
    ERRCMD_RUNNING = 0x4C

    #: no CAN messages received
    WARN_NODATA = 0x80
    #: overrun in receive buffer of the kernel driver
    WARN_SYS_RXOVERRUN = 0x81
    #: overrun in receive buffer of the USB-CAN-library
    WARN_DLL_RXOVERRUN = 0x82
    #: reserved
    WARN_RESERVED1 = 0x83
    #: reserved
    WARN_RESERVED2 = 0x84
    #: overrun in transmit buffer of the firmware (but this CAN message was successfully stored in buffer of the
    #: library)
    WARN_FW_TXOVERRUN = 0x85
    #: overrun in receive buffer of the firmware (but this CAN message was successfully read)
    WARN_FW_RXOVERRUN = 0x86
    #: reserved
    WARN_FW_TXMSGLOST = 0x87
    #: pointer is NULL
    WARN_NULL_PTR = 0x90
    #: not all CAN messages could be stored to the transmit buffer in USB-CAN-library (check output of parameter
    #: pdwCount_p)
    WARN_TXLIMIT = 0x91
    #: reserved
    WARN_BUSY = 0x92


class CbEvent(BYTE):
    """
    This enum defines events for the callback functions of the library.

    .. seealso:: :meth:`USBCanServer.get_status`
    """

    #: The USB-CANmodul has been initialized.
    EVENT_INITHW = 0
    #: The CAN interface has been initialized.
    EVENT_init_can = 1
    #: A new CAN message has been received.
    EVENT_RECEIVE = 2
    #: The error state in the module has changed.
    EVENT_STATUS = 3
    #: The CAN interface has been deinitialized.
    EVENT_DEINIT_CAN = 4
    #: The USB-CANmodul has been deinitialized.
    EVENT_DEINITHW = 5
    #: A new USB-CANmodul has been connected.
    EVENT_CONNECT = 6
    #: Any USB-CANmodul has been disconnected.
    EVENT_DISCONNECT = 7
    #: A USB-CANmodul has been disconnected during operation.
    EVENT_FATALDISCON = 8
    #: Reserved
    EVENT_RESERVED1 = 0x80


class CanStatus(WORD):
    """
    CAN error status bits. These bit values occurs in combination with the method :meth:`USBCanServer.get_status`.

    .. seealso::

       :meth:`USBCanServer.get_status`

       :meth:`USBCanServer.get_can_status_message`
    """

    #: No error.
    CANERR_OK = 0x0
    #: Transmit buffer of the CAN controller is full.
    CANERR_XMTFULL = 0x1
    #: Receive buffer of the CAN controller is full.
    CANERR_OVERRUN = 0x2
    #: Bus error: Error Limit 1 exceeded (Warning Limit reached)
    CANERR_BUSLIGHT = 0x4
    #: Bus error: Error Limit 2 exceeded (Error Passive)
    CANERR_BUSHEAVY = 0x8
    #: Bus error: CAN controller has gone into Bus-Off state.
    #: Method :meth:`USBCanServer.reset_can` has to be called.
    CANERR_BUSOFF = 0x10
    #: No CAN message is within the receive buffer.
    CANERR_QRCVEMPTY = 0x20
    #: Receive buffer is full. CAN messages has been lost.
    CANERR_QOVERRUN = 0x40
    #: Transmit buffer is full.
    CANERR_QXMTFULL = 0x80
    #: Register test of the CAN controller failed.
    CANERR_REGTEST = 0x100
    #: Memory test on hardware failed.
    CANERR_MEMTEST = 0x200
    #: Transmit CAN message(s) was/were automatically deleted by firmware (transmit timeout).
    CANERR_TXMSGLOST = 0x400


class UsbStatus(WORD):
    """
    USB error status bits. These bit values occurs in combination with the method :meth:`USBCanServer.get_status`.

    .. seealso:: :meth:`USBCanServer.get_status`
    """

    #: No error.
    USBERR_OK = 0x0


#: Specifies the acceptance mask for receiving all CAN messages.
#:
#: .. seealso::
#:
#:    :const:`ACR_ALL`
#:
#:    :meth:`USBCanServer.init_can`
#:
#:    :meth:`USBCanServer.set_acceptance`
AMR_ALL = 0xFFFFFFFF

#: Specifies the acceptance code for receiving all CAN messages.
#:
#: .. seealso::
#:
#:    :const:`AMR_ALL`
#:
#:    :meth:`USBCanServer.init_can`
#:
#:    :meth:`USBCanServer.set_acceptance`
ACR_ALL = 0x0


class OutputControl(BYTE):
    """
    Specifies pre-defined values for the Output Control Register of SJA1000 on GW-001 and GW-002.
    These values are only important for GW-001 and GW-002.
    They does not have an effect on systec USB-CANmoduls.
    """
    #: default OCR value for the standard USB-CANmodul GW-001/GW-002
    OCR_DEFAULT = 0x1A
    #: OCR value for RS485 interface and galvanic isolation
    OCR_RS485_ISOLATED = 0x1E
    #: OCR value for RS485 interface but without galvanic isolation
    OCR_RS485_NOT_ISOLATED = 0xA


#: Specifies the default value for the maximum number of entries in the receive and transmit buffer.
DEFAULT_BUFFER_ENTRIES = 4096


class Channel(BYTE):
    """
    Specifies values for the CAN channel to be used on multi-channel USB-CANmoduls.
    """

    #: Specifies the first CAN channel (GW-001/GW-002 and USB-CANmodul1 only can be used with this channel).
    CHANNEL_CH0 = 0
    #: Specifies the second CAN channel (this channel cannot be used with GW-001/GW-002 and USB-CANmodul1).
    CHANNEL_CH1 = 1
    #: Specifies all CAN channels (can only be used with the method :meth:`USBCanServer.shutdown`).
    CHANNEL_ALL = 254
    #: Specifies the use of any channel (can only be used with the method :meth:`USBCanServer.read_can_msg`).
    CHANNEL_ANY = 255
    #: Specifies the first CAN channel (equivalent to :data:`CHANNEL_CH0`).
    CHANNEL_CAN1 = CHANNEL_CH0
    #: Specifies the second CAN channel (equivalent to :data:`CHANNEL_CH1`).
    CHANNEL_CAN2 = CHANNEL_CH1
    #: Specifies the LIN channel (currently not supported by the software).
    CHANNEL_LIN = CHANNEL_CH1


class ResetFlags(DWORD):
    """
    Specifies flags for resetting USB-CANmodul with method :meth:`USBCanServer.reset_can`.
    These flags can be used in combination.

    .. seealso:: :meth:`USBCanServer.reset_can`
    """

    #: reset everything
    RESET_ALL = 0x0
    #: no CAN status reset (only supported for systec USB-CANmoduls)
    RESET_NO_STATUS = 0x1
    #: no CAN controller reset
    RESET_NO_CANCTRL = 0x2
    #: no transmit message counter reset
    RESET_NO_TXCOUNTER = 0x4
    #: no receive message counter reset
    RESET_NO_RXCOUNTER = 0x8
    #: no transmit message buffer reset at channel level
    RESET_NO_TXBUFFER_CH = 0x10
    #: no transmit message buffer reset at USB-CAN-library level
    RESET_NO_TXBUFFER_DLL = 0x20
    #: no transmit message buffer reset at firmware level
    RESET_NO_TXBUFFER_FW = 0x80
    #: no receive message buffer reset at channel level
    RESET_NO_RXBUFFER_CH = 0x100
    #: no receive message buffer reset at USB-CAN-library level
    RESET_NO_RXBUFFER_DLL = 0x200
    #: no receive message buffer reset at kernel driver level
    RESET_NO_RXBUFFER_SYS = 0x400
    #: no receive message buffer reset at firmware level
    RESET_NO_RXBUFFER_FW = 0x800
    #: complete firmware reset (module will automatically reconnect at USB port in 500msec)
    RESET_FIRMWARE = 0xFFFFFFFF

    #: no reset of all message counters
    RESET_NO_COUNTER_ALL = (RESET_NO_TXCOUNTER | RESET_NO_RXCOUNTER)
    #: no reset of transmit message buffers at communication level (firmware, kernel and library)
    RESET_NO_TXBUFFER_COMM = (RESET_NO_TXBUFFER_DLL | 0x40 | RESET_NO_TXBUFFER_FW)
    #: no reset of receive message buffers at communication level (firmware, kernel and library)
    RESET_NO_RXBUFFER_COMM = (RESET_NO_RXBUFFER_DLL | RESET_NO_RXBUFFER_SYS | RESET_NO_RXBUFFER_FW)
    #: no reset of all transmit message buffers
    RESET_NO_TXBUFFER_ALL = (RESET_NO_TXBUFFER_CH | RESET_NO_TXBUFFER_COMM)
    #: no reset of all receive message buffers
    RESET_NO_RXBUFFER_ALL = (RESET_NO_RXBUFFER_CH | RESET_NO_RXBUFFER_COMM)
    #: no reset of all message buffers at communication level (firmware, kernel and library)
    RESET_NO_BUFFER_COMM = (RESET_NO_TXBUFFER_COMM | RESET_NO_RXBUFFER_COMM)
    #: no reset of all message buffers
    RESET_NO_BUFFER_ALL = (RESET_NO_TXBUFFER_ALL | RESET_NO_RXBUFFER_ALL)
    #: reset of the CAN status only
    RESET_ONLY_STATUS = (0xFFFF & ~RESET_NO_STATUS)
    #: reset of the CAN controller only
    RESET_ONLY_CANCTRL = (0xFFFF & ~RESET_NO_CANCTRL)
    #: reset of the transmit buffer in firmware only
    RESET_ONLY_TXBUFFER_FW = (0xFFFF & ~RESET_NO_TXBUFFER_FW)
    #: reset of the receive buffer in firmware only
    RESET_ONLY_RXBUFFER_FW = (0xFFFF & ~RESET_NO_RXBUFFER_FW)
    #: reset of the specified channel of the receive buffer only
    RESET_ONLY_RXCHANNEL_BUFF = (0xFFFF & ~RESET_NO_RXBUFFER_CH)
    #: reset of the specified channel of the transmit buffer only
    RESET_ONLY_TXCHANNEL_BUFF = (0xFFFF & ~RESET_NO_TXBUFFER_CH)
    #: reset of the receive buffer and receive message counter only
    RESET_ONLY_RX_BUFF = (0xFFFF & ~(RESET_NO_RXBUFFER_ALL | RESET_NO_RXCOUNTER))
    #: reset of the receive buffer and receive message counter (for GW-002) only
    RESET_ONLY_RX_BUFF_GW002 = (0xFFFF & ~(RESET_NO_RXBUFFER_ALL | RESET_NO_RXCOUNTER |
                                                  RESET_NO_TXBUFFER_FW))
    #: reset of the transmit buffer and transmit message counter only
    RESET_ONLY_TX_BUFF = (0xFFFF & ~(RESET_NO_TXBUFFER_ALL | RESET_NO_TXCOUNTER))
    #: reset of all buffers and all message counters only
    RESET_ONLY_ALL_BUFF = (RESET_ONLY_RX_BUFF & RESET_ONLY_TX_BUFF)
    #: reset of all message counters only
    RESET_ONLY_ALL_COUNTER = (0xFFFF & ~RESET_NO_COUNTER_ALL)


PRODCODE_PID_TWO_CHA = 0x1
PRODCODE_PID_TERM = 0x1
PRODCODE_PID_RBUSER = 0x1
PRODCODE_PID_RBCAN = 0x1
PRODCODE_PID_G4 = 0x20
PRODCODE_PID_RESVD = 0x40

PRODCODE_MASK_DID = 0xFFFF0000
PRODCODE_MASK_PID = 0xFFFF
PRODCODE_MASK_PIDG3 = (PRODCODE_MASK_PID & 0xFFFFFFBF)


class ProductCode(WORD):
    """
    These values defines product codes for all known USB-CANmodul derivatives received in member
    :attr:`HardwareInfoEx.m_dwProductCode` of structure :class:`HardwareInfoEx`
    with method :meth:`USBCanServer.get_hardware_info`.

    .. seealso::

       :meth:`USBCanServer.get_hardware_info`

       :class:`HardwareInfoEx`
    """

    #: Product code for GW-001 (outdated).
    PRODCODE_PID_GW001 = 0x1100
    #: Product code for GW-002 (outdated).
    PRODCODE_PID_GW002 = 0x1102
    #: Product code for Multiport CAN-to-USB G3.
    PRODCODE_PID_MULTIPORT = 0x1103
    #: Product code for USB-CANmodul1 G3.
    PRODCODE_PID_BASIC = 0x1104
    #: Product code for USB-CANmodul2 G3.
    PRODCODE_PID_ADVANCED = 0x1105
    #: Product code for USB-CANmodul8 G3.
    PRODCODE_PID_USBCAN8 = 0x1107
    #: Product code for USB-CANmodul16 G3.
    PRODCODE_PID_USBCAN16 = 0x1109
    #: Reserved.
    PRODCODE_PID_RESERVED3 = 0x1110
    #: Product code for USB-CANmodul2 G4.
    PRODCODE_PID_ADVANCED_G4 = 0x1121
    #: Product code for USB-CANmodul1 G4.
    PRODCODE_PID_BASIC_G4 = 0x1122
    #: Reserved.
    PRODCODE_PID_RESERVED1 = 0x1144
    #: Reserved.
    PRODCODE_PID_RESERVED2 = 0x1145


#: Definitions for cyclic CAN messages.
MAX_CYCLIC_CAN_MSG = 16


class CyclicFlags(DWORD):
    """
    Specifies flags for cyclical CAN messages.
    These flags can be used in combinations with method :meth:`USBCanServer.enable_cyclic_can_msg`.

    .. seealso:: :meth:`USBCanServer.enable_cyclic_can_msg`
    """

    #: Stops the transmission of cyclic CAN messages.
    CYCLIC_FLAG_STOPP = 0x0
    #: Global enable of transmission of cyclic CAN messages.
    CYCLIC_FLAG_START = 0x80000000
    #: List of cyclcic CAN messages will be processed in sequential mode (otherwise in parallel mode).
    CYCLIC_FLAG_SEQUMODE = 0x40000000
    #: No echo will be sent back if echo mode is enabled with method :meth:`USBCanServer.init_can`.
    CYCLIC_FLAG_NOECHO = 0x10000
    #: CAN message with index 0 of the list will not be sent.
    CYCLIC_FLAG_LOCK_0 = 0x1
    #: CAN message with index 1 of the list will not be sent.
    CYCLIC_FLAG_LOCK_1 = 0x2
    #: CAN message with index 2 of the list will not be sent.
    CYCLIC_FLAG_LOCK_2 = 0x4
    #: CAN message with index 3 of the list will not be sent.
    CYCLIC_FLAG_LOCK_3 = 0x8
    #: CAN message with index 4 of the list will not be sent.
    CYCLIC_FLAG_LOCK_4 = 0x10
    #: CAN message with index 5 of the list will not be sent.
    CYCLIC_FLAG_LOCK_5 = 0x20
    #: CAN message with index 6 of the list will not be sent.
    CYCLIC_FLAG_LOCK_6 = 0x40
    #: CAN message with index 7 of the list will not be sent.
    CYCLIC_FLAG_LOCK_7 = 0x80
    #: CAN message with index 8 of the list will not be sent.
    CYCLIC_FLAG_LOCK_8 = 0x100
    #: CAN message with index 9 of the list will not be sent.
    CYCLIC_FLAG_LOCK_9 = 0x200
    #: CAN message with index 10 of the list will not be sent.
    CYCLIC_FLAG_LOCK_10 = 0x400
    #: CAN message with index 11 of the list will not be sent.
    CYCLIC_FLAG_LOCK_11 = 0x800
    #: CAN message with index 12 of the list will not be sent.
    CYCLIC_FLAG_LOCK_12 = 0x1000
    #: CAN message with index 13 of the list will not be sent.
    CYCLIC_FLAG_LOCK_13 = 0x2000
    #: CAN message with index 14 of the list will not be sent.
    CYCLIC_FLAG_LOCK_14 = 0x4000
    #: CAN message with index 15 of the list will not be sent.
    CYCLIC_FLAG_LOCK_15 = 0x8000


class PendingFlags(BYTE):
    """
    Specifies flags for method :meth:`USBCanServer.get_msg_pending`.
    These flags can be uses in combinations.

    .. seealso:: :meth:`USBCanServer.get_msg_pending`
    """

    #: number of pending CAN messages in receive buffer of USB-CAN-library
    PENDING_FLAG_RX_DLL = 0x1
    #: reserved
    PENDING_FLAG_RX_SYS = 0x2
    #: number of pending CAN messages in receive buffer of firmware
    PENDING_FLAG_RX_FW = 0x4
    #: number of pending CAN messages in transmit buffer of USB-CAN-library
    PENDING_FLAG_TX_DLL = 0x10
    #: reserved
    PENDING_FLAG_TX_SYS = 0x20
    #: number of pending CAN messages in transmit buffer of firmware
    PENDING_FLAG_TX_FW = 0x40
    #: number of pending CAN messages in all receive buffers
    PENDING_FLAG_RX_ALL = (PENDING_FLAG_RX_DLL | PENDING_FLAG_RX_SYS |
                                  PENDING_FLAG_RX_FW)
    #: number of pending CAN messages in all transmit buffers
    PENDING_FLAG_TX_ALL = (PENDING_FLAG_TX_DLL | PENDING_FLAG_TX_SYS |
                                  PENDING_FLAG_TX_FW)
    #: number of pending CAN messages in all buffers
    PENDING_FLAG_ALL = (PENDING_FLAG_RX_ALL | PENDING_FLAG_TX_ALL)


class CanMsg(Structure):
    """
    Structure of a CAN message.

    .. seealso::

       :meth:`USBCanServer.read_can_msg`

       :meth:`USBCanServer.write_can_msg`

       :meth:`USBCanServer.define_cyclic_can_msg`

       :meth:`USBCanServer.read_cyclic_can_msg`
    """
    _pack_ = 1
    _fields_ = [
        ("m_dwID", DWORD),  # CAN Identifier
        ("m_bFF", BYTE),  # CAN Frame Format (see enum :class:`MsgFrameFormat`)
        ("m_bDLC", BYTE),  # CAN Data Length Code
        ("m_bData", BYTE * 8),  # CAN Data (array of 8 bytes)
        ("m_dwTime", DWORD,)  # Receive time stamp in ms (for transmit messages no meaning)
    ]

    def __init__(self, id=0, frame_format=MsgFrameFormat.MSG_FF_STD, data=[]):
        super(CanMsg, self).__init__(id, frame_format, len(data), (BYTE * 8)(*data), 0)

    @property
    def id(self): return self.m_dwID

    @id.setter
    def id(self, id): self.m_dwID = id

    @property
    def frame_format(self): return self.m_bFF

    @frame_format.setter
    def frame_format(self, frame_format): self.m_bFF = frame_format

    @property
    def data(self): return self.m_bData[:self.m_bDLC]

    @data.setter
    def data(self, data):
        self.m_bDLC = len(data)
        self.m_bData((BYTE * 8)(*data))

    @property
    def time(self): return self.m_dwTime


class Status(Structure):
    """
    Structure with the error status of CAN and USB.
    Use this structure with the method :meth:`USBCanServer.get_status`

    .. seealso::

       :meth:`USBCanServer.get_status`

       :meth:`USBCanServer.get_can_status_message`
    """
    _pack_ = 1
    _fields_ = [
        ("m_wCanStatus", WORD),  # CAN error status (see enum :class:`CanStatus`)
        ("m_wUsbStatus", WORD),  # USB error status (see enum :class:`UsbStatus`)
    ]

    @property
    def can_status(self): return self.m_wCanStatus

    @property
    def usb_status(self): return self.m_wUsbStatus


class Mode(BYTE):
    """
    Specifies values for operation mode of a CAN channel.
    These values can be combined by OR operation with the method :meth:`USBCanServer.init_can`.
    """

    #: normal operation mode (transmitting and receiving)
    MODE_NORMAL = 0
    #: listen only mode (receiving only, no ACK at CAN bus)
    MODE_LISTEN_ONLY = 1
    #: CAN messages which was sent will be received back with method :meth:`USBCanServer.read_can_msg`
    MODE_TX_ECHO = 2
    #: reserved (not implemented in this version)
    MODE_RX_ORDER_CH = 4
    #: high resolution time stamps in received CAN messages (only available with STM derivatives)
    MODE_HIGH_RES_TIMER = 8


class InitCanParam(Structure):
    """
    Structure including initialisation parameters used internally in :meth:`USBCanServer.init_can`.

    .. note:: This structure is only used internally.
    """
    _pack_ = 1
    _fields_ = [
        ("m_dwSize", DWORD),  # size of this structure (only used internally)
        ("m_bMode", Mode),  # selects the mode of CAN controller (see enum :class:`Mode`)
        # Baudrate Registers for GW-001 or GW-002
        ("m_bBTR0", BYTE),  # Bus Timing Register 0 (see enum :class:`Baudrate`)
        ("m_bBTR1", BYTE),  # Bus Timing Register 1 (see enum :class:`Baudrate`)
        ("m_bOCR", BYTE),  # Output Control Register (see enum :class:`OutputControl`)
        ("m_dwAMR", DWORD),  # Acceptance Mask Register (see method :meth:`USBCanServer.set_acceptance`)
        ("m_dwACR", DWORD),  # Acceptance Code Register (see method :meth:`USBCanServer.set_acceptance`)
        ("m_dwBaudrate", DWORD),  # Baudrate Register for all systec USB-CANmoduls
                                  # (see enum :class:`BaudrateEx`)
        ("m_wNrOfRxBufferEntries", WORD),  # number of receive buffer entries (default is 4096)
        ("m_wNrOfTxBufferEntries", WORD),  # number of transmit buffer entries (default is 4096)
    ]

    def __init__(self, mode, BTR, OCR, AMR, ACR, baudrate, rx_buffer_entries, tx_buffer_entries):
        super(InitCanParam, self).__init__(sizeof(InitCanParam), mode, BTR >> 8, BTR, OCR, AMR, ACR,
                                           baudrate, rx_buffer_entries, tx_buffer_entries)

    @property
    def mode(self): return self.m_bMode

    @mode.setter
    def mode(self, mode): self.m_bMode = mode

    @property
    def BTR(self): return self.m_bBTR0 << 8 | self.m_bBTR1

    @BTR.setter
    def BTR(self, BTR): self.m_bBTR0, self.m_bBTR1 = BTR >> 8, BTR

    @property
    def OCR(self): return self.m_bOCR

    @OCR.setter
    def OCR(self, OCR): self.m_bOCR = OCR

    @property
    def baudrate(self): return self.m_dwBaudrate

    @baudrate.setter
    def baudrate(self, baudrate): self.m_dwBaudrate = baudrate

    @property
    def rx_buffer_entries(self): return self.m_wNrOfRxBufferEntries

    @rx_buffer_entries.setter
    def rx_buffer_entries(self, rx_buffer_entries): self.m_wNrOfRxBufferEntries = rx_buffer_entries

    @property
    def tx_buffer_entries(self): return self.m_wNrOfTxBufferEntries

    @rx_buffer_entries.setter
    def tx_buffer_entries(self, tx_buffer_entries): self.m_wNrOfTxBufferEntries = tx_buffer_entries


class Handle(BYTE):
    pass


class HardwareInfoEx(Structure):
    """
    Structure including hardware information about the USB-CANmodul.
    This structure is used with the method :meth:`USBCanServer.get_hardware_info`.

    .. seealso:: :meth:`USBCanServer.get_hardware_info`
    """
    _pack_ = 1
    _fields_ = [
        ("m_dwSize", DWORD),  # size of this structure (only used internally)
        ("m_UcanHandle", Handle),  # USB-CAN-Handle assigned by the DLL
        ("m_bDeviceNr", BYTE),  # device number of the USB-CANmodul
        ("m_dwSerialNr", DWORD),  # serial number from USB-CANmodul
        ("m_dwFwVersionEx", DWORD),  # version of firmware
        ("m_dwProductCode", DWORD),  # product code (see enum :class:`ProductCode`)
        # unique ID (available since V5.01) !!! m_dwSize must be >= HWINFO_SIZE_V2
        ("m_dwUniqueId0", DWORD),
        ("m_dwUniqueId1", DWORD),
        ("m_dwUniqueId2", DWORD),
        ("m_dwUniqueId3", DWORD),
        ("m_dwFlags", DWORD),  # additional flags
    ]

    def __init__(self):
        super(HardwareInfoEx, self).__init__(sizeof(HardwareInfoEx))

    @property
    def device_number(self): return self.m_bDeviceNr

    @property
    def serial(self): return self.m_dwSerialNr

    @property
    def fw_version(self): return self.m_dwFwVersionEx

    @property
    def product_code(self): return self.m_dwProductCode

    @property
    def unique_id(self): return self.m_dwUniqueId0, self.m_dwUniqueId1, self.m_dwUniqueId2, self.m_dwUniqueId3

    @property
    def flags(self): return self.m_dwFlags


# void PUBLIC UcanCallbackFktEx (Handle UcanHandle_p, DWORD dwEvent_p,
#                                BYTE bChannel_p, void* pArg_p);
CallbackFktEx = WINFUNCTYPE(None, Handle, DWORD, BYTE, LPVOID)


class HardwareInitInfo(Structure):
    """
    Structure including information about the enumeration of USB-CANmoduls.

    .. seealso:: :meth:`USBCanServer.enumerate_hardware`

    .. note:: This structure is only used internally.
    """
    _pack_ = 1
    _fields_ = [
        ("m_dwSize", DWORD),  # size of this structure
        ("m_fDoInitialize", BOOL),  # specifies if the found module should be initialized by the DLL
        ("m_pUcanHandle", Handle),  # pointer to variable receiving the USB-CAN-Handle
        ("m_fpCallbackFktEx", CallbackFktEx),  # pointer to callback function
        ("m_pCallbackArg", LPVOID),  # pointer to user defined parameter for callback function
        ("m_fTryNext", BOOL),  # specifies if a further module should be found
    ]


class ChannelInfo(Structure):
    """
    Structure including CAN channel information.
    This structure is used with the method :meth:`USBCanServer.get_hardware_info`.

    .. seealso:: :meth:`USBCanServer.get_hardware_info`
    """
    _pack_ = 1
    _fields_ = [
        ("m_dwSize", DWORD),  # size of this structure
        ("m_bMode", BYTE),  # operation mode of CAN controller (see enum :class:`Mode`)
        ("m_bBTR0", BYTE),  # Bus Timing Register 0 (see enum :class:`Baudrate`)
        ("m_bBTR1", BYTE),  # Bus Timing Register 1 (see enum :class:`Baudrate`)
        ("m_bOCR", BYTE),  # Output Control Register (see enum :class:`OutputControl`)
        ("m_dwAMR", DWORD),  # Acceptance Mask Register (see method :meth:`USBCanServer.set_acceptance`)
        ("m_dwACR", DWORD),  # Acceptance Code Register (see method :meth:`USBCanServer.set_acceptance`)
        ("m_dwBaudrate", DWORD),  # Baudrate Register for all systec USB-CANmoduls
                                  # (see enum :class:`BaudrateEx`)
        ("m_fCanIsInit", BOOL),  # True if the CAN interface is initialized, otherwise false
        ("m_wCanStatus", WORD),  # CAN status (same as received by method :meth:`USBCanServer.get_status`)
    ]

    def __init__(self):
        super(ChannelInfo, self).__init__(sizeof(ChannelInfo))

    @property
    def mode(self): return self.m_bMode

    @property
    def BTR(self): return self.m_bBTR0 << 8 | self.m_bBTR1

    @property
    def OCR(self): return self.m_bOCR

    @property
    def AMR(self): return self.m_dwAMR

    @property
    def ACR(self): return self.m_dwACR

    @property
    def baudrate(self): return self.m_dwBaudrate

    @property
    def can_is_init(self): return self.m_fCanIsInit

    @property
    def can_status(self): return self.m_wCanStatus


class MsgCountInfo(Structure):
    """
    Structure including the number of sent and received CAN messages.
    This structure is used with the method :meth:`USBCanServer.get_msg_count_info`.

    .. seealso:: :meth:`USBCanServer.get_msg_count_info`

    .. note:: This structure is only used internally.
    """
    _fields_ = [
        ("m_wSentMsgCount", WORD),  # number of sent CAN messages
        ("m_wRecvdMsgCount", WORD),  # number of received CAN messages
    ]

    @property
    def sent_msg_count(self): return self.m_wSentMsgCount

    @property
    def recv_msg_count(self): return self.m_wRecvdMsgCount


class VersionType(BYTE):
    """
    Specifies values for receiving the version information of several driver files.

    .. note:: This structure is only used internally.
    """

    #: version of the USB-CAN-library
    VER_TYPE_USER_LIB = 1
    #: equivalent to :attr:`VER_TYPE_USER_LIB`
    VER_TYPE_USER_DLL = 1
    #: version of USBCAN.SYS (not supported in this version)
    VER_TYPE_SYS_DRV = 2
    #: version of firmware in hardware (not supported, use method :meth:`USBCanServer.get_fw_version`)
    VER_TYPE_FIRMWARE = 3
    #: version of UCANNET.SYS
    VER_TYPE_NET_DRV = 4
    #: version of USBCANLD.SYS
    VER_TYPE_SYS_LD = 5
    #: version of USBCANL2.SYS
    VER_TYPE_SYS_L2 = 6
    #: version of USBCANL3.SYS
    VER_TYPE_SYS_L3 = 7
    #: version of USBCANL4.SYS
    VER_TYPE_SYS_L4 = 8
    #: version of USBCANL5.SYS
    VER_TYPE_SYS_L5 = 9
    #: version of USBCANCP.CPL
    VER_TYPE_CPL = 10


# void (PUBLIC *ConnectControlFktEx) (DWORD dwEvent_p, DWORD dwParam_p, void* pArg_p);
ConnectControlFktEx = WINFUNCTYPE(None, DWORD, DWORD, LPVOID)

# typedef void (PUBLIC *EnumCallback) (DWORD dwIndex_p, BOOL fIsUsed_p,
#    HardwareInfoEx* pHwInfoEx_p, HardwareInitInfo* pInitInfo_p, void* pArg_p);
EnumCallback = WINFUNCTYPE(None, DWORD, BOOL, POINTER(HardwareInfoEx), POINTER(HardwareInitInfo), LPVOID)


class USBCanException(Exception):
    """ Base class for USB can errors. """
    def __init__(self, result, func, arguments):
        self.result = result.value
        self.func = func
        self.arguments = arguments
        self.return_msgs = NotImplemented

    def __str__(self):
        return "Function %s returned %d: %s" % \
               (self.func.__name__, self.result, self.return_msgs.get(self.result, "unknown"))


class USBCanError(USBCanException):
    """ Exception class for errors from USB-CAN-library. """
    def __init__(self, result, func, arguments):
        super(USBCanError, self).__init__(result, func, arguments)
        self.return_msgs = {
            ReturnCode.ERR_RESOURCE: "could not created a resource (memory, handle, ...)",
            ReturnCode.ERR_MAXMODULES: "the maximum number of opened modules is reached",
            ReturnCode.ERR_HWINUSE: "the specified module is already in use",
            ReturnCode.ERR_ILLVERSION: "the software versions of the module and library are incompatible",
            ReturnCode.ERR_ILLHW: "the module with the specified device number is not connected "
                                          "(or used by an other application)",
            ReturnCode.ERR_ILLHANDLE: "wrong USB-CAN-Handle handed over to the function",
            ReturnCode.ERR_ILLPARAM: "wrong parameter handed over to the function",
            ReturnCode.ERR_BUSY: "instruction can not be processed at this time",
            ReturnCode.ERR_TIMEOUT: "no answer from module",
            ReturnCode.ERR_IOFAILED: "a request to the driver failed",
            ReturnCode.ERR_DLL_TXFULL: "a CAN message did not fit into the transmit buffer",
            ReturnCode.ERR_MAXINSTANCES: "maximum number of applications is reached",
            ReturnCode.ERR_CANNOTINIT: "CAN interface is not yet initialized",
            ReturnCode.ERR_DISCONECT: "USB-CANmodul was disconnected",
            ReturnCode.ERR_NOHWCLASS: "the needed device class does not exist",
            ReturnCode.ERR_ILLCHANNEL: "illegal CAN channel",
            ReturnCode.ERR_RESERVED1: "reserved",
            ReturnCode.ERR_ILLHWTYPE: "the API function can not be used with this hardware",
        }


class USBCanCmdError(USBCanException):
    """ Exception class for errors from firmware in USB-CANmodul."""
    def __init__(self, result, func, arguments):
        super(USBCanCmdError, self).__init__(result, func, arguments)
        self.return_msgs = {
            ReturnCode.ERRCMD_NOTEQU: "the received response does not match to the transmitted command",
            ReturnCode.ERRCMD_REGTST: "no access to the CAN controller",
            ReturnCode.ERRCMD_ILLCMD: "the module could not interpret the command",
            ReturnCode.ERRCMD_EEPROM: "error while reading the EEPROM",
            ReturnCode.ERRCMD_RESERVED1: "reserved",
            ReturnCode.ERRCMD_RESERVED2: "reserved",
            ReturnCode.ERRCMD_RESERVED3: "reserved",
            ReturnCode.ERRCMD_ILLBDR: "illegal baud rate value specified in BTR0/BTR1 for systec "
                                              "USB-CANmoduls",
            ReturnCode.ERRCMD_NOTINIT: "CAN channel is not initialized",
            ReturnCode.ERRCMD_ALREADYINIT: "CAN channel is already initialized",
            ReturnCode.ERRCMD_ILLSUBCMD: "illegal sub-command specified",
            ReturnCode.ERRCMD_ILLIDX: "illegal index specified (e.g. index for cyclic CAN messages)",
            ReturnCode.ERRCMD_RUNNING: "cyclic CAN message(s) can not be defined because transmission of "
                                               "cyclic CAN messages is already running",
        }


class USBCanWarning(USBCanException):
    """ Exception class for warnings, the function has been executed anyway. """
    def __init__(self, result, func, arguments):
        super(USBCanWarning, self).__init__(result, func, arguments)
        self.return_msgs = {
            ReturnCode.WARN_NODATA: "no CAN messages received",
            ReturnCode.WARN_SYS_RXOVERRUN: "overrun in receive buffer of the kernel driver",
            ReturnCode.WARN_DLL_RXOVERRUN: "overrun in receive buffer of the USB-CAN-library",
            ReturnCode.WARN_RESERVED1: "reserved",
            ReturnCode.WARN_RESERVED2: "reserved",
            ReturnCode.WARN_FW_TXOVERRUN: "overrun in transmit buffer of the firmware (but this CAN message "
                                                  "was successfully stored in buffer of the ibrary)",
            ReturnCode.WARN_FW_RXOVERRUN: "overrun in receive buffer of the firmware (but this CAN message "
                                                  "was successfully read)",
            ReturnCode.WARN_FW_TXMSGLOST: "reserved",
            ReturnCode.WARN_NULL_PTR: "pointer is NULL",
            ReturnCode.WARN_TXLIMIT: "not all CAN messages could be stored to the transmit buffer in "
                                             "USB-CAN-library",
            ReturnCode.WARN_BUSY: "reserved"
        }


def check_valid_rx_can_msg(result):
    """
    Checks if function :meth:`USBCanServer.read_can_msg` returns a valid CAN message.

    :param ReturnCode result: Error code of the function.
    :return: True if a valid CAN messages was received, otherwise False.
    :rtype: bool
    """
    return (result.value == ReturnCode.SUCCESSFUL) or (result.value > ReturnCode.WARNING)


def check_tx_ok(result):
    """
    Checks if function :meth:`USBCanServer.write_can_msg` successfully wrote CAN message(s).

    While using :meth:`USBCanServer.write_can_msg_ex` the number of sent CAN messages can be less than
    the number of CAN messages which should be sent.

    :param ReturnCode result: Error code of the function.
    :return: True if CAN message(s) was(were) written successfully, otherwise False.
    :rtype: bool

    .. :seealso: :const:`ReturnCode.WARN_TXLIMIT`
    """
    return (result.value == ReturnCode.SUCCESSFUL) or (result.value > ReturnCode.WARNING)


def check_tx_success(result):
    """
    Checks if function :meth:`USBCanServer.write_can_msg_ex` successfully wrote all CAN message(s).

    :param ReturnCode result: Error code of the function.
    :return: True if CAN message(s) was(were) written successfully, otherwise False.
    :rtype: bool
    """
    return result.value == ReturnCode.SUCCESSFUL


def check_tx_not_all(result):
    """
    Checks if function :meth:`USBCanServer.write_can_msg_ex` did not sent all CAN messages.

    :param ReturnCode result: Error code of the function.
    :return: True if not all CAN messages were written, otherwise False.
    :rtype: bool
    """
    return result.value == ReturnCode.WARN_TXLIMIT


def check_warning(result):
    """
    Checks if any function returns a warning.

    :param ReturnCode result: Error code of the function.
    :return: True if a function returned warning, otherwise False.
    :rtype: bool
    """
    return result.value >= ReturnCode.WARNING


def check_error(result):
    """
    Checks if any function returns an error from USB-CAN-library.

    :param ReturnCode result: Error code of the function.
    :return: True if a function returned error, otherwise False.
    :rtype: bool
    """
    return (result.value != ReturnCode.SUCCESSFUL) and (result.value < ReturnCode.WARNING)


def check_error_cmd(result):
    """
    Checks if any function returns an error from firmware in USB-CANmodul.

    :param ReturnCode result: Error code of the function.
    :return: True if a function returned error from firmware, otherwise False.
    :rtype: bool
    """
    return (result.value >= ReturnCode.ERRCMD) and (result.value < ReturnCode.WARNING)


def check_result(result, func, arguments):
    if check_warning(result):
        logger.warning(USBCanWarning(result, func, arguments))
    elif check_error(result):
        if check_error_cmd(result):
            raise USBCanCmdError(result, func, arguments)
        else:
            raise USBCanError(result, func, arguments)
    return result

# Give a friendly explanation for the assumption of Windows OS.
assert os.name == "nt", "The Systec adapter driver only runs on Windows"

# Select the proper .DLL for the platform.
# see first note in https://docs.python.org/3.7/library/platform.html
try:
    if sys.maxsize > 2**32:
        usbcan_dll = WinDLL("USBCAN64.dll")
    else:
        usbcan_dll = WinDLL("USBCAN32.dll")
except OSError as e:
    print(e, "\n")
    sys.stderr.write("If you reach this error, try:\n"
        "1) Install the proper 32/64-bit USB-to-CAN driver from https://www.systec-electronic.com/\n"
        "2) Read https://stackoverflow.com/questions/57187566/python-ctypes-loading-dll-throws-oserror-winerror-193-1-is-not-a-valid-win\n")
    sys.exit(-1)

# BOOL PUBLIC UcanSetDebugMode (DWORD dwDbgLevel_p, _TCHAR* pszFilePathName_p, DWORD dwFlags_p);
UcanSetDebugMode = usbcan_dll.UcanSetDebugMode
UcanSetDebugMode.restype = BOOL
UcanSetDebugMode.argtypes = [DWORD, PWCHAR, DWORD]

# DWORD PUBLIC UcanGetVersionEx (VersionType VerType_p);
UcanGetVersionEx = usbcan_dll.UcanGetVersionEx
UcanGetVersionEx.restype = DWORD
UcanGetVersionEx.argtypes = [VersionType]

# DWORD PUBLIC UcanGetFwVersion (Handle UcanHandle_p);
UcanGetFwVersion = usbcan_dll.UcanGetFwVersion
UcanGetFwVersion.restype = DWORD
UcanGetFwVersion.argtypes = [Handle]

# BYTE PUBLIC UcanInitHwConnectControlEx (ConnectControlFktEx fpConnectControlFktEx_p, void* pCallbackArg_p);
UcanInitHwConnectControlEx = usbcan_dll.UcanInitHwConnectControlEx
UcanInitHwConnectControlEx.restype = ReturnCode
UcanInitHwConnectControlEx.argtypes = [ConnectControlFktEx, LPVOID]
UcanInitHwConnectControlEx.errcheck = check_result

# BYTE PUBLIC UcanDeinitHwConnectControl (void)
UcanDeinitHwConnectControl = usbcan_dll.UcanDeinitHwConnectControl
UcanDeinitHwConnectControl.restype = ReturnCode
UcanDeinitHwConnectControl.argtypes = []
UcanDeinitHwConnectControl.errcheck = check_result

# DWORD PUBLIC UcanEnumerateHardware (EnumCallback fpCallback_p, void* pCallbackArg_p,
#    BOOL  fEnumUsedDevs_p,
#    BYTE  bDeviceNrLow_p,     BYTE  bDeviceNrHigh_p,
#    DWORD dwSerialNrLow_p,    DWORD dwSerialNrHigh_p,
#    DWORD dwProductCodeLow_p, DWORD dwProductCodeHigh_p);
UcanEnumerateHardware = usbcan_dll.UcanEnumerateHardware
UcanEnumerateHardware.restype = DWORD
UcanEnumerateHardware.argtypes = [EnumCallback, LPVOID, BOOL, BYTE, BYTE, DWORD, DWORD, DWORD, DWORD]

# BYTE PUBLIC UcanInitHardwareEx (Handle* pUcanHandle_p, BYTE bDeviceNr_p,
#   CallbackFktEx fpCallbackFktEx_p, void* pCallbackArg_p);
UcanInitHardwareEx = usbcan_dll.UcanInitHardwareEx
UcanInitHardwareEx.restype = ReturnCode
UcanInitHardwareEx.argtypes = [POINTER(Handle), BYTE, CallbackFktEx, LPVOID]
UcanInitHardwareEx.errcheck = check_result

# BYTE PUBLIC UcanInitHardwareEx2 (Handle* pUcanHandle_p, DWORD dwSerialNr_p,
#   CallbackFktEx fpCallbackFktEx_p, void* pCallbackArg_p);
UcanInitHardwareEx2 = usbcan_dll.UcanInitHardwareEx2
UcanInitHardwareEx2.restype = ReturnCode
UcanInitHardwareEx2.argtypes = [POINTER(Handle), DWORD, CallbackFktEx, LPVOID]
UcanInitHardwareEx2.errcheck = check_result

# BYTE PUBLIC UcanGetModuleTime (Handle UcanHandle_p, DWORD* pdwTime_p);
UcanGetModuleTime = usbcan_dll.UcanGetModuleTime
UcanGetModuleTime.restype = ReturnCode
UcanGetModuleTime.argtypes = [Handle, PDWORD]
UcanGetModuleTime.errcheck = check_result

# BYTE PUBLIC UcanGetHardwareInfoEx2 (Handle UcanHandle_p,
#   HardwareInfoEx* pHwInfo_p,
#   ChannelInfo* pCanInfoCh0_p, ChannelInfo* pCanInfoCh1_p);
UcanGetHardwareInfoEx2 = usbcan_dll.UcanGetHardwareInfoEx2
UcanGetHardwareInfoEx2.restype = ReturnCode
UcanGetHardwareInfoEx2.argtypes = [Handle, POINTER(HardwareInfoEx), POINTER(ChannelInfo),
                                   POINTER(ChannelInfo)]
UcanGetHardwareInfoEx2.errcheck = check_result

# BYTE PUBLIC UcanInitCanEx2 (Handle UcanHandle_p, BYTE bChannel_p, tUcaninit_canParam* pinit_canParam_p);
UcanInitCanEx2 = usbcan_dll.UcanInitCanEx2
UcanInitCanEx2.restype = ReturnCode
UcanInitCanEx2.argtypes = [Handle, BYTE, POINTER(InitCanParam)]
UcanInitCanEx2.errcheck = check_result

# BYTE PUBLIC UcanSetBaudrateEx (Handle UcanHandle_p,
#   BYTE bChannel_p, BYTE bBTR0_p, BYTE bBTR1_p, DWORD dwBaudrate_p);
UcanSetBaudrateEx = usbcan_dll.UcanSetBaudrateEx
UcanSetBaudrateEx.restype = ReturnCode
UcanSetBaudrateEx.argtypes = [Handle, BYTE, BYTE, BYTE, DWORD]
UcanSetBaudrateEx.errcheck = check_result

# BYTE PUBLIC UcanSetAcceptanceEx (Handle UcanHandle_p, BYTE bChannel_p,
#   DWORD dwAMR_p, DWORD dwACR_p);
UcanSetAcceptanceEx = usbcan_dll.UcanSetAcceptanceEx
UcanSetAcceptanceEx.restype = ReturnCode
UcanSetAcceptanceEx.argtypes = [Handle, BYTE, DWORD, DWORD]
UcanSetAcceptanceEx.errcheck = check_result

# BYTE PUBLIC UcanResetCanEx (Handle UcanHandle_p, BYTE bChannel_p, DWORD dwResetFlags_p);
UcanResetCanEx = usbcan_dll.UcanResetCanEx
UcanResetCanEx.restype = ReturnCode
UcanResetCanEx.argtypes = [Handle, BYTE, DWORD]
UcanResetCanEx.errcheck = check_result

# BYTE PUBLIC UcanReadCanMsgEx (Handle UcanHandle_p, BYTE* pbChannel_p,
#   CanMsg* pCanMsg_p, DWORD* pdwCount_p);
UcanReadCanMsgEx = usbcan_dll.UcanReadCanMsgEx
UcanReadCanMsgEx.restype = ReturnCode
UcanReadCanMsgEx.argtypes = [Handle, PBYTE, POINTER(CanMsg), PDWORD]
UcanReadCanMsgEx.errcheck = check_result

# BYTE PUBLIC UcanWriteCanMsgEx (Handle UcanHandle_p, BYTE bChannel_p,
#   CanMsg* pCanMsg_p, DWORD* pdwCount_p);
UcanWriteCanMsgEx = usbcan_dll.UcanWriteCanMsgEx
UcanWriteCanMsgEx.restype = ReturnCode
UcanWriteCanMsgEx.argtypes = [Handle, BYTE, POINTER(CanMsg), PDWORD]
UcanWriteCanMsgEx.errcheck = check_result

# BYTE PUBLIC UcanGetStatusEx (Handle UcanHandle_p, BYTE bChannel_p, Status* pStatus_p);
UcanGetStatusEx = usbcan_dll.UcanGetStatusEx
UcanGetStatusEx.restype = ReturnCode
UcanGetStatusEx.argtypes = [Handle, BYTE, POINTER(Status)]
UcanGetStatusEx.errcheck = check_result

# BYTE PUBLIC UcanGetMsgCountInfoEx (Handle UcanHandle_p, BYTE bChannel_p,
#   MsgCountInfo* pMsgCountInfo_p);
UcanGetMsgCountInfoEx = usbcan_dll.UcanGetMsgCountInfoEx
UcanGetMsgCountInfoEx.restype = ReturnCode
UcanGetMsgCountInfoEx.argtypes = [Handle, BYTE, POINTER(MsgCountInfo)]
UcanGetMsgCountInfoEx.errcheck = check_result

# BYTE PUBLIC UcanGetMsgPending (Handle UcanHandle_p,
#   BYTE bChannel_p, DWORD dwFlags_p, DWORD* pdwPendingCount_p);
UcanGetMsgPending = usbcan_dll.UcanGetMsgPending
UcanGetMsgPending.restype = ReturnCode
UcanGetMsgPending.argtypes = [Handle, BYTE, DWORD, PDWORD]
UcanGetMsgPending.errcheck = check_result

# BYTE PUBLIC UcanGetCanErrorCounter (Handle UcanHandle_p,
#   BYTE bChannel_p, DWORD* pdwTxErrorCounter_p, DWORD* pdwRxErrorCounter_p);
UcanGetCanErrorCounter = usbcan_dll.UcanGetCanErrorCounter
UcanGetCanErrorCounter.restype = ReturnCode
UcanGetCanErrorCounter.argtypes = [Handle, BYTE, PDWORD, PDWORD]
UcanGetCanErrorCounter.errcheck = check_result

# BYTE PUBLIC UcanSetTxTimeout (Handle UcanHandle_p,
#   BYTE bChannel_p, DWORD dwTxTimeout_p);
UcanSetTxTimeout = usbcan_dll.UcanSetTxTimeout
UcanSetTxTimeout.restype = ReturnCode
UcanSetTxTimeout.argtypes = [Handle, BYTE, DWORD]
UcanSetTxTimeout.errcheck = check_result

# BYTE PUBLIC UcanDeinitCanEx (Handle UcanHandle_p, BYTE bChannel_p);
UcanDeinitCanEx = usbcan_dll.UcanDeinitCanEx
UcanDeinitCanEx.restype = ReturnCode
UcanDeinitCanEx.argtypes = [Handle, BYTE]
UcanDeinitCanEx.errcheck = check_result

# BYTE PUBLIC UcanDeinitHardware (Handle UcanHandle_p);
UcanDeinitHardware = usbcan_dll.UcanDeinitHardware
UcanDeinitHardware.restype = ReturnCode
UcanDeinitHardware.argtypes = [Handle]
UcanDeinitHardware.errcheck = check_result

# BYTE PUBLIC UcanDefineCyclicCanMsg (Handle UcanHandle_p,
#   BYTE bChannel_p, CanMsg* pCanMsgList_p, DWORD dwCount_p);
UcanDefineCyclicCanMsg = usbcan_dll.UcanDefineCyclicCanMsg
UcanDefineCyclicCanMsg.restype = ReturnCode
UcanDefineCyclicCanMsg.argtypes = [Handle, BYTE, POINTER(CanMsg), DWORD]
UcanDefineCyclicCanMsg.errcheck = check_result

# BYTE PUBLIC UcanReadCyclicCanMsg (Handle UcanHandle_p,
#   BYTE bChannel_p, CanMsg* pCanMsgList_p, DWORD* pdwCount_p);
UcanReadCyclicCanMsg = usbcan_dll.UcanReadCyclicCanMsg
UcanReadCyclicCanMsg.restype = ReturnCode
UcanReadCyclicCanMsg.argtypes = [Handle, BYTE, POINTER(CanMsg), PDWORD]
UcanReadCyclicCanMsg.errcheck = check_result

# BYTE PUBLIC UcanEnableCyclicCanMsg (Handle UcanHandle_p,
#   BYTE bChannel_p, DWORD dwFlags_p);
UcanEnableCyclicCanMsg = usbcan_dll.UcanEnableCyclicCanMsg
UcanEnableCyclicCanMsg.restype = ReturnCode
UcanEnableCyclicCanMsg.argtypes = [Handle, BYTE, DWORD]
UcanEnableCyclicCanMsg.errcheck = check_result


class USBCanServer:
    """
    USBCanServer is a Python wrapper class for using the USBCAN32.DLL.

    The module is based on the (c) SYSTEC electronic GmbH USBcanServer wrapped class for .NET programming languages
    such as Visual Basic .NET, Managed C++ and C#.
    """
    _modules_found = []
    _connect_control_ref = None

    def __init__(self):
        self._handle = Handle(INVALID_HANDLE)
        self._is_initialized = False
        self._hw_is_initialized = False
        self._ch_is_initialized = {
            Channel.CHANNEL_CH0: False,
            Channel.CHANNEL_CH1: False
        }
        self._callback_ref = CallbackFktEx(self._callback)
        if self._connect_control_ref is None:
            self._connect_control_ref = ConnectControlFktEx(self._connect_control)
            UcanInitHwConnectControlEx(self._connect_control_ref, None)

    @property
    def is_initialized(self):
        """
        Returns whether hardware interface is initialized.

        :return: True if initialized, otherwise False.
        :rtype: bool
        """
        return self._is_initialized

    @property
    def is_can0_initialized(self):
        """
        Returns whether CAN interface for channel 0 is initialized.

        :return: True if initialized, otherwise False.
        :rtype: bool
        """
        return self._ch_is_initialized[Channel.CHANNEL_CH0]

    @property
    def is_can1_initialized(self):
        """
        Returns whether CAN interface for channel 1 is initialized.

        :return: True if initialized, otherwise False.
        :rtype: bool
        """
        return self._ch_is_initialized[Channel.CHANNEL_CH1]

    @classmethod
    def _enum_callback(cls, index, is_used, hw_info_ex, init_info, arg):
        cls._modules_found.append((index, bool(is_used), hw_info_ex.contents, init_info.contents))

    @classmethod
    def enumerate_hardware(cls, device_number_low=0, device_number_high=-1, serial_low=0, serial_high=-1,
                           product_code_low=0, product_code_high=-1, enum_used_devices=False):
        cls._modules_found = []
        UcanEnumerateHardware(cls._enum_callback_ref, None, enum_used_devices,
                              device_number_low, device_number_high,
                              serial_low, serial_high,
                              product_code_low, product_code_high)
        return cls._modules_found

    def init_hardware(self, serial=None, device_number=ANY_MODULE):
        """
        Initializes the device with the corresponding serial or device number.

        :param int or None serial: Serial number of the USB-CANmodul.
        :param int device_number: Device number (0 - 254, or :const:`ANY_MODULE` for the first device).
        """
        if not self._hw_is_initialized:
            # initialize hardware either by device number or serial
            if serial is None:
                UcanInitHardwareEx(byref(self._handle), device_number, self._callback_ref, None)
            else:
                UcanInitHardwareEx2(byref(self._handle), serial, self._callback_ref, None)
            self._hw_is_initialized = True

    def init_can(self, channel=Channel.CHANNEL_CH0, BTR=Baudrate.BAUD_1MBit, baudrate=BaudrateEx.BAUDEX_USE_BTR01,
                 AMR=AMR_ALL, ACR=ACR_ALL, mode=Mode.MODE_NORMAL, OCR=OutputControl.OCR_DEFAULT,
                 rx_buffer_entries=DEFAULT_BUFFER_ENTRIES, tx_buffer_entries=DEFAULT_BUFFER_ENTRIES):
        """
        Initializes a specific CAN channel of a device.

        :param int channel: CAN channel to be initialized (:data:`Channel.CHANNEL_CH0` or :data:`Channel.CHANNEL_CH1`).
        :param int BTR:
            Baud rate register BTR0 as high byte, baud rate register BTR1 as low byte (see enum :class:`Baudrate`).
        :param int baudrate: Baud rate register for all systec USB-CANmoduls (see enum :class:`BaudrateEx`).
        :param int AMR: Acceptance filter mask (see method :meth:`set_acceptance`).
        :param int ACR: Acceptance filter code (see method :meth:`set_acceptance`).
        :param int mode: Transmission mode of CAN channel (see enum :class:`Mode`).
        :param int OCR: Output Control Register (see enum :class:`OutputControl`).
        :param int rx_buffer_entries: The number of maximum entries in the receive buffer.
        :param int tx_buffer_entries: The number of maximum entries in the transmit buffer.
        """
        if not self._ch_is_initialized.get(channel, False):
            init_param = InitCanParam(mode, BTR, OCR, AMR, ACR, baudrate, rx_buffer_entries, tx_buffer_entries)
            UcanInitCanEx2(self._handle, channel, init_param)
            self._ch_is_initialized[channel] = True

    def read_can_msg(self, channel, count):
        """
        Reads one or more CAN-messages from the buffer of the specified CAN channel.

        :param int channel:
            CAN channel to read from (:data:`Channel.CHANNEL_CH0`, :data:`Channel.CHANNEL_CH1`,
            :data:`Channel.CHANNEL_ANY`).
        :param int count: The number of CAN messages to be received.
        :return: Tuple with list of CAN message/s received and the CAN channel where the read CAN messages came from.
        :rtype: tuple(list(CanMsg), int)
        """
        c_channel = BYTE(channel)
        c_can_msg = (CanMsg * count)()
        c_count = DWORD(count)
        UcanReadCanMsgEx(self._handle, byref(c_channel), c_can_msg, byref(c_count))
        return c_can_msg[:c_count.value], c_channel.value

    def write_can_msg(self, channel, can_msg):
        """
        Transmits one ore more CAN messages through the specified CAN channel of the device.

        :param int channel:
            CAN channel, which is to be used (:data:`Channel.CHANNEL_CH0` or :data:`Channel.CHANNEL_CH1`).
        :param list(CanMsg) can_msg: List of CAN message structure (see structure :class:`CanMsg`).
        :return: The number of successfully transmitted CAN messages.
        :rtype: int
        """
        c_can_msg = (CanMsg * len(can_msg))(*can_msg)
        c_count = DWORD(len(can_msg))
        UcanWriteCanMsgEx(self._handle, channel, c_can_msg, c_count)
        return c_count

    def set_baudrate(self, channel, BTR, baudarate):
        """
        This function is used to configure the baud rate of specific CAN channel of a device.

        :param int channel:
            CAN channel, which is to be configured (:data:`Channel.CHANNEL_CH0` or :data:`Channel.CHANNEL_CH1`).
        :param int BTR:
            Baud rate register BTR0 as high byte, baud rate register BTR1 as low byte (see enum :class:`Baudrate`).
        :param int baudarate: Baud rate register for all systec USB-CANmoduls (see enum :class:`BaudrateEx`>).
        """
        UcanSetBaudrateEx(self._handle, channel, BTR >> 8, BTR, baudarate)

    def set_acceptance(self, channel=Channel.CHANNEL_CH0, AMR=AMR_ALL, ACR=ACR_ALL):
        """
        This function is used to change the acceptance filter values for a specific CAN channel on a device.

        :param int channel:
            CAN channel, which is to be configured (:data:`Channel.CHANNEL_CH0` or :data:`Channel.CHANNEL_CH1`).
        :param int AMR: Acceptance filter mask (AMR).
        :param int ACR: Acceptance filter code (ACR).
        """
        UcanSetAcceptanceEx(self._handle, channel, AMR, ACR)

    def get_status(self, channel=Channel.CHANNEL_CH0):
        """
        Returns the error status of a specific CAN channel.

        :param int channel: CAN channel, to be used (:data:`Channel.CHANNEL_CH0` or :data:`Channel.CHANNEL_CH1`).
        :return: Tuple with CAN and USB status (see structure :class:`Status`).
        :rtype: tuple(int, int)
        """
        status = Status()
        UcanGetStatusEx(self._handle, channel, byref(status))
        return status.can_status, status.usb_status

    def get_msg_count_info(self, channel=Channel.CHANNEL_CH0):
        """
        Reads the message counters of the specified CAN channel.

        :param int channel:
            CAN channel, which is to be used (:data:`Channel.CHANNEL_CH0` or :data:`Channel.CHANNEL_CH1`).
        :return: Tuple with number of CAN messages sent and received.
        :rtype: tuple(int, int)
        """
        msg_count_info = MsgCountInfo()
        UcanGetMsgCountInfoEx(self._handle, channel, byref(msg_count_info))
        return msg_count_info.sent_msg_count, msg_count_info.recv_msg_count

    def reset_can(self, chanel=Channel.CHANNEL_CH0, flags=ResetFlags.RESET_ALL):
        """
        Resets a CAN channel of a device (hardware reset, empty buffer, and so on).

        :param int chanel: CAN channel, to be reset (:data:`Channel.CHANNEL_CH0` or :data:`Channel.CHANNEL_CH1`).
        :param int flags: Flags defines what should be reset (see enum :class:`ResetFlags`).
        """
        UcanResetCanEx(self._handle, chanel, flags)

    def get_hardware_info(self):
        """
        Returns the extended hardware information of a device. With multi-channel USB-CANmoduls the information for
        both CAN channels are returned separately.

        :return:
            Tuple with extended hardware information structure (see structure :class:`HardwareInfoEx`) and
            structures with information of CAN channel 0 and 1 (see structure :class:`ChannelInfo`).
        :rtype: tuple(HardwareInfoEx, ChannelInfo, ChannelInfo)
        """
        hw_info_ex = HardwareInfoEx()
        can_info_ch0, can_info_ch1 = ChannelInfo(), ChannelInfo()
        UcanGetHardwareInfoEx2(self._handle, byref(hw_info_ex), byref(can_info_ch0), byref(can_info_ch1))
        return hw_info_ex, can_info_ch0, can_info_ch1

    def get_fw_version(self):
        """
        Returns the firmware version number of the device.

        :return: Firmware version number.
        :rtype: int
        """
        return UcanGetFwVersion(self._handle)

    def define_cyclic_can_msg(self, channel, can_msg=None):
        """
        Defines a list of CAN messages for automatic transmission.

        :param int channel: CAN channel, to be used (:data:`Channel.CHANNEL_CH0` or :data:`Channel.CHANNEL_CH1`).
        :param list(CanMsg) can_msg:
            List of CAN messages (up to 16, see structure :class:`CanMsg`), or None to delete an older list.
        """
        if can_msg is not None:
            c_can_msg = (CanMsg * len(can_msg))(*can_msg)
            c_count = DWORD(len(can_msg))
        else:
            c_can_msg = CanMsg()
            c_count = 0
        UcanDefineCyclicCanMsg(self._handle, channel, c_can_msg, c_count)

    def read_cyclic_can_msg(self, channel, count):
        """
        Reads back the list of CAN messages for automatically sending.

        :param int channel: CAN channel, to be used (:data:`Channel.CHANNEL_CH0` or :data:`Channel.CHANNEL_CH1`).
        :param int count: The number of cyclic CAN messages to be received.
        :return: List of received CAN messages (up to 16, see structure :class:`CanMsg`).
        :rtype: list(CanMsg)
        """
        c_channel = BYTE(channel)
        c_can_msg = (CanMsg * count)()
        c_count = DWORD(count)
        UcanReadCyclicCanMsg(self._handle, byref(c_channel), c_can_msg, c_count)
        return c_can_msg[:c_count.value]

    def enable_cyclic_can_msg(self, channel, flags):
        """
        Enables or disables the automatically sending.

        :param int channel: CAN channel, to be used (:data:`Channel.CHANNEL_CH0` or :data:`Channel.CHANNEL_CH1`).
        :param int flags: Flags for enabling or disabling (see enum :class:`CyclicFlags`).
        """
        UcanEnableCyclicCanMsg(self._handle, channel, flags)

    def get_msg_pending(self, channel, flags):
        """
        Returns the number of pending CAN messages.

        :param int channel: CAN channel, to be used (:data:`Channel.CHANNEL_CH0` or :data:`Channel.CHANNEL_CH1`).
        :param int flags: Flags specifies which buffers should be checked (see enum :class:`PendingFlags`).
        :return: The number of pending messages.
        :rtype: int
        """
        count = DWORD(0)
        UcanGetMsgPending(self._handle, channel, flags, byref(count))
        return count

    def get_can_error_counter(self, channel):
        """
        Reads the current value of the error counters within the CAN controller.

        :param int channel: CAN channel, to be used (:data:`Channel.CHANNEL_CH0` or :data:`Channel.CHANNEL_CH1`).
        :return: Tuple with the TX and RX error counter.
        :rtype: tuple(int, int)

        .. note:: Only available for systec USB-CANmoduls (NOT for GW-001 and GW-002 !!!).
        """
        tx_error_counter = DWORD(0)
        rx_error_counter = DWORD(0)
        UcanGetCanErrorCounter(self._handle, channel, byref(tx_error_counter), byref(rx_error_counter))
        return tx_error_counter, rx_error_counter

    def set_tx_timeout(self, channel, timeout):
        """
        Sets the transmission timeout.

        :param int channel: CAN channel, to be used (:data:`Channel.CHANNEL_CH0` or :data:`Channel.CHANNEL_CH1`).
        :param float timeout: Transmit timeout in seconds (value 0 disables this feature).
        """
        UcanSetTxTimeout(self._handle, channel, int(timeout * 1000))

    def shutdown(self, channel=Channel.CHANNEL_ALL, shutdown_hardware=True):
        """
        Shuts down all CAN interfaces and/or the hardware interface.

        :param int channel:
            CAN channel, to be used (:data:`Channel.CHANNEL_CH0`, :data:`Channel.CHANNEL_CH1` or
            :data:`Channel.CHANNEL_ALL`)
        :param bool shutdown_hardware: If true then the hardware interface will be closed too.
        """
        # shutdown each channel if it's initialized
        for _channel, is_initialized in self._ch_is_initialized.items():
            if is_initialized and (_channel == channel or channel == Channel.CHANNEL_ALL or shutdown_hardware):
                UcanDeinitCanEx(self._handle, _channel)
                self._ch_is_initialized[_channel] = False

        # shutdown hardware
        if self._hw_is_initialized and shutdown_hardware:
            UcanDeinitHardware(self._handle)
            self._hw_is_initialized = False
            self._handle = Handle(INVALID_HANDLE)

    @staticmethod
    def get_user_dll_version():
        """
        Returns the version number of the USBCAN-library.

        :return: Software version number.
        :rtype: int
        """
        return UcanGetVersionEx(VersionType.VER_TYPE_USER_DLL)

    @staticmethod
    def set_debug_mode(level, filename, flags=0):
        """
        This function enables the creation of a debug log file out of the USBCAN-library. If this
        feature has already been activated via the USB-CANmodul Control, the content of the
        “old” log file will be copied to the new file. Further debug information will be appended to
        the new file.

        :param int level: Debug level (bit format).
        :param str filename: File path to debug log file.
        :param int flags: Additional flags (bit0: file append mode).
        :return: False if logfile not created otherwise True.
        :rtype: bool
        """
        return UcanSetDebugMode(level, filename, flags)

    @staticmethod
    def get_can_status_message(can_status):
        """
        Converts a given CAN status value to the appropriate message string.

        :param can_status: CAN status value from method :meth:`get_status` (see enum :class:`CanStatus`)
        :return: Status message string.
        :rtype: str
        """
        status_msgs = {
            CanStatus.CANERR_TXMSGLOST: "Transmit message lost",
            CanStatus.CANERR_MEMTEST: "Memory test failed",
            CanStatus.CANERR_REGTEST: "Register test failed",
            CanStatus.CANERR_QXMTFULL: "Transmit queue is full",
            CanStatus.CANERR_QOVERRUN: "Receive queue overrun",
            CanStatus.CANERR_QRCVEMPTY: "Receive queue is empty",
            CanStatus.CANERR_BUSOFF: "Bus Off",
            CanStatus.CANERR_BUSHEAVY: "Error Passive",
            CanStatus.CANERR_BUSLIGHT: "Warning Limit",
            CanStatus.CANERR_OVERRUN: "Rx-buffer is full",
            CanStatus.CANERR_XMTFULL: "Tx-buffer is full",
        }
        return "OK" if can_status == CanStatus.CANERR_OK \
            else ", ".join(msg for status, msg in status_msgs.items() if can_status & status)

    @staticmethod
    def get_baudrate_message(baudrate):
        """
        Converts a given baud rate value for GW-001/GW-002 to the appropriate message string.

        :param Baudrate baudrate:
            Bus Timing Registers, BTR0 in high order byte and BTR1 in low order byte
            (see enum :class:`Baudrate`)
        :return: Baud rate message string.
        :rtype: str
        """
        baudrate_msgs = {
            Baudrate.BAUD_AUTO: "auto baudrate",
            Baudrate.BAUD_10kBit: "10 kBit/sec",
            Baudrate.BAUD_20kBit: "20 kBit/sec",
            Baudrate.BAUD_50kBit: "50 kBit/sec",
            Baudrate.BAUD_100kBit: "100 kBit/sec",
            Baudrate.BAUD_125kBit: "125 kBit/sec",
            Baudrate.BAUD_250kBit: "250 kBit/sec",
            Baudrate.BAUD_500kBit: "500 kBit/sec",
            Baudrate.BAUD_800kBit: "800 kBit/sec",
            Baudrate.BAUD_1MBit: "1 MBit/s",
            Baudrate.BAUD_USE_BTREX: "BTR Ext is used",
        }
        return baudrate_msgs.get(baudrate, "BTR is unknown (user specific)")

    @staticmethod
    def get_baudrate_ex_message(baudrate_ex):
        """
        Converts a given baud rate value for systec USB-CANmoduls to the appropriate message string.

        :param BaudrateEx baudrate_ex: Bus Timing Registers (see enum :class:`BaudrateEx`)
        :return: Baud rate message string.
        :rtype: str
        """
        baudrate_ex_msgs = {
            Baudrate.BAUDEX_AUTO: "auto baudrate",
            Baudrate.BAUDEX_10kBit: "10 kBit/sec",
            Baudrate.BAUDEX_SP2_10kBit: "10 kBit/sec",
            Baudrate.BAUDEX_20kBit: "20 kBit/sec",
            Baudrate.BAUDEX_SP2_20kBit: "20 kBit/sec",
            Baudrate.BAUDEX_50kBit: "50 kBit/sec",
            Baudrate.BAUDEX_SP2_50kBit: "50 kBit/sec",
            Baudrate.BAUDEX_100kBit: "100 kBit/sec",
            Baudrate.BAUDEX_SP2_100kBit: "100 kBit/sec",
            Baudrate.BAUDEX_125kBit: "125 kBit/sec",
            Baudrate.BAUDEX_SP2_125kBit: "125 kBit/sec",
            Baudrate.BAUDEX_250kBit: "250 kBit/sec",
            Baudrate.BAUDEX_SP2_250kBit: "250 kBit/sec",
            Baudrate.BAUDEX_500kBit: "500 kBit/sec",
            Baudrate.BAUDEX_SP2_500kBit: "500 kBit/sec",
            Baudrate.BAUDEX_800kBit: "800 kBit/sec",
            Baudrate.BAUDEX_SP2_800kBit: "800 kBit/sec",
            Baudrate.BAUDEX_1MBit: "1 MBit/s",
            Baudrate.BAUDEX_SP2_1MBit: "1 MBit/s",
            Baudrate.BAUDEX_USE_BTR01: "BTR0/BTR1 is used",
        }
        return baudrate_ex_msgs.get(baudrate_ex, "BTR is unknown (user specific)")

    @classmethod
    def convert_to_major_ver(cls, version):
        """
        Converts the a version number into the major version.

        :param int version: Version number to be converted.
        :return: Major version.
        :rtype: int
        """
        return version & 0xFF

    @classmethod
    def convert_to_minor_ver(cls, version):
        """
        Converts the a version number into the minor version.

        :param int version: Version number to be converted.
        :return: Minor version.
        :rtype: int
        """
        return (version & 0xFF00) >> 8

    @classmethod
    def convert_to_release_ver(cls, version):
        """
        Converts the a version number into the release version.

        :param int version: Version number to be converted.
        :return: Release version.
        :rtype: int
        """
        return (version & 0xFFFF0000) >> 16

    @classmethod
    def check_version_is_equal_or_higher(cls, version, cmp_major, cmp_minor):
        """
        Checks if the version is equal or higher than a specified value.

        :param int version: Version number to be checked.
        :param int cmp_major: Major version to be compared with.
        :param int cmp_minor: Minor version to be compared with.
        :return: True if equal or higher, otherwise False.
        :rtype: bool
        """
        return (cls.convert_to_major_ver(version) > cmp_major) or \
               (cls.convert_to_major_ver(version) == cmp_major and cls.convert_to_minor_ver(version) >= cmp_minor)

    @classmethod
    def check_is_systec(cls, hw_info_ex):
        """
        Checks whether the module is a systec USB-CANmodul.

        :param HardwareInfoEx hw_info_ex:
            Extended hardware information structure (see method :meth:`get_hardware_info`).
        :return: True when the module is a systec USB-CANmodul, otherwise False.
        :rtype: bool
        """
        return (hw_info_ex.m_dwProductCode & PRODCODE_MASK_PID) >= ProductCode.PRODCODE_PID_MULTIPORT

    @classmethod
    def check_is_G4(cls, hw_info_ex):
        """
        Checks whether the module is an USB-CANmodul of fourth generation (G4).

        :param HardwareInfoEx hw_info_ex:
            Extended hardware information structure (see method :meth:`get_hardware_info`).
        :return: True when the module is an USB-CANmodul G4, otherwise False.
        :rtype: bool
        """
        return hw_info_ex.m_dwProductCode & PRODCODE_PID_G4

    @classmethod
    def check_is_G3(cls, hw_info_ex):
        """
        Checks whether the module is an USB-CANmodul of third generation (G3).

        :param HardwareInfoEx hw_info_ex:
            Extended hardware information structure (see method :meth:`get_hardware_info`).
        :return: True when the module is an USB-CANmodul G3, otherwise False.
        :rtype: bool
        """
        return cls.check_is_systec(hw_info_ex) and not cls.check_is_G4(hw_info_ex)

    @classmethod
    def check_support_cyclic_msg(cls, hw_info_ex):
        """
        Checks whether the module supports automatically transmission of cyclic CAN messages.

        :param HardwareInfoEx hw_info_ex:
            Extended hardware information structure (see method :meth:`get_hardware_info`).
        :return: True when the module does support cyclic CAN messages, otherwise False.
        :rtype: bool
        """
        return cls.check_is_systec(hw_info_ex) and \
               cls.check_version_is_equal_or_higher(hw_info_ex.m_dwFwVersionEx, 3, 6)

    @classmethod
    def check_support_two_channel(cls, hw_info_ex):
        """
        Checks whether the module supports two CAN channels (at logical device).

        :param HardwareInfoEx hw_info_ex:
            Extended hardware information structure (see method :meth:`get_hardware_info`).
        :return: True when the module (logical device) does support two CAN channels, otherwise False.
        :rtype: bool
        """
        return cls.check_is_systec(hw_info_ex) and (hw_info_ex.m_dwProductCode & PRODCODE_PID_TWO_CHA)

    @classmethod
    def check_support_term_resistor(cls, hw_info_ex):
        """
        Checks whether the module supports a termination resistor at the CAN bus.

        :param HardwareInfoEx hw_info_ex:
            Extended hardware information structure (see method :meth:`get_hardware_info`).
        :return: True when the module does support a termination resistor.
        :rtype: bool
        """
        return hw_info_ex.m_dwProductCode & PRODCODE_PID_TERM

    @classmethod
    def check_support_user_port(cls, hw_info_ex):
        """
        Checks whether the module supports a user I/O port.

        :param HardwareInfoEx hw_info_ex:
            Extended hardware information structure (see method :meth:`get_hardware_info`).
        :return: True when the module supports a user I/O port, otherwise False.
        :rtype: bool
        """
        return ((hw_info_ex.m_dwProductCode & PRODCODE_MASK_PID) != ProductCode.PRODCODE_PID_BASIC) \
               and ((hw_info_ex.m_dwProductCode & PRODCODE_MASK_PID) != ProductCode.PRODCODE_PID_RESERVED1) \
               and cls.check_version_is_equal_or_higher(hw_info_ex.m_dwFwVersionEx, 2, 16)

    @classmethod
    def check_support_rb_user_port(cls, hw_info_ex):
        """
        Checks whether the module supports a user I/O port including read back feature.

        :param HardwareInfoEx hw_info_ex:
            Extended hardware information structure (see method :meth:`get_hardware_info`).
        :return: True when the module does support a user I/O port including the read back feature, otherwise False.
        :rtype: bool
        """
        return hw_info_ex.m_dwProductCode & PRODCODE_PID_RBUSER

    @classmethod
    def check_support_rb_can_port(cls, hw_info_ex):
        """
        Checks whether the module supports a CAN I/O port including read back feature.

        :param HardwareInfoEx hw_info_ex:
            Extended hardware information structure (see method :meth:`get_hardware_info`).
        :return: True when the module does support a CAN I/O port including the read back feature, otherwise False.
        :rtype: bool
        """
        return hw_info_ex.m_dwProductCode & PRODCODE_PID_RBCAN

    @classmethod
    def check_support_ucannet(cls, hw_info_ex):
        """
        Checks whether the module supports the usage of USB-CANnetwork driver.

        :param HardwareInfoEx hw_info_ex:
            Extended hardware information structure (see method :meth:`get_hardware_info`).
        :return: True when the module does support the usage of the USB-CANnetwork driver, otherwise False.
        :rtype: bool
        """
        return cls.check_is_systec(hw_info_ex) and \
               cls.check_version_is_equal_or_higher(hw_info_ex.m_dwFwVersionEx, 3, 8)

    @classmethod
    def calculate_amr(cls, is_extended, from_id, to_id, rtr_only=False, rtr_too=True):
        """
        Calculates AMR using CAN-ID range as parameter.

        :param bool is_extended: If True parameters from_id and to_id contains 29-bit CAN-ID.
        :param int from_id: First CAN-ID which should be received.
        :param int to_id: Last CAN-ID which should be received.
        :param bool rtr_only: If True only RTR-Messages should be received, and rtr_too will be ignored.
        :param bool rtr_too: If True CAN data frames and RTR-Messages should be received.
        :return: Value for AMR.
        :rtype: int
        """
        return (((from_id ^ to_id) << 3) | (0x7 if rtr_too and not rtr_only else 0x3)) if is_extended else \
            (((from_id ^ to_id) << 21) | (0x1FFFFF if rtr_too and not rtr_only else 0xFFFFF))

    @classmethod
    def calculate_acr(cls, is_extended, from_id, to_id, rtr_only=False, rtr_too=True):
        """
        Calculates ACR using CAN-ID range as parameter.

        :param bool is_extended: If True parameters from_id and to_id contains 29-bit CAN-ID.
        :param int from_id: First CAN-ID which should be received.
        :param int to_id: Last CAN-ID which should be received.
        :param bool rtr_only: If True only RTR-Messages should be received, and rtr_too will be ignored.
        :param bool rtr_too: If True CAN data frames and RTR-Messages should be received.
        :return: Value for ACR.
        :rtype: int
        """
        return (((from_id & to_id) << 3) | (0x04 if rtr_only else 0)) if is_extended else \
            (((from_id & to_id) << 21) | (0x100000 if rtr_only else 0))

    def _connect_control(self, event, param, arg):
        """
        Is the actual callback function for :meth:`init_hw_connect_control_ex`.

        :param event:
            Event (:data:`CbEvent.EVENT_CONNECT`, :data:`CbEvent.EVENT_DISCONNECT` or
            :data:`CbEvent.EVENT_FATALDISCON`).
        :param param: Additional parameter depending on the event.
        - CbEvent.EVENT_CONNECT: always 0
        - CbEvent.EVENT_DISCONNECT: always 0
        - CbEvent.EVENT_FATALDISCON: USB-CAN-Handle of the disconnected module
        :param arg: Additional parameter defined with :meth:`init_hardware_ex` (not used in this wrapper class).
        """
        logger.debug("Event: %s, Param: %s" % (event, param))

        if event == CbEvent.EVENT_FATALDISCON:
            self.fatal_disconnect_event(param)
        elif event == CbEvent.EVENT_CONNECT:
            self.connect_event()
        elif event == CbEvent.EVENT_DISCONNECT:
            self.disconnect_event()

    def _callback(self, handle, event, channel, arg):
        """
        Is called if a working event occurred.

        :param int handle: USB-CAN-Handle returned by the function :meth:`init_hardware`.
        :param int event: Event type.
        :param int channel:
            CAN channel (:data:`Channel.CHANNEL_CH0`, :data:`Channel.CHANNEL_CH1` or :data:`Channel.CHANNEL_ANY`).
        :param arg: Additional parameter defined with :meth:`init_hardware_ex`.
        """
        logger.debug("Handle: %s, Event: %s, Channel: %s" % (handle, event, channel))

        if event == CbEvent.EVENT_INITHW:
            self.init_hw_event()
        elif event == CbEvent.EVENT_init_can:
            self.init_can_event(channel)
        elif event == CbEvent.EVENT_RECEIVE:
            self.can_msg_received_event(channel)
        elif event == CbEvent.EVENT_STATUS:
            self.status_event(channel)
        elif event == CbEvent.EVENT_DEINIT_CAN:
            self.deinit_can_event(channel)
        elif event == CbEvent.EVENT_DEINITHW:
            self.deinit_hw_event()

    def init_hw_event(self):
        """
        Event occurs when an USB-CANmodul has been initialized (see method :meth:`init_hardware`).

        .. note:: To be overridden by subclassing.
        """
        pass

    def init_can_event(self, channel):
        """
        Event occurs when a CAN interface of an USB-CANmodul has been initialized.

        :param int channel: Specifies the CAN channel which was initialized (see method :meth:`init_can`).

        .. note:: To be overridden by subclassing.
        """
        pass

    def can_msg_received_event(self, channel):
        """
        Event occurs when at leas one CAN message has been received.

        Call the method :meth:`read_can_msg` to receive the CAN messages.

        :param int channel: Specifies the CAN channel which received CAN messages.

        .. note:: To be overridden by subclassing.
        """
        pass

    def status_event(self, channel):
        """
        Event occurs when the error status of a module has been changed.

        Call the method :meth:`get_status` to receive the error status.

        :param int channel: Specifies the CAN channel which status has been changed.

        .. note:: To be overridden by subclassing.
        """
        pass

    def deinit_can_event(self, channel):
        """
        Event occurs when a CAN interface has been deinitialized (see method :meth:`shutdown`).

        :param int channel: Specifies the CAN channel which status has been changed.

        .. note:: To be overridden by subclassing.
        """
        pass

    def deinit_hw_event(self):
        """
        Event occurs when an USB-CANmodul has been deinitialized (see method :meth:`shutdown`).

        .. note:: To be overridden by subclassing.
        """
        pass

    def connect_event(self):
        """
        Event occurs when a new USB-CANmodul has been connected to the host.

        .. note:: To be overridden by subclassing.
        """
        pass

    def disconnect_event(self):
        """
        Event occurs when an USB-CANmodul has been disconnected from the host.

        .. note:: To be overridden by subclassing.
        """
        pass

    def fatal_disconnect_event(self, device_number):
        """
        Event occurs when an USB-CANmodul has been disconnected from the host which was currently initialized.

        No method can be called for this module.

        :param int device_number: The device number which was disconnected.

        .. note:: To be overridden by subclassing.
        """
        pass


USBCanServer._enum_callback_ref = EnumCallback(USBCanServer._enum_callback)
