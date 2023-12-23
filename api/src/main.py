import asyncio
import re
from random import random

import requests
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache
from loguru import logger
from src.config import get_settings
from src.constants import GH_REPOSITORIES, USER_DATA

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
FastAPICache.init(InMemoryBackend())


@app.get("/{username}")
async def user_data(username: str):
    if get_settings().ENVIRONMENT == "DEV":
        logger.debug("DEV MODE")
        await asyncio.sleep(random() * 5)
        return USER_DATA
    return requests.get(
        f"https://api.github.com/users/{username}",
        headers={
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    ).json()


@app.get("/{username}/repos/{amount}")
async def repository_data(username: str, amount: int):
    return (await get_paginated_repository_data(username))[:amount]


@app.get("/{username}/repos/plot/{information}")
async def repository_plot_data(username: str, information: str):
    gh_repositories = await get_paginated_repository_data(username)
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


@cache(expire=60 * 60 * 24)
async def get_paginated_repository_data(username: str):
    def parse_data(data):
        if data is None:
            return []
        return data

    if get_settings().ENVIRONMENT == "DEV":
        logger.debug("DEV MODE")
        await asyncio.sleep(random() * 5)
        return GH_REPOSITORIES

    url = f"https://api.github.com/users/{username}/repos?sort=updated"
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
        logger.debug(f"GitHub response: {response}")
        # response.raise_for_status()
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
