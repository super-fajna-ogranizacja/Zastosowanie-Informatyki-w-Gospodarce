import json
import os
import re

try:
    import requests
except ImportError:
    raise ImportError("Please install the required packages: requests")


COLUMNS = 105
owner, repo_name = os.environ["OWNER_AND_REPO"].split("/")

url = "https://api.github.com/graphql"
query = """
query getDiscussions {
    repository(name: "$repo_name", owner: "$owner") {
        discussions(first: 100) {
            nodes {
                title
                body
                author {
                    login
                }
            }
            totalCount
        }
    }
}
"""

variables = {
    "repo_name": repo_name,
    "owner": owner,
}


def apply_variables(query, variables):
    """Replaces the variables names in the query with their values

    Parameters
    ----------
    query : str
        The query to be sent to the server
    variables : dict
        The variables to be replaced in the query

    """

    for name, value in variables.items():
        query = query.replace("$"+name, str(value))

    return query


def parse_discussions(response):
    """Gets discussions from server's response and prints them

    Parameters
    ----------
    response : requests.Response object
        Contains the server's response to the HTTP request.

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

    print("Printing fetched and parsed discussions:")
    for discussion in json.loads(response.text)["data"]["repository"]["discussions"]["nodes"]:
        app_name = discussion["title"]
        matched = body_regex.match(discussion["body"])
        printAppDetails(app_name, matched)

    print('*' * COLUMNS)


def printAppDetails(app_name, matched):
    """Prints the details of an app

    Parameters
    ----------
    app_name : str
        Name of the app
    matched : re.Match object
        Contains the matched groups of the regex
    """

    print('-' * COLUMNS)

    try:
        description = matched.group(1)
        urls = matched.group(2)
        types = matched.group(3)
        platforms = matched.group(4)
        comments = matched.group(5)
    except (AttributeError):
        print(f'Error during body parsing for {app_name}')
        return

    print(f'App_name: {app_name}',
          f'Description: {description}',
          f'Urls: {urls}',
          f'Types: {types}',
          f'Platforms: {platforms}',
          f'Comments: {comments}',
          sep='\n'
          )


api_token = os.environ["API_TOKEN"]
headers = {
    "Authorization": "Bearer " + api_token,
}

response = requests.post(
    url=url,
    json={"query": apply_variables(query, variables)},
    headers=headers,
)

parse_discussions(response)
