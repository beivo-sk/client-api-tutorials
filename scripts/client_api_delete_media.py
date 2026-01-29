"""
Remove media from an advert via POST /api/v1/adverts/{advert_id}/delete-media.
"""
from __future__ import annotations

from pathlib import Path

from client_api_session import ClientApiSession, build_parser, config_from_args
from tutorial_utils import load_json_list


def main() -> None:
    parser = build_parser("Delete media from an advert (POST /api/v1/adverts/{advert_id}/delete-media).")
    parser.add_argument("--advert-id", required=True, help="Advert identifier.")
    parser.add_argument(
        "--media-type",
        choices=["photos", "videos", "visualizations", "visualizations3d"],
        default="photos",
        help="Media type to delete.",
    )
    parser.add_argument(
        "--media-url",
        action="append",
        default=[],
        help="Media URL to remove (repeatable).",
    )
    parser.add_argument(
        "--urls-file",
        type=Path,
        default=None,
        help="JSON file containing an array of media URLs.",
    )
    args = parser.parse_args()

    media_urls = list(args.media_url)
    if args.urls_file:
        media_urls.extend(load_json_list(args.urls_file))

    if not media_urls:
        parser.error("Provide at least one --media-url or --urls-file.")

    api = ClientApiSession.from_config(config_from_args(args))
    response = api.json(
        "POST",
        f"/adverts/{args.advert_id}/delete-media",
        params={"media_type": args.media_type},
        json=media_urls,
    )
    print("Updated media:")
    print(ClientApiSession.pretty(response.get("media", response)))


if __name__ == "__main__":
    main()
