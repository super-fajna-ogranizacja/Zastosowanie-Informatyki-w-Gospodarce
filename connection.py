import requests


GRAPHQL_URL = "https://api.github.com/graphql"


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


def get_discussions(owner, repo_name, api_token):
    """Gets the discussions from the GitHub repository

    Returns
    -------
    requests.Response object
        Contains the server's response to the HTTP request.
    """

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
    headers = {
        "Authorization": "Bearer " + api_token,
    }

    response = requests.post(
        url=GRAPHQL_URL,
        json={"query": apply_variables(query, variables)},
        headers=headers,
    )

    return response
