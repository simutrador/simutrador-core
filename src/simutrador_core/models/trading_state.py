"""Trading state models for per-session simulation state.

These models represent the server-side view of cash, positions, open
orders, and last prices for a given simulation session. They are shared
between simutrador-server and any client tooling that needs to inspect
or serialize the internal trading state.
"""

from __future__ import annotations

from decimal import Decimal
from typing import Literal

from pydantic import BaseModel

from .enums import OrderSide, OrderStatus
from .websocket import PositionData


class OpenOrderState(BaseModel):
    """Internal per-order state tracked by the execution engine.

    This complements the public ``OrderData`` WebSocket model with
    lifecycle status and bracket configuration. It is not sent directly
    over the wire; instead, it is used to derive ExecutionReportData and
    AccountSnapshotData.
    """

    order_id: str
    symbol: str
    side: OrderSide
    quantity: int
    stop_loss: Decimal | None = None
    take_profit: Decimal | None = None
    status: OrderStatus = OrderStatus.OPEN


class SymbolPriceState(BaseModel):
    """Last known price for a symbol within a simulation session.

    Used by the execution engine to evaluate order fills and bracket
    triggers based on the latest candle close.
    """

    symbol: str
    last_price: Decimal


class PositionBracketState(BaseModel):
    """Server-side bracket configuration attached to an open position.

    Tracks stop-loss/take-profit configuration and time-in-force for exit
    management. This is stored inside SessionTradingState and not sent
    directly over the wire.
    """

    symbol: str
    side: OrderSide
    quantity: int
    stop_loss: Decimal | None = None
    take_profit: Decimal | None = None
    time_in_force: Literal["day", "gtc", "ioc"] = "day"



class SessionTradingState(BaseModel):
    """Aggregate trading state for a single simulation session.

    This state is typically stored inside ``SimulationSession.metadata``
    on the server side and updated on each tick and order event.
    """

    cash: Decimal
    positions: list[PositionData] = []
    open_orders: list[OpenOrderState] = []
    last_prices: list[SymbolPriceState] = []
    trade_count: int = 0
    brackets: list[PositionBracketState] = []

