try:
    from yaml import CDumper as Dumper
    from yaml import dump
except ImportError:
    raise ImportError("Please install the required package: pyaml")


class App:
    def __init__(self, name, description, urls, types, platforms, categories, comments):
        self.name = name
        self.description = description
        self.urls = urls.split()
        self.types = types
        self.platforms = platforms
        self.categories = categories
        self.comments = comments

    def __str__(self):
        return "\n".join(
            [
                f"App_name: {self.name}",
                f"Description: {self.description}",
                f"Urls: {self.urls}",
                f"Types: {self.types}",
                f"Platforms: {self.platforms}",
                f"Categories: {self.categories}",
                f"Comments: {self.comments}",
            ]
        )


def print_apps(apps):
    """Prints the details of all apps

    Parameters
    ----------
    apps : list
        List of App objects

    """

    columns = 105

    print("\nPrinting parsed discussions:")
    for app in apps:
        print("-" * columns)
        print(app)

    print("*" * columns)


def generate_yaml(apps, filename):
    """Generates a YAML file from the apps list

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
    """

    apps_to_yaml = {}
    for app in apps:
        apps_to_yaml[app.name] = {
            "description": app.description.replace("\r", ""),
            "urls": app.urls,
            "types": app.types,
            "platforms": app.platforms,
            "categories": app.categories,
            "comments": app.comments.replace("\r", ""),
        }

    if filename:
        with open(filename, "w") as f:
            dump(
                data=apps_to_yaml,
                default_flow_style=False,
                stream=f,
                sort_keys=False,
                Dumper=Dumper,
                indent=2,
            )

    y = dump(
        data=apps_to_yaml,
        default_flow_style=False,
        sort_keys=False,
        Dumper=Dumper,
        indent=2,
    )

    print("\nGenerated YAML:")
    print(y)
    return y
