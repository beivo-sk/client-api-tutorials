"""
Unpublish an advert via POST /api/v1/adverts/{advert_id}/unpublish.
"""
from __future__ import annotations

from client_api_session import ClientApiSession, build_parser, config_from_args


def main() -> None:
    parser = build_parser("Unpublish an advert (POST /api/v1/adverts/{advert_id}/unpublish).")
    parser.add_argument(
        "--advert-id",
        required=True,
        help="Advert identifier to unpublish.",
    )
    args = parser.parse_args()

    api = ClientApiSession.from_config(config_from_args(args))
    result = api.json("POST", f"/adverts/{args.advert_id}/unpublish")
    print("Unpublish response:")
    print(ClientApiSession.pretty(result.get("status", result)))


if __name__ == "__main__":
    main()
