#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Defines MMR3 and MRHT class.

For users:

>>> mmr3 = MMR3("ip_address")

Attributes can be directly accessed by their name. Ex:

>>> mmr3.temperature

returns the temperature of the sensors.
If the attribute is writable, you can set its value by:

>>> mmr3.period = 80e-3

Channels values (R, T, ...) are accessible by MMR3.chan1, .chan2, .chan3. Ex:
>>> mmr3.chan1.R

returns the measured resistance of the first channel.
"""


import socket


class MACRTConn:
    """Base class for MMR3, MRHT, ..."""
    # Listen socket port: 12000
    # MMR3 port : 12000 + last IPaddr port
    # ex: 192.168.137.100 | port = 12000 + 100 = 12100
    def __init__(self, addr, timeout=2):
        """Initialisation:
    arguments:
    * addr: ip_address of the iMACRT module
    * timeout: close the connexion after 'timeout' seconds, default to 2"""
        self.addr = addr
        self.port = 12000 + int(self.addr.split('.')[3])
        self.timeout = timeout

    def open_sock(self):
        "Create and configure the communication socket."
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        except AttributeError:
            # Some systems don't support SO_REUSEADDR
            pass
        sock.settimeout(self.timeout)
        sock.bind(('', 12000))
        return sock

    def ask(self, command):
        "Send 'command' to the iMACRT, wait for the response and returns it"
        cmd = command.encode('ascii')
        sock = self.open_sock()
        res = sock.sendto(cmd, (self.addr, self.port))
        if res != len(cmd):
            raise IOError
        ret = sock.recv(1024)
        sock.close()
        return ret.decode('ascii')


class MACRTMeta(type):
    "Meta-class creates the class properties"
    def __new__(mcs, name, bases, dct):
        "Called for the class creation."
        def __get_cmd(prop_idx):
            "Common function to get attributes from the iMACRT module."
            def func(obj):
                "Format the 'get_cmd' string"
                get_cmd = getattr(obj, 'get_cmd', "")
                chan_idx = getattr(obj, 'chan_idx', 0)
                idx_offset = getattr(obj, 'idx_offset', 0)
                idx_sum = prop_idx + idx_offset
                cmd = get_cmd.format(**locals())
                return float(obj.ask(cmd))
            return func

        def __set_cmd(prop_idx):
            "Common function to set attributes to the iMACRT module."
            def func(obj, value):
                "Format the 'set_cmd' string"
                set_cmd = getattr(obj, 'set_cmd', "")
                chan_idx = getattr(obj, 'chan_idx', 0)
                idx_offset = getattr(obj, 'idx_offset', 0)
                chan_idx = getattr(obj, 'chan_idx', 0)
                idx_sum = prop_idx + idx_offset
                cmd = set_cmd.format(**locals())
                return obj.ask(cmd)
            return func

        cls = super(MACRTMeta, mcs).__new__(mcs, name, bases, dct)
        properties = dct.get('properties', [])

        for idx, (name, writable) in enumerate(properties):
            if writable:
                prop = property(
                    __get_cmd(idx),
                    __set_cmd(idx),
                    None)
            else:
                prop = property(__get_cmd(idx), None, None)
            setattr(cls, name, prop)
        return cls


class MMR3(MACRTConn, metaclass=MACRTMeta):
    "MMR3 class. High precision thermometer."
    get_cmd = 'MMR3GET {idx_sum}'
    set_cmd = 'MMR3SET {idx_sum} {value}'
    properties = (('period', True), ('DtADC', True), ('temperature', False))

    def __init__(self, *args, **kwargs):
        super(MMR3, self).__init__(*args, **kwargs)
        for i in range(1, 4):
            setattr(self, 'chan' + str(i),
                    MMR3Chan(self, i, 3 + (i - 1) * 11))


class MMR3Chan(metaclass=MACRTMeta):
    "MMR3Chan class, channel specific properties. High precision thermometer."
    properties = (('R', False), ('range', False), ('X', False),
                  ('status', False), ('avg', True), ('range_mode', True),
                  ('range_mode_I', True), ('range_I', True), ('range_U', True),
                  ('I', True), ('offset', False))

    def __init__(self, parent, chan_idx=0, idx_offset=0):
        self.ask = parent.ask
        self.get_cmd = parent.get_cmd
        self.set_cmd = parent.set_cmd
        self.idx_offset = idx_offset
        self.chan_idx = chan_idx


class MRHT(MACRTConn, metaclass=MACRTMeta):
    "MRHT class, fast measurement."
    get_cmd = 'MRHTGET {idx_sum}'
    set_cmd = 'MRHTSET {idx_sum} {value}'
    properties = (('period', True), ('DtADC', True), ('temperature', False))

    def __init__(self, *args, **kwargs):
        super(MRHT, self).__init__(*args, **kwargs)
        for i in range(1, 4):
            setattr(self, 'chan' + str(i),
                    MRHTChan(self, i, 256 * i + 1))


class MRHTChan(metaclass=MACRTMeta):
    "MRHTChan class, fast measurement. High precision thermometer."
    properties = (('R', False), ('X', False),
                  ('status', False), ('I_set', True),
                  ('Ir', False), ('Ur', False),
                  ('Mode', True), ('ModeI', True),
                  ('range_I', True), ('range_U', True),
                  ('modul', True), ('power', False))

    def __init__(self, parent, chan_idx=0, idx_offset=0):
        self.ask = parent.ask
        self.get_cmd = parent.get_cmd
        self.set_cmd = parent.set_cmd
        self.idx_offset = idx_offset
        self.chan_idx = chan_idx
