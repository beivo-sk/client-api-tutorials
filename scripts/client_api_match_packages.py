"""
Assign adverts to packages via POST /api/v1/orders/match.

Provide --mapping-file to send your own JSON mapping payload, or
use --package-uid together with advert IDs to build a simple mapping.
"""
from __future__ import annotations

from pathlib import Path

from client_api_session import ClientApiSession, build_parser, config_from_args
from tutorial_utils import load_json_dict, read_ids


def main() -> None:
    parser = build_parser("Match packages to adverts (POST /api/v1/orders/match).")
    parser.add_argument(
        "--mapping-file",
        type=Path,
        default=None,
        help="JSON file containing the mapping payload.",
    )
    parser.add_argument(
        "--package-uid",
        default=None,
        help="Package UID to assign adverts to.",
    )
    parser.add_argument(
        "--advert-ids",
        default=None,
        help="Comma-separated advert IDs to assign.",
    )
    parser.add_argument(
        "--ids-file",
        type=Path,
        default=None,
        help="JSON array of advert IDs or {\"advert_ids\": [...]}.",
    )
    args = parser.parse_args()

    if args.mapping_file:
        mapping = load_json_dict(args.mapping_file)
    else:
        if not args.package_uid:
            parser.error("Provide --mapping-file or --package-uid.")
        advert_ids = read_ids(args.advert_ids, args.ids_file)
        if not advert_ids:
            parser.error("Provide at least one advert ID via --advert-ids or --ids-file.")
        mapping = {"mapping": [{"package_uid": args.package_uid, "advert_ids": advert_ids}]}

    api = ClientApiSession.from_config(config_from_args(args))
    response = api.json("POST", "/orders/match", json=mapping)
    print("Match response:")
    print(ClientApiSession.pretty(response))


if __name__ == "__main__":
    main()
