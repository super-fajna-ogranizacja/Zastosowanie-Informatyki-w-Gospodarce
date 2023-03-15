import json
import os
import requests


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
    for name, value in variables.items():
        query = query.replace("$"+name, str(value))

    return query

api_token = os.environ["API_TOKEN"]
headers = {
    "Authorization": "Bearer " + api_token,
}

r = requests.post(
    url=url,
    json={"query": apply_variables(query, variables)},
    headers=headers,
)
print(json.dumps(json.loads(r.text), indent=4))
