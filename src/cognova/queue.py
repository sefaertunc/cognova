"""Generation queue — sequential execution gate.

FIFO queue enforcing one-at-a-time generation across all interfaces
(MCP server and web panel). Next item starts only after current item
reaches terminal state (approved/rejected/abandoned).

Repair loops retry in-place within the same queue slot.
Optional JSON persistence at .cognova/queue.json for restart recovery.
"""

__all__ = ["GenerationQueue", "QueueItem", "QueueStatus"]
