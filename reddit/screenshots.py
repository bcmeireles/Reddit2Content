from pathlib import Path

from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright, ViewportSize

import json

def downloadScreenshots(r_obj, num, storymode=False):
    print("Downloading screenshots...")

    Path("temp/screenshots").mkdir(parents=True, exist_ok=True)

    with sync_playwright() as sp:
        browser = sp.chromium.launch()
        context = browser.new_context()

        cookies = json.load(open("./cookies/dark.json", encoding="utf-8"))
        context.add_cookies(cookies)

        page = context.new_page()
        page.goto(f'https://reddit.com{r_obj["link"]}', timeout=0)

        if page.locator('[data-testid="content-gate"]').is_visible(): # NSFW Post
            page.locator('[data-testid="content-gate"] button').click()
            page.locator(
                '[data-click-id="text"] button'
            ).click()

        page.locator('[data-test-id="post-content"]').screenshot(path="temp/screenshots/title.png")

        if storymode:
            page.locator('[data-click-id="text"]').screenshot(
                path="assets/temp/png/story_content.png"
            )

        else:
            for idx, comment in enumerate(r_obj["replies"]):
                if idx >= num:
                    break

                if page.locator('[data-testid="content-gate"]').is_visible():
                    page.locator('[data-testid="content-gate"] button').click()

                page.goto(f'https://reddit.com{comment["link"]}', timeout=0)


                page.locator(f"#t1_{comment['id']}").screenshot(
                    path=f"temp/screenshots/comment_{idx}.png"
                )

        print("Screenshots downloaded Successfully.")