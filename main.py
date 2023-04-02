import json
import re
import os

try:
    from yaml import dump, CDumper as Dumper
except ImportError:
    raise ImportError("Please install the required packages: requests, pyaml")

from app import App
import connection


COLUMNS = 105


def print_apps(apps):
    """Prints the details of all apps

    Parameters
    ----------
    apps : list
        List of App objects

    """

    print("\nPrinting parsed discussions:")

    for app in apps:
        print('-' * COLUMNS)
        app.print_app()

    print('*' * COLUMNS)


def parse_discussions(response):
    """Gets discussions from server's response and prints them

    Parameters
    ----------
    response : requests.Response object
        Contains the server's response to the HTTP request.

    Returns
    -------
    list
        List of App objects
    """

    # Regexes for parsing the entries in discussion body
    # multiline_re is needed to match even if there are new lines
    multiline_re = r"[\s\S]*"
    description_re = r"\*\*Description\*\*: (.*)" + multiline_re
    url_re = r"\*\*URLs\*\*: (.*)\n" + multiline_re
    types_re = r"\*\*Types\*\*: (.*)\n" + multiline_re
    platforms_re = r"\*\*Platforms\*\*: (.*)\n" + multiline_re
    # Additional lines are considered only in comments section
    comments_re = r"\s*---\s*" + r"(" + multiline_re + r")"

    body_regex = re.compile(description_re + url_re +
                            types_re + platforms_re + comments_re + r"$")

    apps = []
    for discussion in json.loads(response.text)["data"]["repository"]["discussions"]["nodes"]:
        app_name = discussion["title"]
        matched = body_regex.match(discussion["body"])
        try:
            description = matched.group(1)
            urls = matched.group(2)
            types = matched.group(3)
            platforms = matched.group(4)
            comments = matched.group(5)
        except (AttributeError):
            print(f'Error during body parsing for {app_name}')
            continue

        app = App(app_name, description, urls, types, platforms, comments)
        apps.append(app)
        print(f'Parsed discussion for {app_name} successfully')

    return apps


def generate_yaml(apps, filename):
    ''' Generates a YAML file from the apps list

    Parameters
    ----------
    apps : list
        List of App objects
    filename : str
        Name of the file to which YAML will be written

    Returns
    -------
    str
        YAML string
    '''

    apps_to_yaml = {}
    for app in apps:
        apps_to_yaml[app.name] = {
            "description": app.description,
            "urls": app.urls,
            "types": app.types,
            "platforms": app.platforms,
            "comments": app.comments
        }

    if filename:
        with open(filename, "w") as f:
            dump(data=apps_to_yaml, default_flow_style=False,
                 stream=f, sort_keys=False, Dumper=Dumper, indent=4)

    return dump(data=apps_to_yaml, default_flow_style=False,
                sort_keys=False, Dumper=Dumper, indent=4)


owner, repo_name = os.environ["OWNER_AND_REPO"].split("/")
api_token = os.environ["API_TOKEN"]
response = connection.get_discussions(owner, repo_name, api_token)

apps = parse_discussions(response)
print_apps(apps)
print("\nGenerated YAML:")
print(generate_yaml(apps, filename=None))
