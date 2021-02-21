from engine.game import Game


class MyGame(Game):
    async def greeting(self, username: str) -> str:
        return f"Welcome to the adventure, {username}\n"

    async def goodbye_msg(self, username: str) -> str:
        return "Thanks for play my game!\n"
