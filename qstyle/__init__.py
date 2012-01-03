from xcb import xcb
from xcb import xproto
from xcb import render
from xcb import composite
from xcb import damage
from xcb import xfixes
import logging

log = logging.getLogger('qstyle')
atoms = [
    '_NET_WM_WINDOW_OPACITY',
    '_XROOTPMAP_ID',
    '_XSETROOT_I']


class QStyle(object):

    def __init__(self):
        log.debug('Initializing')
        self.connection = xcb.connect()
        self.render = self.connection(render.key)
        self.composite = self.connection(composite.key)
        self.damage = self.connection(damage.key)
        self.xfixes = self.connection(xfixes.key)
        self.core = self.connection.core

        self.setup = self.connection.get_setup()
        self.screen = self.setup.roots[0]
        self.xproto_ex = xproto.xprotoExtension(self.connection)
        self._atoms_init()
        self._sync()

        self.xproto_ex.GrabServer()

        log.debug('Done')

    def _atoms_init(self):
        self.atoms = {}
        for atom in atoms:
            self.atoms[atom] = self.core.InternAtom(
                False, len(atom), atom).reply().atom

    def _sync(self):
        self.core.GetInputFocus().reply()

    def __del__(self):
        log.debug('Destructing')
        self.connection.disconnect()
        log.debug('Done')
