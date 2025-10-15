NAVIGATION = {
    "admin": {
        "top": [
            {"key": "worksites", "label": "Budowy"},
            {"key": "orders", "label": "Zlecenia"},
            {"key": "users", "label": "Uzytkownicy"},
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
            {"key": "worksites", "label": "Budowy"},
            {"key": "orders", "label": "Zlecenia"},
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
