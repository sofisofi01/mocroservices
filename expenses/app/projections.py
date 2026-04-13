from typing import Dict, List, Optional


def replay(events: List[dict]) -> Dict[str, dict]:
    state: Dict[str, dict] = {}

    for event in events:
        event_type = event.get("event_type")
        expense_id = str(event.get("expense_id"))

        if event_type == "ExpenseCreated":
            state[expense_id] = {
                "id": expense_id,
                "user_id": event["user_id"],
                "title": event["title"],
                "cost": event["cost"],
                "quantity": event["quantity"],
                "date": event["date"],
                "version": 1,
            }

        elif event_type == "ExpenseUpdated":
            if expense_id in state:
                for field in ("title", "cost", "quantity", "date"):
                    if event.get(field) is not None:
                        state[expense_id][field] = event[field]
                state[expense_id]["version"] += 1

        elif event_type == "ExpenseDeleted":
            state.pop(expense_id, None)

    return state


def replay_one(events: List[dict], expense_id: str) -> Optional[dict]:
    return replay(events).get(str(expense_id))
