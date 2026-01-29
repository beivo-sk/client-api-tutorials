"""
Create multiple adverts in one request via POST /api/v1/adverts/bulk-create.

Provide --payload-file to send your own JSON array of BriefAdvert payloads.
If omitted, sample payloads are generated.
"""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List

from client_api_session import ClientApiSession, build_parser, config_from_args
from tutorial_utils import build_sample_brief_advert, load_json_list


def print_errors(errors: List[Dict[str, object]]) -> None:
    if not errors:
        return
    print("Errors encountered:")
    for error in errors:
        reference = error.get("reference") or "unknown"
        print(f"- {reference}: {error.get('detail')}")


def main() -> None:
    parser = build_parser("Bulk create adverts (POST /api/v1/adverts/bulk-create).")
    parser.add_argument(
        "--payload-file",
        type=Path,
        default=None,
        help="JSON file containing an array of BriefAdvert payloads.",
    )
    parser.add_argument(
        "--total",
        type=int,
        default=5,
        help="Number of sample adverts to generate when no payload file is supplied.",
    )
    args = parser.parse_args()

    api = ClientApiSession.from_config(config_from_args(args))
    if args.payload_file:
        payloads = load_json_list(args.payload_file)
    else:
        payloads = [build_sample_brief_advert(index) for index in range(1, args.total + 1)]

    if not payloads:
        raise ValueError("No adverts provided for bulk create.")

    response = api.json("POST", "/adverts/bulk-create", json={"adverts": payloads})
    adverts = response.get("adverts", []) if response else []
    print(f"Created {len(adverts)} advert(s) in bulk.")
    print_errors(response.get("errors", []))


if __name__ == "__main__":
    main()
