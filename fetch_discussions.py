import application
import discussion

apps = discussion.parse_discussions()
application.print_apps(apps)
application.generate_yaml(apps, filename="apps.yml")
