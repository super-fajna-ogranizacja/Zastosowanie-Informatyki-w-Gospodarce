import asyncio
import os
import pathlib
from typing import Callable

import aiohttp
import chevron
from memoize.wrapper import memoize
import yaml

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


RenderFn = Callable[[str], str]


class MarkdownRenderer:
    API_URL = "https://api.github.com/markdown"
    API_TOKEN = os.environ["API_TOKEN"]
    API_CONTEXT = os.environ["OWNER_AND_REPO"]

    @staticmethod
    def _remove_p_tags(html: str) -> str:
        """Removes the <p> tags that Github adds when
        passing single words or even sentences.

        Parameters
        ----------
        html: str
            The HTML source to be stripped of the <p> tags

        Returns
        -------
        str
            HTML source without the <p> tags
        """

        return html[len('<p dir="auto">') : -len("</p>")]

    @memoize()
    async def __call__(self, md: str) -> str:
        """Wraps `MarkdownRenderer._inner_render` to memoize render
        calls to limit the API usage.

        Parameters
        ----------
        md: str
            The Markdown source to be rendered

        Returns
        -------
        str
            HTML source
        """

        return await self._inner_render(md)

    async def _inner_render(self, md: str) -> str:
        """Performs the actual rendering. If you want to extend
        functionality of this class, you may want to leave
        `__call__` method intact and override this one.

        Parameters
        ----------
        md: str
            The Markdown source to be rendered

        Returns
        -------
        str
            HTML source
        """

        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": "Bearer " + self.API_TOKEN,
        }

        json = {
            "text": md,
            "context": self.API_CONTEXT,
            "mode": "gfm",
        }

        async with aiohttp.request(
            "POST", url=self.API_URL, headers=headers, json=json
        ) as resp:
            return self._remove_p_tags(await resp.text())


async def render_app(render: RenderFn, app: dict) -> dict:
    """Renders given `app` using the `render` function.

    Parameters
    ----------
    render: RenderFn
        Renderer function, which will render smaller items
    app: dict
        Dictionary containing app's parameters

    Returns
    -------
    dict
        Dictionary containing app's parameters rendered
        into the HTML
    """

    html_app = {"original_name": app["name"]}

    for field, field_value in app.items():
        if isinstance(field_value, list):
            html_app[field] = []
            for item in field_value:
                html_app[field].append({"item": await render(item)})
        else:
            html_app[field] = await render(field_value)

    return html_app


async def main():
    output_dir = pathlib.Path("html")

    with open("apps.yml") as fd:
        apps = yaml.load(fd, Loader=Loader)

    render = MarkdownRenderer()

    # generate tasks for rendering the apps' params
    tasks = []
    for name, app_data in apps.items():
        tasks.append(render_app(render, app_data | {"name": name}))

    # render apps' parameters
    html_apps = await asyncio.gather(*tasks)

    # make sure the output directory exists
    if not output_dir.is_dir():
        output_dir.mkdir()

    # read the mustache template
    with open("project.html.mustache") as fd:
        template = fd.read()

    # render each app using the template
    for app in html_apps:
        name = app["original_name"]
        with open(output_dir / f"{name}.html", "w") as fd:
            fd.write(chevron.render(template, app))


if __name__ == "__main__":
    asyncio.run(main())
