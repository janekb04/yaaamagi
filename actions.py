import asyncio
import contextlib
import os
import iterm2
import iterm2.auth


async def _run(coro, conn=None):
    with open(os.devnull, "w") as devnull:
        with contextlib.redirect_stdout(devnull):
            with contextlib.redirect_stderr(devnull):
                if conn is None:
                    conn = await iterm2.Connection().async_create()
                    asyncio.ensure_future(
                        conn._async_dispatch_forever(conn, asyncio.get_running_loop())
                    )

                async def _coro(connection):
                    asyncio.sleep(0.02)
                    return await coro(await iterm2.async_get_app(connection))

                return await _coro(conn)


async def get_terminal_content():
    async def _coro(app):
        window = app.current_window
        if window is None:
            raise RuntimeError("No iTerm2 window")
        screen: iterm2.ScreenContents = (
            await window.current_tab.current_session.async_get_screen_contents()
        )
        cols = 90
        screen_text = "+" + "-" * cols + "+\n"
        lines = screen.number_of_lines

        while lines > 0 and screen.line(lines - 1).string == "":
            lines -= 1

        for i in range(lines):
            screen_text += f"|{screen.line(i).string.ljust(cols)}|\n"
        screen_text += "+" + "-" * cols + "+\n"
        return screen_text

    return await _run(_coro)


async def terminal_type(text: str):
    async def _coro(app):
        window = app.current_window
        if window is None:
            raise RuntimeError("No iTerm2 window")
        await window.current_tab.current_session.async_send_text(text)

    await _run(_coro)


async def terminal_return():
    async def _coro(app):
        window = app.current_window
        if window is None:
            raise RuntimeError("No iTerm2 window")
        await window.current_tab.current_session.async_send_text("\n")

    await _run(_coro)
