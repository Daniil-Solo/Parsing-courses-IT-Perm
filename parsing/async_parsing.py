import aiohttp
import asyncio

from classes import Program
from parsing.data_extraction import get_link_for_programs, get_program_info
from parsing.constants import ALL_PROGRAM_LINK


async def get_document(link: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(link) as resp:
            return await resp.text()


async def collect_program_documents():
    home_document = await get_document(ALL_PROGRAM_LINK)
    links = get_link_for_programs(home_document)
    tasks = []
    for link in links:
        tasks.append(asyncio.create_task(get_document(link)))
    documents = await asyncio.gather(*tasks)
    return documents


async def async_get_programs() -> list[Program]:
    documents = await collect_program_documents()
    return [get_program_info(d) for d in documents]


def get_programs() -> list[Program]:
    return asyncio.run(async_get_programs())
