"""
Reusable HTTP helper + CLI utilities for the Client API tutorials.

Every tutorial exposes `--base-url`, `--basic-user`, `--basic-password`,
`--account-uid`, and `--api-key` flags, each defaulting to the similarly named
environment variable (base-url defaults to http://localhost:8081/api/v1).
"""
from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests
from requests import Response
from requests.auth import HTTPBasicAuth


@dataclass
class ClientApiConfig:
    base_url: str
    basic_user: str
    basic_password: str
    account_uid: str
    api_key: str

    @classmethod
    def from_env(cls) -> "ClientApiConfig":
        return cls(
            base_url=os.getenv("CLIENT_API_BASE_URL", "http://localhost:8081/api/v1"),
            basic_user=os.getenv("CLIENT_API_BASIC_USER", ""),
            basic_password=os.getenv("CLIENT_API_BASIC_PASSWORD", ""),
            account_uid=os.getenv("CLIENT_API_ACCOUNT", ""),
            api_key=os.getenv("CLIENT_API_KEY", ""),
        )


def build_parser(description: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=description)
    env_config = ClientApiConfig.from_env()
    parser.add_argument(
        "--base-url",
        default=env_config.base_url,
        help=f"Client API base URL (default: {env_config.base_url})",
    )
    parser.add_argument(
        "--basic-user",
        default=env_config.basic_user or None,
        help="HTTP Basic username (env: CLIENT_API_BASIC_USER)",
    )
    parser.add_argument(
        "--basic-password",
        default=env_config.basic_password or None,
        help="HTTP Basic password (env: CLIENT_API_BASIC_PASSWORD)",
    )
    parser.add_argument(
        "--account-uid",
        default=env_config.account_uid or None,
        help="Account UID used for X-Client-Account (env: CLIENT_API_ACCOUNT)",
    )
    parser.add_argument(
        "--api-key",
        default=env_config.api_key or None,
        help="Plaintext API key used for X-Client-Api-Key (env: CLIENT_API_KEY)",
    )
    return parser


def config_from_args(args: argparse.Namespace) -> ClientApiConfig:
    values = {
        "basic_user": args.basic_user,
        "basic_password": args.basic_password,
        "account_uid": args.account_uid,
        "api_key": args.api_key,
    }
    missing = [name for name, value in values.items() if not value]
    if missing:
        joined = ", ".join(missing)
        raise SystemExit(
            f"Missing credentials: {joined}. "
            f"Provide them via CLI flags or environment variables."
        )
    return ClientApiConfig(
        base_url=args.base_url,
        basic_user=args.basic_user,
        basic_password=args.basic_password,
        account_uid=args.account_uid,
        api_key=args.api_key,
    )


@dataclass
class ClientApiSession:
    base_url: str
    session: requests.Session

    @classmethod
    def from_config(cls, config: ClientApiConfig) -> "ClientApiSession":
        sess = requests.Session()
        sess.auth = HTTPBasicAuth(config.basic_user, config.basic_password)
        sess.headers.update({
            "X-Client-Account": config.account_uid,
            "X-Client-Api-Key": config.api_key,
            "Accept": "application/json",
        })
        return cls(base_url=config.base_url.rstrip("/"), session=sess)

    @classmethod
    def from_env(cls) -> "ClientApiSession":
        """
        Build an authenticated session using environment variables.
        """
        config = ClientApiConfig.from_env()
        missing = [
            name for name, value in {
                "CLIENT_API_BASIC_USER": config.basic_user,
                "CLIENT_API_BASIC_PASSWORD": config.basic_password,
                "CLIENT_API_ACCOUNT": config.account_uid,
                "CLIENT_API_KEY": config.api_key,
            }.items() if not value
        ]
        if missing:
            raise RuntimeError(f"Missing environment variables: {', '.join(missing)}")
        return cls.from_config(config)

    def request(self, method: str, path: str, timeout: float = 30, **kwargs: Any) -> Response:
        """
        Send a raw HTTP request and raise for HTTP errors.
        """
        if not path.startswith("/"):
            path = f"/{path}"
        url = f"{self.base_url}{path}"
        response = self.session.request(method=method.upper(), url=url, timeout=timeout, **kwargs)
        response.raise_for_status()
        return response

    def json(self, method: str, path: str, timeout: float = 30, **kwargs: Any) -> Optional[Dict[str, Any]]:
        """
        Convenience wrapper that returns JSON bodies (or None for empty responses).
        """
        response = self.request(method=method, path=path, timeout=timeout, **kwargs)
        if not response.content:
            return None
        return response.json()

    @staticmethod
    def pretty(data: Any) -> str:
        """
        Turn a Python object into formatted JSON for printing.
        """
        return json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False)


__all__ = ["ClientApiSession", "ClientApiConfig", "build_parser", "config_from_args"]
