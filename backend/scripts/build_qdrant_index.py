from __future__ import annotations

import json
import sys
from pathlib import Path


BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.rag.build_qdrant_index import build_qdrant_index  # noqa: E402


def main() -> None:
    result = build_qdrant_index()
    print(
        json.dumps(
            {
                "status": "success",
                "qdrant_url": result.qdrant_url,
                "collection_name": result.collection_name,
                "chunks_loaded": result.chunks_loaded,
                "chunks_upserted": result.chunks_upserted,
                "points_count": result.points_count,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
