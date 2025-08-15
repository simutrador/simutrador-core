"""
WebSocket message models for SimuTrador trading simulation.

These models define the communication protocol between clients and the simulation server.
Based on the WebSocket API v2.0 specification.
"""

from datetime import datetime
from decimal import Decimal
from typing import Any, Literal

from pydantic import BaseModel, Field

from .enums import OrderSide, OrderType

# ===== CORE MESSAGE ENVELOPE =====


class WSMessage(BaseModel):
    """All WebSocket messages use this envelope."""

    type: str = Field(..., description="Message type")
    data: dict[str, Any] = Field(
        ..., description="Payload (simple dict for JSON safety)"
    )
    request_id: str | None = Field(None, description="For request/response correlation")
    timestamp: datetime = Field(..., description="Message timestamp")


# ===== AUTHENTICATION & CONNECTION =====


class ConnectionReadyData(BaseModel):
    """Server confirms WebSocket connection and authentication."""

    user_id: str = Field(..., description="Authenticated user ID")
    plan: str = Field(..., description="User plan (starter, professional, enterprise)")
    server_time: datetime = Field(..., description="Current server time")
    connection_expires_at: datetime = Field(..., description="When connection expires")
    idle_timeout_sec: int = Field(..., description="Idle timeout in seconds")
    max_simulation_duration_sec: int = Field(..., description="Max simulation duration")
    concurrent_connections_limit: int = Field(
        ..., description="Max concurrent connections"
    )
    supported_features: list[str] = Field(..., description="Supported features list")


class ConnectionWarningData(BaseModel):
    """Server warns about impending connection closure."""

    warning_type: Literal[
        "approaching_timeout", "imminent_closure", "rate_limit_warning"
    ] = Field(..., description="Type of warning")
    message: str = Field(..., description="Warning message")
    expires_at: datetime | None = Field(None, description="When connection expires")
    action_required: str = Field(..., description="Required action")
    seconds_remaining: int | None = Field(None, description="Seconds until closure")


class ConnectionClosingData(BaseModel):
    """Server notifies about connection closure."""

    reason: Literal[
        "idle_timeout",
        "max_duration",
        "api_key_revoked",
        "rate_limit",
        "simulation_complete",
        "server_maintenance",
    ] = Field(..., description="Reason for closure")
    message: str = Field(..., description="Closure message")
    close_code: int = Field(..., description="WebSocket close code")
    reconnect_allowed: bool = Field(..., description="Whether reconnection is allowed")
    session_state: str | None = Field(None, description="Session state after closure")


# ===== SESSION MANAGEMENT =====


class CreateSessionData(BaseModel):
    """WebSocket: Create new simulation session."""

    session_id: str = Field(..., description="Unique session identifier")
    symbols: list[str] = Field(..., description="list of symbols to trade")
    start: datetime = Field(..., description="Simulation start time")
    end: datetime = Field(..., description="Simulation end time")
    data_provider: str = Field(default="polygon", description="Data provider to use")
    initial_cash: Decimal = Field(..., description="Starting cash amount")
    commission_per_trade: Decimal = Field(
        default=Decimal("1.00"), description="Commission per trade"
    )
    slippage_bps: int = Field(default=5, description="Slippage in basis points")


class SessionCreatedData(BaseModel):
    """WebSocket: Session creation confirmation."""

    session_id: str = Field(..., description="Session identifier")
    estimated_ticks: int = Field(..., description="Total estimated ticks in simulation")
    symbols_loaded: list[str] = Field(..., description="Symbols with data available")
    data_range_actual: dict[str, Any] = Field(
        ..., description="Actual data availability per symbol"
    )
    server_ready: bool = Field(
        ..., description="Whether server is ready for simulation"
    )


# ===== SIMULATION CONTROL =====


class SimulationStartData(BaseModel):
    """Client requests simulation start."""

    flow_control: bool = Field(default=True, description="Enable tick acknowledgments")
    max_pending_ticks: int = Field(default=1, description="Backpressure control")
    account_update_frequency: Literal["every_fill", "every_tick", "on_demand"] = Field(
        default="every_fill", description="Account update frequency"
    )


class SimulationStartedData(BaseModel):
    """Server confirms simulation has begun."""

    session_id: str = Field(..., description="Session identifier")
    started_at: datetime = Field(..., description="Simulation start timestamp")
    estimated_duration_sec: int = Field(
        ..., description="Estimated duration in seconds"
    )
    tick_interval_ms: int = Field(..., description="Time between ticks in milliseconds")
    flow_control_enabled: bool = Field(
        ..., description="Whether flow control is enabled"
    )


class TickData(BaseModel):
    """Server advances simulation time."""

    sim_time: datetime = Field(..., description="Current simulation time")
    sequence_id: int = Field(..., description="Sequence ID for ordering guarantees")
    market_session: Literal["pre_market", "regular", "after_hours"] = Field(
        ..., description="Current market session"
    )
    symbols_trading: list[str] = Field(
        ..., description="Symbols tradeable at this time"
    )
    is_eod: bool = Field(default=False, description="Whether this is end of day")


