"""
Delete an advert via DELETE /api/v1/adverts/{advert_id}.
"""
from __future__ import annotations

from client_api_session import ClientApiSession, build_parser, config_from_args


def main() -> None:
    parser = build_parser("Delete an advert (DELETE /api/v1/adverts/{advert_id}).")
    parser.add_argument(
        "--advert-id",
        required=True,
        help="Advert identifier to delete.",
    )
    args = parser.parse_args()

    api = ClientApiSession.from_config(config_from_args(args))
    result = api.json("DELETE", f"/adverts/{args.advert_id}")
    print("Delete response:")
    print(ClientApiSession.pretty(result))


if __name__ == "__main__":
    main()
