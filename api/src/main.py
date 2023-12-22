import asyncio
import re
from random import random

import requests
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from src.config import get_settings
from src.constants import GH_REPOSITORIES

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/{username}/{information}")
async def data(username: str, information: str):
    await asyncio.sleep(random() * 5)
    gh_repositories = get_paginated_data(username)
    return calc_repo_info_for_plotly(gh_repositories, information)


def calc_repo_info_for_plotly(gh_repositories, information: str):
    return [
        {
            "values": [
                count := len(
                    list(
                        filter(
                            lambda repo: repo.get(information, False), gh_repositories
                        )
                    )
                ),
                len(gh_repositories) - count,
            ],
            "labels": [information.capitalize().replace("_", " "), "Otherwise"],
            "type": "pie",
            "hole": ".4",
            "marker": {"colors": ["rgb(255, 127, 14)", "rgb(31, 119, 180)"]},
        }
    ]


def get_paginated_data(username: str):
    def parse_data(data):
        if data is None:
            return []
        return data

    if get_settings().ENVIRONMENT == "DEV":
        logger.debug("DEV MODE")
        return GH_REPOSITORIES

    url = f"https://api.github.com/users/{username}/repos"
    next_pattern = re.compile(r'<([^>]+)>; rel="next"')
    pages_remaining = True
    data = []

    while pages_remaining:
        response = requests.get(
            url,
            params={"per_page": 25},
            headers={
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
            },
        )
        logger.debug(get_settings().PRIVATE_KEY_PATH)
        logger.debug(response)
        logger.debug(response.json())
        response.raise_for_status()
        data.extend(parse_data(response.json()))

        link_header = response.headers.get("link", "")

        pages_remaining = 'rel="next"' in link_header

        if pages_remaining:
            logger.debug(link_header)
            url = next_pattern.search(link_header).group(1)
    return data


if __name__ == "__main__":
    uvicorn.run(
        "src.main:app", host=get_settings().HOST, port=get_settings().PORT, reload=True
    )