class TickAckData(BaseModel):
    """Client acknowledges tick and signals readiness."""

    sequence_id: int = Field(..., description="Echo from TickData")
    processing_status: Literal["ready", "processing", "need_time"] = Field(
        ..., description="Client processing status"
    )
    orders_pending: int = Field(
        default=0, description="Number of orders client will send"
    )
    max_wait_ms: int = Field(default=1000, description="Maximum wait time needed")


# ===== ORDER MANAGEMENT =====


class OrderData(BaseModel):
    """Individual order within a batch."""

    order_id: str = Field(..., description="Unique order identifier")
    symbol: str = Field(..., description="Trading symbol")
    side: OrderSide = Field(..., description="Order side (buy/sell)")
    type: OrderType = Field(..., description="Order type (market/limit)")
    quantity: int = Field(..., description="Order quantity", gt=0)
    price: Decimal | None = Field(
        None, description="Limit price (required for limit orders)"
    )
    stop_loss: Decimal | None = Field(None, description="Stop loss price")
    take_profit: Decimal | None = Field(None, description="Take profit price")
    time_in_force: Literal["day", "gtc", "ioc"] = Field(
        default="day", description="Time in force"
    )


class OrderBatchData(BaseModel):
    """Client submits batch of orders."""

    batch_id: str = Field(..., description="Unique batch identifier")
    orders: list[OrderData] = Field(..., description="list of orders in batch")
    execution_mode: Literal["atomic", "best_effort"] = Field(
        default="best_effort", description="Execution mode"
    )
    parent_strategy: str | None = Field(
        None, description="Strategy identifier for tracking"
    )


class BatchAckData(BaseModel):
    """Server acknowledges order batch."""

    batch_id: str = Field(..., description="Batch identifier")
    accepted_orders: list[str] = Field(..., description="Order IDs that were accepted")
    rejected_orders: dict[str, str] = Field(
        ..., description="Order ID to rejection reason mapping"
    )
    estimated_fills: dict[str, Decimal] = Field(
        ..., description="Order ID to estimated fill price"
    )


class ExecutionReportData(BaseModel):
    """Server reports order execution."""

    execution_id: str = Field(..., description="Unique execution identifier")
    order_id: str = Field(..., description="Order identifier")
    symbol: str = Field(..., description="Trading symbol")
    side: OrderSide = Field(..., description="Order side")
    quantity: int = Field(..., description="Executed quantity")
    price: Decimal = Field(..., description="Execution price")
    timestamp: datetime = Field(..., description="Execution timestamp")
    commission: Decimal = Field(..., description="Commission charged")
    slippage_bps: int = Field(..., description="Slippage applied in basis points")


# ===== ACCOUNT & PORTFOLIO =====


class PositionData(BaseModel):
    """Current position in a symbol."""

    symbol: str = Field(..., description="Trading symbol")
    quantity: int = Field(
        ..., description="Position quantity (positive=long, negative=short)"
    )
    avg_cost: Decimal = Field(..., description="Average cost basis")
    market_value: Decimal = Field(..., description="Current market value")
    unrealized_pnl: Decimal = Field(..., description="Unrealized profit/loss")


class AccountSnapshotData(BaseModel):
    """Current account state."""

    cash: Decimal = Field(..., description="Available cash")
    equity: Decimal = Field(..., description="Total equity")
    buying_power: Decimal = Field(..., description="Available buying power")
    day_pnl: Decimal = Field(..., description="Day profit/loss")
    positions: list[PositionData] = Field(..., description="Current positions")
    open_orders: list[str] = Field(..., description="Open order IDs")


# ===== ERROR HANDLING =====


class ErrorData(BaseModel):
    """Enhanced error reporting."""

    error_code: str = Field(..., description="Error code (e.g., INVALID_ORDER)")
    message: str = Field(..., description="Error message")
    error_type: Literal["validation", "execution", "connection", "data"] = Field(
        ..., description="Error type"
    )
    severity: Literal["warning", "error", "fatal"] = Field(
        ..., description="Error severity"
    )
    details: dict[str, Any] | None = Field(None, description="Additional error details")
    retry_allowed: bool = Field(default=False, description="Whether retry is allowed")


# ===== SIMULATION END =====


class SimulationEndData(BaseModel):
    """Final simulation results."""

    session_id: str = Field(..., description="Session identifier")
    final_equity: Decimal = Field(..., description="Final equity value")
    total_return_pct: Decimal = Field(..., description="Total return percentage")
    total_trades: int = Field(..., description="Total number of trades")
    win_rate: Decimal = Field(..., description="Win rate percentage")
    sharpe_ratio: Decimal | None = Field(None, description="Sharpe ratio")
    max_drawdown_pct: Decimal = Field(..., description="Maximum drawdown percentage")
    simulation_duration_sec: int = Field(
        ..., description="Simulation duration in seconds"
    )
