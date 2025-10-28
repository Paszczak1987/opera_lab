NAVIGATION = {
    "admin": {
        "top": [
            {
                "key": "worksites",
                "label": "Budowy",
                "url_name": "users:admin_dashboard",
                "params": {"section": "worksites"},
            },
            {
                "key": "orders",
                "label": "Zlecenia",
                "url_name": "users:admin_dashboard",
                "params": {"section": "orders"},
            },
            {
                "key": "users",
                "label": "Uzytkownicy",
                "url_name": "users:admin_dashboard",
                "params": {"section": "users"},
            },
        ],
        "side": {
            "worksites": [
                {
                    "key": "worksites_all",
                    "label": "Lista budow",
                    "url_name": "worksites:list",
                    "section": "worksites",
                    "params": {"scope": "all"},
                },
                {
                    "key": "worksites_manage",
                    "label": "Dodaj / Edytuj",
                    "url_name": "worksites:create",
                    "section": "worksites",
                },
            ],
            "orders": [
                {"key": "orders_placeholder", "label": "Zlecenia", "url": "#", "disabled": True},
            ],
            "users": [
                {"key": "users_all", "label": "Lista uzytkownikow", "url": "#", "disabled": True},
            ],
        },
    },
    "client": {
        "top": [
            {
                "key": "worksites",
                "label": "Budowy",
                "url_name": "users:client_dashboard",
                "params": {"section": "worksites"},
            },
            {
                "key": "orders",
                "label": "Zlecenia",
                "url_name": "users:client_dashboard",
                "params": {"section": "orders"},
            },
        ],
        "side": {
            "worksites": [
                {
                    "key": "worksites_all",
                    "label": "Lista budów",
                    "url_name": "worksites:list",
                    "section": "worksites",
                    "params": {"scope": "all"},
                },
                {
                    "key": "worksites_mine",
                    "label": "Moje budowy",
                    "url_name": "worksites:list",
                    "section": "worksites",
                    "params": {"scope": "mine"},
                },
                {
                    "key": "worksites_manage",
                    "label": "Dodaj / Edytuj",
                    "url_name": "worksites:create",
                    "section": "worksites",
                },
            ],
            "orders": [
                {"key": "orders_placeholder", "label": "Zlecenia (w przygotowaniu)", "url": "#", "disabled": True},
            ],
        },
    },
}
