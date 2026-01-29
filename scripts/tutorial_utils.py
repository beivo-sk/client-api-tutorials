from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


def load_json_file(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_json_dict(path: Path) -> Dict[str, Any]:
    payload = load_json_file(path)
    if not isinstance(payload, dict):
        raise ValueError(f"Expected a JSON object in {path}.")
    return payload


def load_json_list(path: Path) -> List[Any]:
    payload = load_json_file(path)
    if not isinstance(payload, list):
        raise ValueError(f"Expected a JSON array in {path}.")
    return payload


def parse_comma_list(value: Optional[str]) -> List[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def read_ids(ids: Optional[str], ids_file: Optional[Path]) -> List[str]:
    result: List[str] = []
    result.extend(parse_comma_list(ids))

    if ids_file:
        payload = load_json_file(ids_file)
        if isinstance(payload, list):
            result.extend(str(item) for item in payload)
        elif isinstance(payload, dict) and "advert_ids" in payload:
            result.extend(str(item) for item in payload["advert_ids"])
        else:
            raise ValueError("IDs file must be a JSON array or an object with 'advert_ids'.")

    seen = set()
    unique: List[str] = []
    for item in result:
        if item in seen:
            continue
        seen.add(item)
        unique.append(item)

    return unique


def build_sample_brief_advert(index: int = 1) -> Dict[str, object]:
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M")
    suffix = f" #{index}"
    lat_offset = index * 0.001
    lon_offset = index * 0.0015
    return {
        "title": f"Client API sample{suffix} ({timestamp})",
        "description": "Sample advert created via the Client API tutorial.",
        "advert_type": "rent",
        "reality_type": "flat",
        "reality_state": "renovated",
        "energy_rating": "A",
        "currency": "eur",
        "measurement_system": "metric",
        "price": {
            "overall": 900 + (index * 10),
            "utilities": 150,
            "show_price": True,
        },
        "layout": {
            "num_rooms": 2,
            "floor_area": 68.5,
            "floor_number": 4,
        },
        "features": {
            "furnishing": True,
            "lift": True,
            "dedicated_parking": False,
            "internet": "fiber_optic",
        },
        "location": {
            "lat": 48.14663 + lat_offset,
            "lon": 17.10775 + lon_offset,
        },
        "media": {
            "photos": [f"https://example.com/photos/sample-{index}.jpg"],
            "videos": [f"https://example.com/videos/sample-{index}.mp4"],
        },
        "is_vip": False,
    }
