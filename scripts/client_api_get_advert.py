"""
Retrieve a single advert via GET /api/v1/adverts/{advert_id}.
"""
from __future__ import annotations

from client_api_session import ClientApiSession, build_parser, config_from_args


def main() -> None:
    parser = build_parser("Get an advert (GET /api/v1/adverts/{advert_id}).")
    parser.add_argument(
        "--advert-id",
        required=True,
        help="Advert identifier to fetch.",
    )
    args = parser.parse_args()

    api = ClientApiSession.from_config(config_from_args(args))
    advert = api.json("GET", f"/adverts/{args.advert_id}")
    print("Advert details:")
    print(ClientApiSession.pretty(advert))


if __name__ == "__main__":
    main()
