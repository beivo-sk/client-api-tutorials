"""
Update an advert via PUT /api/v1/adverts/{advert_id}.

The API expects a full BriefAdvert payload, not a patch.
Provide --payload-file to send your own JSON payload.
"""
from __future__ import annotations

from pathlib import Path

from client_api_session import ClientApiSession, build_parser, config_from_args
from tutorial_utils import build_sample_brief_advert, load_json_dict


def main() -> None:
    parser = build_parser("Update an advert (PUT /api/v1/adverts/{advert_id}).")
    parser.add_argument(
        "--advert-id",
        required=True,
        help="Advert identifier to update.",
    )
    parser.add_argument(
        "--payload-file",
        type=Path,
        default=None,
        help="JSON file containing a BriefAdvert payload.",
    )
    args = parser.parse_args()

    api = ClientApiSession.from_config(config_from_args(args))
    payload = load_json_dict(args.payload_file) if args.payload_file else build_sample_brief_advert()
    payload["description"] = "Updated via client API tutorial."

    updated = api.json("PUT", f"/adverts/{args.advert_id}", json=payload)
    print("Updated advert:")
    print(ClientApiSession.pretty(updated))


if __name__ == "__main__":
    main()
