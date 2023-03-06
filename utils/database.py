from External_functions import get_async, post_async

import os

class Database:
    def __init__(self, folder: str):
        self.url = os.getenv("dburl")
        self.token = os.getenv("database")
        self.folder = folder

    async def fetch(self, id = "") -> dict:
        return await get_async(
            "{}/get/{}/{}".format(self.url, self.folder, id), 
            headers={"authorization": self.token},
            kind="json"
        )
    
    async def create(self) -> dict:
        return await post_async(
            "{}/create/{}".format(self.url, self.folder), 
            headers={"authorization": self.token},
            kind="json"
        )
    
    async def update(self, **data) -> dict:
        return await post_async(
            self.url + self.folder, 
            headers={"authorization": self.token},
            data=data,
            kind="json"
        )
    
    async def setFolder(self, folder: str) -> None:
        self.folder = folder
    

    
