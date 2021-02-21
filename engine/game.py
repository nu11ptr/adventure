import asyncio


class Player:
    def __init__(self, username: str):
        self.username = username
        self.input = "Are we there yet?"

    async def send_input(self, text: str):
        self.input = text

    async def recv_output(self) -> str:
        await asyncio.sleep(3.0)
        return self.input


class Game:
    async def greeting(self, username: str) -> str:
        return "Greetings!"

    async def goodbye_msg(self, username: str) -> str:
        return "Goodbye!"

    async def login(self, username: str, password: str) -> bool:
        return True

    async def player(self, username: str):
        return Player(username)


def load_game(class_path: str) -> Game:
    import importlib

    mod, clz = class_path.rsplit(".", 1)
    game_mod = importlib.import_module(mod)
    game_type = getattr(game_mod, clz)
    return game_type()
