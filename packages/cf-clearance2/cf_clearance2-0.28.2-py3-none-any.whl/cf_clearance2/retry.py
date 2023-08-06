# -*- coding: utf-8 -*-
from playwright.async_api import Error
from playwright.async_api import Page as AsyncPage
from playwright.sync_api import Page as SyncPage


async def async_cf_retry(page: AsyncPage, tries: int = 10, wait_for_url: str = None) -> bool:
    success = False
    while tries != 0:
        await page.wait_for_timeout(1500)
        try:
            if wait_for_url:
                await page.wait_for_url(wait_for_url)
            success = False if await page.query_selector("#challenge-form") else True
        except Error:
            success = False
        if success:
            break
        tries -= 1
    return success


def sync_cf_retry(page: SyncPage, tries: int = 10, wait_for_url: str = None) -> bool:
    success = False
    while tries != 0:
        page.wait_for_timeout(1500)
        try:
            if wait_for_url:
                page.wait_for_url(wait_for_url)
            success = False if page.query_selector("#challenge-form") else True
        except Error:
            success = False
        if success:
            break
        tries -= 1
    return success
