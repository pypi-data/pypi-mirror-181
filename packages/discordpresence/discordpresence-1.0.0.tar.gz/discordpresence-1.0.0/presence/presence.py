import asyncio
from pypresence import AioPresence
from time import time
from typing import List


class Button:
    def __init__(self, label: str, url: str) -> None:
        self.__label = label
        self.__url = url

    def to_dict(self) -> dict:
        return {
            "url": self.__url,
            "label": self.__label
        }

class DiscordPresence:
    def __init__(self, client_id: str) -> None:
        self.__client_id = client_id
        self.__presence = AioPresence(self.__client_id)
        self.__loop = asyncio.get_event_loop()

    def connect(self) -> None:
        self.__loop.run_until_complete(self.__presence.connect())

    def close(self) -> None:
        self.__presence.close()

    def update(
        self,
        state: str=None,
        details: str=None,
        start: int=round(time()),
        end: int=None,
        large_image: str=None,
        large_text: str=None,
        small_image: str=None,
        small_text: str=None,
        buttons: List[Button]=[]
    ) -> None:
        buttons = [button.to_dict() for button in buttons] if len(buttons) != 0 else None
        self.__loop.run_until_complete(self.__presence.update(
            state=state, 
            details=details, 
            start=start, 
            end=end, 
            large_image=large_image, 
            large_text=large_text, 
            small_image=small_image, 
            small_text=small_text, 
            buttons=buttons
        ))