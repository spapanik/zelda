from typing import Any

from grappelli.dashboard import Dashboard, modules


class AdminDashboard(Dashboard):  # type: ignore[misc]
    def init_with_context(self, context: list[dict[str, Any]]) -> None:  # noqa: ARG002
        self.children.append(
            modules.Group(
                "Group: Administration & Applications",
                column=1,
                collapsible=True,
                children=[
                    modules.ModelList(
                        "Authorisation",
                        column=1,
                        models=["django.contrib.auth.models.Group"],
                    ),
                    modules.ModelList(
                        "Users", column=1, models=["zelda.registration.models.User"]
                    ),
                ],
            )
        )

        self.children.append(
            modules.LinkList(
                "Useful links",
                column=2,
                children=[
                    {
                        "title": "Django Documentation",
                        "url": "https://docs.djangoproject.com/",
                        "external": True,
                    },
                    {
                        "title": "Grappelli Documentation",
                        "url": "https://django-grappelli.readthedocs.io/",
                        "external": True,
                    },
                ],
            )
        )

        self.children.append(
            modules.RecentActions(
                "Recent actions", limit=5, collapsible=False, column=3
            )
        )
