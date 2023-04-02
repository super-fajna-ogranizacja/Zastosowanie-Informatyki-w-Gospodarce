class App:
    def __init__(self, name, description, urls, types, platforms, comments):
        self.name = name
        self.description = description
        self.urls = urls.split()
        self.types = types.split()
        self.platforms = platforms.split()
        self.comments = comments

    def print_app(self):
        """Prints the details of an app"""

        print(f'App_name: {self.name}',
              f'Description: {self.description}',
              f'Urls: {self.urls}',
              f'Types: {self.types}',
              f'Platforms: {self.platforms}',
              f'Comments: {self.comments}',
              sep='\n'
              )
