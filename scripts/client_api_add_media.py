"""
Attach media to an advert via POST /api/v1/adverts/{advert_id}/media.

Use --media-url for external links and --upload-file to upload to MinIO.
"""
from __future__ import annotations

import mimetypes
from pathlib import Path

from client_api_session import ClientApiSession, build_parser, config_from_args


def main() -> None:
    parser = build_parser("Add media to an advert (POST /api/v1/adverts/{advert_id}/media).")
    parser.add_argument("--advert-id", required=True, help="Advert identifier.")
    parser.add_argument(
        "--media-type",
        choices=["photos", "videos", "visualizations", "visualizations3d"],
        default="photos",
        help="Media type for the upload.",
    )
    parser.add_argument(
        "--media-url",
        action="append",
        default=[],
        help="External media URL to attach (repeatable).",
    )
    parser.add_argument(
        "--upload-file",
        type=Path,
        default=None,
        help="Optional file path to upload to MinIO.",
    )
    args = parser.parse_args()

    if not args.media_url and not args.upload_file:
        parser.error("Provide at least one --media-url or --upload-file.")

    if args.upload_file and not args.upload_file.exists():
        raise FileNotFoundError(f"Upload file not found: {args.upload_file}")

    api = ClientApiSession.from_config(config_from_args(args))
    form_data = [("media_type", args.media_type)]
    for url in args.media_url:
        form_data.append(("urls", url))

    if args.upload_file:
        mime_type = mimetypes.guess_type(args.upload_file.name)[0] or "application/octet-stream"
        with args.upload_file.open("rb") as handle:
            files = [("files", (args.upload_file.name, handle, mime_type))]
            response = api.request(
                "POST",
                f"/adverts/{args.advert_id}/media",
                data=form_data,
                files=files,
            ).json()
    else:
        response = api.request(
            "POST",
            f"/adverts/{args.advert_id}/media",
            data=form_data,
        ).json()

    print("Updated media:")
    print(ClientApiSession.pretty(response.get("media", response)))


if __name__ == "__main__":
    main()
