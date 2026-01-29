"""
List orders via GET /api/v1/orders.
"""
from __future__ import annotations

from client_api_session import ClientApiSession, build_parser, config_from_args


def main() -> None:
    parser = build_parser("List orders (GET /api/v1/orders).")
    parser.add_argument("--page", type=int, default=1, help="Page number to fetch.")
    parser.add_argument("--page-size", type=int, default=20, help="Number of orders per page.")
    parser.add_argument(
        "--sort",
        choices=["asc", "desc"],
        default="desc",
        help="Sort direction for order list.",
    )
    args = parser.parse_args()

    api = ClientApiSession.from_config(config_from_args(args))
    payload = api.json(
        "GET",
        "/orders",
        params={"page": args.page, "page_size": args.page_size, "sort": args.sort},
    )
    if not payload:
        raise RuntimeError("Empty response received from /orders.")

    print(f"Page {payload['meta']['current_page']} of {payload['meta']['page_count']}")
    orders = payload.get("orders", [])
    if not orders:
        print("No orders found for this account.")
        return

    for order in orders:
        order_id = order.get("order_id") or order.get("uid") or "unknown"
        status = order.get("status", "unknown")
        package_count = len(order.get("packages", []))
        print(f"- {order_id} -> {status} ({package_count} package(s))")


if __name__ == "__main__":
    main()
