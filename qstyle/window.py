import struct
from . import xproto, log


class Window(object):

    def __init__(self, qstyle, wid):
        self.id = wid
        self.cookies = {
            'attributes': qstyle.core.GetWindowAttributes(self.id),
            'geometry': qstyle.core.GetGeometry(self.id),
            '_opacity': qstyle.core.GetProperty(
                False,
                self.id,
                qstyle.atoms['_NET_WM_WINDOW_OPACITY'],
                xproto.Atom.CARDINAL,
                0,
                1
            )
        }
        for name, cookie in self.cookies.items():
            try:
                setattr(self, name, cookie.reply())
            except Exception:
                log.exception(
                    "Error on getting %s of window %d" % (name, self.id))
                setattr(self, name, None)

    @property
    def opacity(self):
        val_len = len(self._opacity.value)
        if val_len:
            unpacked = struct.unpack(
                'I' * (len(self._opacity.value) / 4),
                self._opacity.value.buf())
            if unpacked:
                try:
                    return int((float(unpacked[0]) / float(0xffff)) * 0xffff)
                except Exception:
                    log.exception("Error getting opacity")
        return int(0xffff)

    def __repr__(self):
        return "Window(%d) Attributes%r Geometry%r Opacity%r" % (
            self.id,
            self.attributes,
            self.geometry,
            self.opacity)
