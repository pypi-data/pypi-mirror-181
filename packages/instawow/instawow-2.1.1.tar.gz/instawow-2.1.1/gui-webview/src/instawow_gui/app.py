from __future__ import annotations

import json
import os
from functools import partial
from typing import Any

import toga
import toga.constants
import toga.style
from loguru import logger

from . import json_rpc_server


class InstawowApp(toga.App):
    def __init__(self, **kwargs: object) -> None:
        super().__init__(
            formal_name='instawow-gui',
            app_id='org.instawow.instawow_gui',
            app_name='instawow_gui',
            icon='resources/instawow_gui',
            **kwargs,
        )

    def startup(self) -> None:
        self.main_window = toga.MainWindow(title=self.formal_name, size=(800, 600))

        if os.name == 'nt':
            import ctypes

            # Enable high DPI support.
            ctypes.windll.user32.SetProcessDPIAware()

        self.main_window.content = web_view = toga.WebView(style=toga.style.Pack(flex=1))

        if os.name == 'nt':
            from toga_winforms.widgets.webview import TogaWebBrowser

            def configure_webview2(sender: TogaWebBrowser, event_args: Any):
                if event_args.IsSuccess:
                    sender.CoreWebView2.Settings.AreBrowserAcceleratorKeysEnabled = False

            web_view._impl.native.CoreWebView2InitializationCompleted += configure_webview2

        def dispatch_js_keyboard_event(_: toga.Command, *, action: str):
            event_args = json.dumps(
                {'detail': {'action': action}, 'bubbles': True, 'cancelable': True}
            )
            web_view.invoke_javascript(
                f'document.dispatchEvent(new CustomEvent("togaSimulateKeypress", {event_args}));'
            )

        self.commands.add(
            toga.Command(
                partial(dispatch_js_keyboard_event, action='toggleSearchFilter'),
                label='Toggle Search Filter',
                shortcut=toga.Key.MOD_1 + toga.Key.G,
                group=toga.Group.EDIT,
                section=20,
                order=10,
            ),
            toga.Command(
                partial(dispatch_js_keyboard_event, action='activateViewInstalled'),
                label='Installed',
                shortcut=toga.Key.MOD_1 + toga.Key.L,
                group=toga.Group.WINDOW,
                section=20,
                order=10,
            ),
            toga.Command(
                partial(dispatch_js_keyboard_event, action='activateViewReconcile'),
                label='Unreconciled',
                group=toga.Group.WINDOW,
                section=20,
                order=20,
            ),
            toga.Command(
                partial(dispatch_js_keyboard_event, action='activateViewSearch'),
                label='Search',
                shortcut=toga.Key.MOD_1 + toga.Key.F,
                group=toga.Group.WINDOW,
                section=20,
                order=30,
            ),
        )

        async def startup() -> None:
            web_app = await json_rpc_server.create_app(self.main_window)
            server_url, serve = await json_rpc_server.run_app(web_app)
            logger.debug(f'JSON-RPC server running on {server_url}')
            web_view.url = str(server_url)
            await serve()

        serve_task = self._impl.loop.create_task(startup())
        self.on_exit = lambda _: serve_task.cancel()

        self.main_window.show()
