from __future__ import annotations

import time
from typing import Iterable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.core.metrics import metrics_collector


class MetricsMiddleware(BaseHTTPMiddleware):
    """Capture rolling request metrics for admin dashboards."""

    _exclude_prefixes: Iterable[str] = (
        "/static",
        "/media",
        "/docs",
        "/redoc",
        "/openapi.json",
        "/favicon.ico",
    )

    async def dispatch(self, request: Request, call_next) -> Response:
        path = request.url.path
        if self._should_skip(path):
            return await call_next(request)

        start = time.perf_counter()
        try:
            response = await call_next(request)
        except Exception:
            duration_ms = (time.perf_counter() - start) * 1000
            metrics_collector.record(self._normalize_path(request), 500, duration_ms)
            raise

        duration_ms = (time.perf_counter() - start) * 1000
        metrics_collector.record(
            self._normalize_path(request),
            response.status_code,
            duration_ms,
        )
        return response

    def _should_skip(self, path: str) -> bool:
        return any(path.startswith(prefix) for prefix in self._exclude_prefixes)

    def _normalize_path(self, request: Request) -> str:
        route = request.scope.get("route")
        if route is not None and hasattr(route, "path"):
            return str(route.path)
        return request.url.path
