import uuid
from typing import Set, Type, Union, Callable

from PyQt6 import QtCore
from PyQt6.QtCore import QObject


_last_signal_id = 0


class _AnySignal:
    def __init__(self, *args, dest: Union['QSignalReceiver', None] = None, tag=None, **kwargs):
        global _last_signal_id
        _last_signal_id += _last_signal_id
        self.signal_id = _last_signal_id
        self.tag = tag
        _SignalsMgr.emit(self, dest)


class _QuerySignal(_AnySignal):
    def __init__(self, *, source: 'QSignalReceiver', callback: Callable[[_AnySignal], None] = None, **kwargs):
        self.source = source
        self.callback = callback
        super().__init__(**kwargs)


class _ResponseSignal(_AnySignal):
    def __init__(self, *, query_signal: _QuerySignal, **kwargs):
        self.query_signal = query_signal
        super().__init__(dest=query_signal.source, **kwargs)


class QSignal:
    """

    """
    Any = _AnySignal
    Query = _QuerySignal
    Response = _ResponseSignal


class QSignalReceiver:
    signal_in = QtCore.pyqtSignal(_AnySignal)

    def __init__(self, *, signaltypes: Set[Type[_AnySignal]], **kwargs):
        assert isinstance(self, QObject)
        super().__init__(**kwargs)
        _SignalsMgr.add_receiver(self, signaltypes)
        self.signal_in.connect(self._signal_received)
        self.destroyed.connect(_SignalsMgr.remove_receiver)

    def _signal_received(self, signal: _AnySignal) -> bool:
        if isinstance(signal, _ResponseSignal) and signal.query_signal.callback:
            signal.query_signal.callback(signal)
            return True  # Signal processed
        return False  # Signal not processed


class _SignalsMgr:
    receivers = {}

    @classmethod
    def add_receiver(cls, receiver: QObject, signaltypes: Set[Type[_AnySignal]]):
        assert False not in {issubclass(sigtype, _AnySignal) for sigtype in signaltypes}
        sig_receiver_uuid = uuid.uuid4()
        receiver.setProperty('sig_receiver_uuid', sig_receiver_uuid)
        cls.receivers[sig_receiver_uuid] = {'receiver': receiver, 'signaltypes': signaltypes}

    @classmethod
    def remove_receiver(cls, receiver: QObject):
        sig_receiver_uuid = receiver.property('sig_receiver_uuid')
        if sig_receiver_uuid in cls.receivers.keys():
            del cls.receivers[sig_receiver_uuid]

    @classmethod
    def emit(cls, signal: _AnySignal, dest: Union['QSignalReceiver', None]):
        if isinstance(dest, QObject):
            sig_receiver_uuid = dest.property('sig_receiver_uuid')
            if sig_receiver_uuid in _SignalsMgr.receivers.keys():
                dest.signal_in.emit(signal)
        else:
            for sig_receiver_uuid in cls.receivers:
                signaltypes = cls.receivers[sig_receiver_uuid]['signaltypes']
                for signaltype in signaltypes:
                    if isinstance(signal, signaltype):
                        receiver = cls.receivers[sig_receiver_uuid]['receiver']
                        receiver.signal_in.emit(signal)
                        break
