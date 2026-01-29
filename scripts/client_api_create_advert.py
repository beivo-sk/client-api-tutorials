"""
Create a new advert via POST /api/v1/adverts.

Provide --payload-file to send your own BriefAdvert JSON payload.
If omitted, a sample payload is generated.
"""
from __future__ import annotations

from pathlib import Path

from client_api_session import ClientApiSession, build_parser, config_from_args
from tutorial_utils import build_sample_brief_advert, load_json_dict


def main() -> None:
    parser = build_parser("Create a single advert (POST /api/v1/adverts).")
    parser.add_argument(
        "--payload-file",
        type=Path,
        default=None,
        help="JSON file containing a BriefAdvert payload.",
    )
    args = parser.parse_args()

    api = ClientApiSession.from_config(config_from_args(args))
    payload = load_json_dict(args.payload_file) if args.payload_file else build_sample_brief_advert()

    created = api.json("POST", "/adverts", json=payload)
    print("Created advert:")
    print(ClientApiSession.pretty(created))


if __name__ == "__main__":
    main()
