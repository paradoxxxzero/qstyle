from xcb import xcb
from xcb import xproto
from xcb import render
from xcb import composite
from xcb import damage
from xcb import xfixes
import logging
log = logging.getLogger('qstyle')
from .window import Window

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

        # Getting all windows
        qt_cookie = self.core.QueryTree(self.screen.root)

        # Redirect all windows
        self.composite.RedirectSubwindows(
            self.screen.root,
            composite.Redirect.Manual
        )

        # Subscribe to X events
        self.core.ChangeWindowAttributes(
            self.screen.root,
            xproto.CW.EventMask,
            [
                xproto.EventMask.KeyPress |
                xproto.EventMask.KeyRelease |
                xproto.EventMask.ButtonRelease |
                xproto.EventMask.SubstructureNotify |
                xproto.EventMask.StructureNotify |
                xproto.EventMask.PropertyChange
            ])

        self._sync()
        wids = qt_cookie.reply().children
        self.windows = [Window(self, wid) for wid in wids]

        self.xproto_ex.UngrabServer()

        for window in self.windows:
            log.info(window)

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
