from __future__ import annotations

from collections import Counter, deque
from dataclasses import dataclass
from threading import Lock
from time import time
from typing import Deque, Dict, List, Optional


@dataclass(frozen=True)
class _MetricEvent:
    timestamp: float
    duration_ms: float
    status_code: int
    path: str


class MetricsCollector:
    """In-memory rolling window request metrics."""

    def __init__(self, window_seconds: int = 300, max_events: int = 10000) -> None:
        self._window_seconds = window_seconds
        self._max_events = max_events
        self._events: Deque[_MetricEvent] = deque()
        self._lock = Lock()

    def record(self, path: str, status_code: int, duration_ms: float) -> None:
        now = time()
        event = _MetricEvent(
            timestamp=now,
            duration_ms=duration_ms,
            status_code=status_code,
            path=path,
        )
        with self._lock:
            self._events.append(event)
            self._prune(now)
            while len(self._events) > self._max_events:
                self._events.popleft()

    def snapshot(self) -> Dict[str, object]:
        now = time()
        with self._lock:
            self._prune(now)
            events = list(self._events)

        total = len(events)
        if total == 0:
            return {
                "window_seconds": self._window_seconds,
                "total_requests": 0,
                "avg_response_time_ms": 0,
                "p95_response_time_ms": 0,
                "requests_per_minute": 0,
                "error_rate": 0,
                "top_endpoints": [],
            }

        durations = [e.duration_ms for e in events]
        durations.sort()
        p95_index = int(round(0.95 * (total - 1)))
        p95 = durations[p95_index] if durations else 0

        error_count = sum(1 for e in events if e.status_code >= 500)
        rpm = round(total * 60 / self._window_seconds, 2)

        counts = Counter(e.path for e in events)
        top_endpoints = [
            {"path": path, "requests": count}
            for path, count in counts.most_common(5)
        ]

        return {
            "window_seconds": self._window_seconds,
            "total_requests": total,
            "avg_response_time_ms": round(sum(durations) / total, 2),
            "p95_response_time_ms": round(p95, 2),
            "requests_per_minute": rpm,
            "error_rate": round(error_count / total * 100, 2),
            "top_endpoints": top_endpoints,
        }

    def _prune(self, now: float) -> None:
        cutoff = now - self._window_seconds
        while self._events and self._events[0].timestamp < cutoff:
            self._events.popleft()


metrics_collector = MetricsCollector()
