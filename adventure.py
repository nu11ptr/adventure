from typing import Optional
import asyncio
import sys

import asyncssh

from engine.game import load_game, Player


_SSH_KEY = "server_host_key"


class ClientHandler:
    def __init__(self, process: asyncssh.SSHClientProcess):
        self._username = process.get_extra_info("username")
        self._player: Optional[Player] = None
        self._process = process
        self._done = False

    async def _input(self):
        try:
            async for input_ in self._process.stdin:
                input_ = input_.rstrip("\n")
                await self._player.send_input(input_)
        except asyncssh.BreakReceived:
            pass

    async def _output(self):
        while True:
            output = await self._player.recv_output()
            self._process.stdout.write(output)
            self._process.stdout.write("\n")

    async def handle(self):
        self._player = await game.player(self._username)

        self._process.stdout.write(await game.greeting(self._username))

        _, pending = await asyncio.wait(
            [self._input(), self._output()], return_when=asyncio.FIRST_COMPLETED
        )

        for task in pending:
            task.cancel()

        self._process.stdout.write(await game.goodbye_msg(self._username))
        self._process.exit(0)


async def client_handler(process: asyncssh.SSHClientProcess):
    handler = ClientHandler(process)
    await handler.handle()


class SSHServer(asyncssh.SSHServer):
    def connection_made(self, conn: asyncssh.SSHClientConnection):
        peer = conn.get_extra_info("peername")[0]
        print(f"SSH connection received from {peer}.")

    def begin_auth(self, username: str) -> bool:
        "True if password is required for the username"
        return True

    def password_auth_supported(self) -> bool:
        return True

    async def validate_password(self, username: str, password: str) -> bool:
        "True if username/password combo correct or False if not"
        return await game.login(username, password)


async def create_server():
    await asyncssh.create_server(
        SSHServer,
        host="127.0.0.1",
        port=2022,
        server_host_keys=[_SSH_KEY],
        process_factory=client_handler,
    )


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python adventure.py <game_module>\n")
        sys.exit(1)

    game = load_game(sys.argv[1])

    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(create_server())
    except (OSError, asyncssh.Error) as e:
        sys.exit(f"Error starting SSH server: {str(e)}")

    loop.run_forever()
    loop.close()
