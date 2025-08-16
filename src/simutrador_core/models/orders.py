"""
Order-related Pydantic models for SimuTrador WebSocket communication.

These models are shared between the simulation server and client SDKs
for WebSocket-based trading simulation.
"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, ValidationInfo, field_validator
from typing_extensions import override

from .enums import OrderSide, OrderType


class Order(BaseModel):
    """
    Individual order model representing a trading instruction.

    This model is used for WebSocket communication between clients and
    the simulation server.
    """

    entry_time: datetime = Field(
        ..., description="ISO 8601 timestamp when the order should be entered"
    )
    entry_type: OrderType = Field(
        ..., description="Order type: MKT (market) or LMT (limit)"
    )
    entry_price: float | None = Field(
        None,
        description="Entry price for limit orders (ignored for market orders)",
        gt=0,
    )
    side: OrderSide = Field(..., description="Order side: buy or sell")
    stop_loss: float | None = Field(None, description="Stop loss price level", gt=0)
    take_profit: float | None = Field(None, description="Take profit price level", gt=0)

    @field_validator("entry_price")
    @classmethod
    def validate_entry_price(
        cls, v: float | None, info: ValidationInfo
    ) -> float | None:
        """Validate entry price is required for limit orders."""
        if info.data.get("entry_type") == OrderType.LIMIT and v is None:
            raise ValueError("entry_price is required for limit orders")
        return v

    @field_validator("stop_loss", "take_profit")
    @classmethod
    def validate_price_levels(cls, v: float | None) -> float | None:
        """Validate price levels are positive if provided."""
        if v is not None and v <= 0:
            raise ValueError("Price levels must be positive")
        return v

    @override
    def model_post_init(self, __context: Any) -> None:
        """Additional validation after model initialization."""
        if self.entry_type == OrderType.LIMIT and self.entry_price is None:
            raise ValueError("entry_price is required for limit orders")

        # Validate stop loss and take profit levels make sense relative to entry price
        if self.entry_price is not None:
            if self.side == OrderSide.BUY:
                if self.stop_loss is not None and self.stop_loss >= self.entry_price:
                    raise ValueError(
                        "Stop loss must be below entry price for buy orders"
                    )
                if (
                    self.take_profit is not None
                    and self.take_profit <= self.entry_price
                ):
                    raise ValueError(
                        "Take profit must be above entry price for buy orders"
                    )
            else:  # SELL
                if self.stop_loss is not None and self.stop_loss <= self.entry_price:
                    raise ValueError(
                        "Stop loss must be above entry price for sell orders"
                    )
                if (
                    self.take_profit is not None
                    and self.take_profit >= self.entry_price
                ):
                    raise ValueError(
                        "Take profit must be below entry price for sell orders"
                    )


class OrderBatch(BaseModel):
    """
    Batch of orders sent via WebSocket.

    Used for sending multiple orders in a single WebSocket message.
    """

    orders: list[Order] = Field(
        ..., description="List of orders to execute", min_length=1
    )
    batch_id: str | None = Field(
        None, description="Optional batch identifier for tracking"
    )

    @field_validator("orders")
    @classmethod
    def validate_orders_not_empty(cls, v: list[Order]) -> list[Order]:
        """Validate that orders list is not empty."""
        if not v:
            raise ValueError("Orders list cannot be empty")
        return v
