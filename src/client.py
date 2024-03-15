import requests
import os
from dotenv import load_dotenv
from pathlib import Path


class HeuristAPI:
    SERVER = "https://heurist.huma-num.fr/heurist/"
    API = "hserv/controller/record_output.php"

    def __init__(self, session_id: str | None = None, db_name: str | None = None):
        load_dotenv()
        if not session_id:
            session_id = os.getenv("SESSION_ID")
        self.session_id = session_id
        if not db_name:
            db_name = os.getenv("DB_NAME")
        self.db_name = db_name

    def call(self, url: str):
        return requests.get(url, cookies={"heurist-sessionid": self.session_id})

    def gexf(self, outfile: Path, query_str: str = "{t%%3A101%%2C102%%2C103}}"):
        url = (
            self.SERVER
            + self.API
            + "?q="
            + query_str
            + "db={}".format(self.db_name)
            + "&depth=all&linkmode=direct&format=gephi&defs=0&extended=2"
        )
        r = self.call(url)
        with open(outfile, "wb") as f:
            f.write(r.content)


if __name__ == "__main__":
    client = HeuristAPI()
    fp = Path(__file__).parent.parent.joinpath("img").joinpath("graph.gexf")
    client.gexf(fp)
