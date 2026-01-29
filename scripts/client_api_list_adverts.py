"""
List adverts owned by the authenticated account via GET /api/v1/adverts.
"""
from __future__ import annotations

from client_api_session import ClientApiSession, build_parser, config_from_args


def main() -> None:
    parser = build_parser("List adverts (GET /api/v1/adverts).")
    parser.add_argument("--page", type=int, default=1, help="Page number to fetch.")
    parser.add_argument("--page-size", type=int, default=20, help="Number of adverts per page.")
    args = parser.parse_args()

    api = ClientApiSession.from_config(config_from_args(args))
    payload = api.json("GET", "/adverts", params={"page": args.page, "page_size": args.page_size})
    if not payload:
        raise RuntimeError("Empty response received from /adverts.")

    meta = payload.get("meta", {})
    current_page = meta.get("current_page", args.page)
    page_count = meta.get("page_count", "?")
    print(f"Page {current_page} of {page_count}")
    adverts = payload.get("adverts", [])
    if not adverts:
        print("No adverts found for this account.")
        return

    for advert in adverts:
        status_payload = advert.get("status", {})
        status = "published" if status_payload.get("is_published") else "draft"
        processed = "processed" if status_payload.get("is_processed") else "queued"
        advert_id = advert.get("advert_id") or "unknown"
        title = advert.get("title") or "Untitled"
        print(f"- {advert_id} -> {title} ({status}, {processed})")


if __name__ == "__main__":
    main()
