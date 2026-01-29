"""
Publish multiple adverts in one request via POST /api/v1/adverts/bulk-publish.
"""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List

from client_api_session import ClientApiSession, build_parser, config_from_args
from tutorial_utils import read_ids


def print_errors(errors: List[Dict[str, object]]) -> None:
    if not errors:
        return
    print("Errors encountered:")
    for error in errors:
        reference = error.get("reference") or error.get("advert_id") or "unknown"
        print(f"- {reference}: {error.get('detail')}")


def main() -> None:
    parser = build_parser("Bulk publish adverts (POST /api/v1/adverts/bulk-publish).")
    parser.add_argument(
        "--advert-ids",
        default=None,
        help="Comma-separated advert IDs to publish.",
    )
    parser.add_argument(
        "--ids-file",
        type=Path,
        default=None,
        help="JSON array of advert IDs or {\"advert_ids\": [...]}.",
    )
    args = parser.parse_args()

    advert_ids = read_ids(args.advert_ids, args.ids_file)
    if not advert_ids:
        parser.error("Provide at least one advert ID via --advert-ids or --ids-file.")

    api = ClientApiSession.from_config(config_from_args(args))
    response = api.json("POST", "/adverts/bulk-publish", json={"advert_ids": advert_ids})
    adverts = response.get("adverts", []) if response else []
    print(f"Published {len(adverts)} advert(s) in bulk.")
    print_errors(response.get("errors", []))


if __name__ == "__main__":
    main()
