from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from django.urls import NoReverseMatch, reverse

from .navigation import NAVIGATION


def navigation(request):
    user = getattr(request, "user", None)
    nav_top_links = []
    nav_side_links = []
    nav_active_section = None

    if not user or not user.is_authenticated:
        return {
            "nav_top_links": nav_top_links,
            "nav_side_links": nav_side_links,
            "nav_active_section": nav_active_section,
        }

    role = getattr(user, "role", None)
    role_config = NAVIGATION.get(role)
    if not role_config:
        return {
            "nav_top_links": nav_top_links,
            "nav_side_links": nav_side_links,
            "nav_active_section": nav_active_section,
        }

    top_entries = role_config.get("top", [])
    requested_section = request.GET.get("section")
    available_keys = [entry.get("key") for entry in top_entries if entry.get("key")]
    if requested_section in available_keys:
        nav_active_section = requested_section

    def append_params(url, params):
        if not params:
            return url
        split = urlsplit(url)
        query = dict(parse_qsl(split.query))
        query.update({k: v for k, v in params.items() if v is not None})
        new_query = urlencode(query, doseq=True)
        return urlunsplit((split.scheme, split.netloc, split.path, new_query, split.fragment))

    def build_section_url(entry_key, explicit_url=None, url_name=None, params=None):
        if explicit_url:
            return append_params(explicit_url, params)
        if url_name:
            try:
                resolved = reverse(url_name)
            except NoReverseMatch:
                return "#"
            return append_params(resolved, params)
        base_url = request.path
        query = request.GET.copy()
        query["section"] = entry_key
        return append_params(base_url, query)

    for entry in top_entries:
        entry_key = entry.get("key")
        if not entry_key:
            continue
        nav_top_links.append(
            {
                "key": entry_key,
                "label": entry.get("label", entry_key.title()),
                "url": build_section_url(
                    entry_key,
                    entry.get("url"),
                    entry.get("url_name"),
                    entry.get("params"),
                ),
                "active": entry_key == nav_active_section,
            }
        )

    side_config = role_config.get("side", {})
    side_entries = side_config.get(nav_active_section, []) if nav_active_section else []

    def resolve_side_url(entry):
        url = entry.get("url")
        url_name = entry.get("url_name")
        target_section = entry.get("section", nav_active_section)
        params = dict(entry.get("params") or {})
        if target_section:
            params.setdefault("section", target_section)
        if url_name:
            try:
                base = reverse(url_name)
            except NoReverseMatch:
                return "#"
            return append_params(base, params)
        if url:
            return append_params(url, params)
        return "#"

    current_view_name = ""
    resolver_match = getattr(request, "resolver_match", None)
    if resolver_match:
        current_view_name = resolver_match.view_name or ""

    effective_scope = request.GET.get("scope")
    if not effective_scope:
        user_role = getattr(user, "role", None)
        effective_scope = "mine" if user_role == "client" else "all"

    for entry in side_entries:
        entry_url = resolve_side_url(entry)
        entry_active = entry.get("active", False)
        url_name = entry.get("url_name")
        entry_params = entry.get("params") or {}
        if not entry_active and url_name and current_view_name == url_name:
            target_scope = entry_params.get("scope")
            if target_scope is None or str(target_scope) == str(effective_scope):
                entry_active = True
        nav_side_links.append(
            {
                "key": entry.get("key"),
                "label": entry.get("label", entry.get("key", "")),
                "url": entry_url,
                "active": entry_active,
                "disabled": entry.get("disabled", False),
            }
        )

    return {
        "nav_top_links": nav_top_links,
        "nav_side_links": nav_side_links,
        "nav_active_section": nav_active_section,
    }
