"""
Update multiple adverts in one request via PUT /api/v1/adverts/bulk-update.

Provide --updates-file to send your own JSON array of update objects.
If omitted, pass advert IDs and a sample payload is generated for each.
"""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List

from client_api_session import ClientApiSession, build_parser, config_from_args
from tutorial_utils import build_sample_brief_advert, load_json_list, read_ids


def print_errors(errors: List[Dict[str, object]]) -> None:
    if not errors:
        return
    print("Errors encountered:")
    for error in errors:
        reference = error.get("reference") or error.get("advert_id") or "unknown"
        print(f"- {reference}: {error.get('detail')}")


def main() -> None:
    parser = build_parser("Bulk update adverts (PUT /api/v1/adverts/bulk-update).")
    parser.add_argument(
        "--updates-file",
        type=Path,
        default=None,
        help="JSON file containing an array of {advert_id, advert} objects.",
    )
    parser.add_argument(
        "--advert-ids",
        default=None,
        help="Comma-separated advert IDs to update.",
    )
    parser.add_argument(
        "--ids-file",
        type=Path,
        default=None,
        help="JSON array of advert IDs or {\"advert_ids\": [...]}.",
    )
    args = parser.parse_args()

    api = ClientApiSession.from_config(config_from_args(args))

    if args.updates_file:
        updates = load_json_list(args.updates_file)
    else:
        ids = read_ids(args.advert_ids, args.ids_file)
        if not ids:
            parser.error("Provide --updates-file or at least one advert ID.")
        updates = []
        for index, advert_id in enumerate(ids, start=1):
            payload = build_sample_brief_advert(index)
            payload["description"] = f"Bulk update example for {advert_id}."
            updates.append({"advert_id": advert_id, "advert": payload})

    if not updates:
        raise ValueError("No updates provided for bulk update.")

    response = api.json("PUT", "/adverts/bulk-update", json={"adverts": updates})
    adverts = response.get("adverts", []) if response else []
    print(f"Updated {len(adverts)} advert(s) in bulk.")
    print_errors(response.get("errors", []))


if __name__ == "__main__":
    main()
