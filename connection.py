import os

try:
    import requests
except ImportError:
    raise ImportError("Please install the required package: requests")


GRAPHQL_URL = "https://api.github.com/graphql"
OWNER, REPO_NAME = os.environ["OWNER_AND_REPO"].split("/")
API_TOKEN = os.environ["API_TOKEN"]

DISCUSSIONS_QUERY = """
query getDiscussions {
    repository(name: "$repo_name", owner: "$owner") {
        discussions(first: 100, categoryId: "$categoryId") {
            nodes {
                title
                body
                number
                author {
                    login
                }
            }
            totalCount
        }
    }
}
"""

CATEGORIES_QUERY = """
query getDiscussionCategories {
    repository(name: "$repo_name", owner: "$owner") {
        discussionCategories(first: 100) {
            nodes {
                id
                name
            }
        }
    }
}
"""


def apply_variables(query, variables):
    """Replaces the variables names in the query with their values

    Parameters
    ----------
    query : str
        The query to be sent to the server
    variables : dict
        The variables to be replaced in the query

    Returns
    -------
    str
        The query with the variables replaced
    """

    # Add the repo name and owner to the variables as they are used in every query
    variables["repo_name"] = REPO_NAME
    variables["owner"] = OWNER

    for name, value in variables.items():
        query = query.replace("$" + name, str(value))

    return query


def send_request(query, variables=None):
    """Sends given query with given parameters

    Parameters
    ----------
    query : str
        The query to be sent to the server
    variables : dict, optional
        The variables to be replaced in the query

    Returns
    -------
    requests.Response object
        Contains the server's response to the HTTP request.
    """

    if variables is None:
        variables = {}

    headers = {
        "Authorization": "Bearer " + API_TOKEN,
    }

    response = requests.post(
        url=GRAPHQL_URL,
        json={"query": apply_variables(query, variables)},
        headers=headers,
    )

    return response
