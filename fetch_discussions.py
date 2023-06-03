import application
import connection
import discussion

response = connection.get_discussions()
apps = discussion.parse_discussions(response)
application.print_apps(apps)
for app in apps:
    application.generate_yaml([app], filename=f"{app.name}.yml")
