import json
import os

try:
    import requests
except ImportError:
    raise ImportError("Please install the required package: requests")


GRAPHQL_URL = "https://api.github.com/graphql"
OWNER, REPO_NAME = os.environ["OWNER_AND_REPO"].split("/")
API_TOKEN = os.environ["API_TOKEN"]
DISCUSSIONS_CATEGORY = os.environ["DISCUSSIONS_CATEGORY"]


DISCUSSIONS_QUERY = """
query getDiscussions {
    repository(name: "$repo_name", owner: "$owner") {
        discussions(first: 100, after:$after, categoryId: "$categoryId") {
            pageInfo {
                hasNextPage
                endCursor
            }
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
        discussionCategories(first: 100, after:$after) {
            pageInfo {
                hasNextPage
                endCursor
            }
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


def merge_responses(responses, query_type):
    """Merges the json responses from the server into one list

    Parameters
    ----------
    responses : list
        List of requests.Response objects
    query_type : str
        The type of the query

    Returns
    -------
    list
        List of the merged responses
    """
    # responses will be merged into the first response
    merged = json.loads(responses[0].text)["data"]["repository"][query_type]["nodes"]
    for response in responses[1:]:
        merged.extend(
            json.loads(response.text)["data"]["repository"][query_type]["nodes"]
        )

    return merged


def send_requests(query, variables=None):
    """Sends given query with given parameters
    Gets all of the requested data, not just the first 100

    Parameters
    ----------
    query : str
        The query to be sent to the server
    variables : dict, optional
        The variables to be replaced in the query

    Returns
    -------
    list
        List of dictionaries containing the data
    """

    responses = []
    has_next_page = True

    if variables is None:
        variables = {}
    # For the first request
    variables["after"] = "null"

    headers = {
        "Authorization": "Bearer " + API_TOKEN,
    }

    while has_next_page:
        response = requests.post(
            url=GRAPHQL_URL,
            json={"query": apply_variables(query, variables)},
            headers=headers,
        )
        data = json.loads(response.text)["data"]["repository"]
        query_type = list(data.keys())[0]
        page_info = json.loads(response.text)["data"]["repository"][query_type][
            "pageInfo"
        ]
        has_next_page = page_info["hasNextPage"]
        variables["after"] = '"' + page_info["endCursor"] + '"'
        responses.append(response)

    return merge_responses(responses, query_type)


def get_category_id():
    """Gets the id of the category with name discussions_category

    Returns
    -------
    str
        id of the category
    """

    response = send_requests(CATEGORIES_QUERY)

    for category in response:
        if category["name"] == DISCUSSIONS_CATEGORY:
            return category["id"]
    return None


def get_discussions():
    """Gets discussions from server's response

    Returns
    -------
    list
        List of discussions
    """

    categoryId = get_category_id()

    variables = {
        "categoryId": categoryId,
    }

    response = send_requests(DISCUSSIONS_QUERY, variables)

    return response
