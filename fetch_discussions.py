import application
import discussion

apps = discussion.parse_discussions()
application.print_apps(apps)
for app in apps:
    application.generate_yaml([app], filename=f"{app.name}.yml")
