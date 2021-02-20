import asyncio
import sys

import asyncssh

_USERNAME = "scott"
_PASSWORD = "password"

_SSH_KEY = "server_host_key"


def client_handler(process: asyncssh.SSHClientProcess):
    username = process.get_extra_info("username")
    process.stdout.write(f"Welcome to my text adventure, {username}!\n")
    process.exit(0)


class SSHServer(asyncssh.SSHServer):
    def connection_made(self, conn: asyncssh.SSHClientConnection):
        peer = conn.get_extra_info("peername")[0]
        print(f"SSH connection received from {peer}.")

    def begin_auth(self, username: str) -> bool:
        "True if password is required for the username"
        return _PASSWORD != ""

    def password_auth_supported(self) -> bool:
        return True

    def validate_password(self, username: str, password: str) -> bool:
        "True if username/password combo correct or False if not"
        return username == _USERNAME and password == _PASSWORD


async def create_server():
    await asyncssh.create_server(
        SSHServer,
        host="127.0.0.1",
        port=2022,
        server_host_keys=[_SSH_KEY],
        process_factory=client_handler,
    )


if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(create_server())
    except (OSError, asyncssh.Error) as e:
        sys.exit(f"Error starting SSH server: {str(e)}")

    loop.run_forever()
