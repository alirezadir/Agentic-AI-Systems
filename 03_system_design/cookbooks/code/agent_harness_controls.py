"""Small examples of production controls for agent harnesses.

This is not a full framework. It shows the mechanics that are easy to skip:
budget caps, trace events, idempotency keys, and approval gates.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Literal, Optional
from uuid import uuid4


EventType = Literal[
    "model_call",
    "tool_call",
    "approval_requested",
    "approval_granted",
    "budget_exceeded",
    "task_completed",
]


@dataclass
class Budget:
    max_steps: int
    max_cost_usd: float
    max_tool_calls: int
    steps: int = 0
    cost_usd: float = 0.0
    tool_calls: int = 0

    def charge_step(self, cost_usd: float = 0.0, tool_call: bool = False) -> None:
        self.steps += 1
        self.cost_usd += cost_usd
        if tool_call:
            self.tool_calls += 1
        self.check()

    def check(self) -> None:
        if self.steps > self.max_steps:
            raise BudgetExceeded(f"step budget exceeded: {self.steps}>{self.max_steps}")
        if self.cost_usd > self.max_cost_usd:
            raise BudgetExceeded(f"cost budget exceeded: {self.cost_usd}>{self.max_cost_usd}")
        if self.tool_calls > self.max_tool_calls:
            raise BudgetExceeded(
                f"tool-call budget exceeded: {self.tool_calls}>{self.max_tool_calls}"
            )


class BudgetExceeded(Exception):
    """Raised when an agent run exceeds an explicit budget."""


@dataclass
class TraceEvent:
    event_type: EventType
    payload: dict[str, Any]
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


@dataclass
class Trace:
    task_id: str
    trace_id: str = field(default_factory=lambda: f"tr_{uuid4().hex}")
    events: list[TraceEvent] = field(default_factory=list)

    def add(self, event_type: EventType, **payload: Any) -> None:
        self.events.append(TraceEvent(event_type=event_type, payload=payload))


class IdempotencyStore:
    """In production, back this with Redis, Postgres, or another durable store."""

    def __init__(self) -> None:
        self._completed: dict[str, Any] = {}

    def get(self, key: str) -> Optional[Any]:
        return self._completed.get(key)

    def put(self, key: str, result: Any) -> None:
        self._completed[key] = result


def side_effecting_refund_tool(
    *,
    ticket_id: str,
    amount_usd: float,
    idempotency_key: str,
    store: IdempotencyStore,
) -> dict[str, Any]:
    """Example write tool protected by idempotency.

    Retrying the same request returns the first result instead of issuing
    a second refund.
    """

    previous = store.get(idempotency_key)
    if previous is not None:
        return previous

    result = {
        "refund_id": f"rf_{uuid4().hex[:10]}",
        "ticket_id": ticket_id,
        "amount_usd": amount_usd,
        "status": "submitted",
    }
    store.put(idempotency_key, result)
    return result


def requires_approval(action: str, amount_usd: float) -> bool:
    if action == "refund" and amount_usd > 25:
        return True
    return False


def run_support_refund_step(ticket_id: str, amount_usd: float) -> Trace:
    task_id = f"task_{uuid4().hex[:10]}"
    budget = Budget(max_steps=6, max_cost_usd=0.25, max_tool_calls=2)
    trace = Trace(task_id=task_id)
    idempotency_store = IdempotencyStore()

    try:
        budget.charge_step(cost_usd=0.01)
        trace.add("model_call", model="router-small", purpose="classify_refund_request")

        if requires_approval("refund", amount_usd):
            trace.add(
                "approval_requested",
                action="refund",
                ticket_id=ticket_id,
                amount_usd=amount_usd,
            )
            return trace

        budget.charge_step(cost_usd=0.0, tool_call=True)
        key = f"{task_id}:refund:{ticket_id}:{amount_usd}"
        result = side_effecting_refund_tool(
            ticket_id=ticket_id,
            amount_usd=amount_usd,
            idempotency_key=key,
            store=idempotency_store,
        )
        trace.add("tool_call", tool="refund", idempotency_key=key, result=result)

        budget.charge_step(cost_usd=0.02)
        trace.add("task_completed", status="ok")
        return trace
    except BudgetExceeded as exc:
        trace.add("budget_exceeded", reason=str(exc))
        return trace


if __name__ == "__main__":
    sample_trace = run_support_refund_step(ticket_id="T-1001", amount_usd=12.50)
    for event in sample_trace.events:
        print(event)
