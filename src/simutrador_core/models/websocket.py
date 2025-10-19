"""
WebSocket message models for SimuTrador trading simulation.

These models define the public protocol between clients and the simulation server
as described in the WebSocket API v2 documentation. Fields are aligned with the
examples; additional fields are optional to allow forward-compatibility.
"""

from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, Field

from .enums import OrderSide, WSErrorCode
from .price_data import PriceCandle, Timeframe

# ===== ENUMS =====


class UserPlan(str, Enum):
    """User subscription plans with different rate limits."""

    FREE = "free"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"


# ===== CORE MESSAGE ENVELOPE =====


class WSMessage(BaseModel):
    """Generic envelope: {"type": "...", "data": {...}, "request_id": "..."}.

    Timestamp is optional (not present in all examples) and may be added by the server.
    """

    type: str = Field(..., description="Message type")
    data: dict[str, Any] = Field(..., description="Payload dictionary")
    request_id: str | None = Field(
        None, description="For request/response correlation when applicable"
    )
    timestamp: datetime | None = Field(None, description="Message timestamp")


# ===== HEALTH =====


class HealthStatus(BaseModel):
    """Standardized health status payload sent in WSMessage.data for health checks."""

    status: Literal["ok", "degraded", "unhealthy"] = "ok"
    server_time: datetime | None = None
    server_version: str | None = None
    message: str | None = None


# ===== AUTHENTICATION =====


class TokenRequest(BaseModel):
    """REST API: Request JWT token (API key sent in header)."""

    # API key sent in X-API-Key header, no body needed
    pass


class TokenResponse(BaseModel):
    """REST API: JWT token response."""

    access_token: str
    expires_in: int  # Token lifetime in seconds
    token_type: str = "Bearer"
    user_id: str
    plan: UserPlan


class UserLimitsResponse(BaseModel):
    """REST API: Current user rate limits."""

    plan: UserPlan
    limits: dict[str, int]  # Current limits
    usage: dict[str, int]  # Current usage
    reset_times: dict[str, datetime]  # When limits reset


# ===== CONNECTION =====


class ConnectionReadyData(BaseModel):
    """Server confirms WebSocket connection and authentication."""

    user_id: str
    plan: str
    connection_expires_at: datetime
    idle_timeout_sec: int
    max_simulation_duration_sec: int
    concurrent_connections_limit: int
    # Optional extras the server may include
    server_time: datetime | None = None
    supported_features: list[str] = Field(default_factory=list)


class ConnectionWarningData(BaseModel):
    """Server warns about impending connection closure."""

    warning_type: Literal[
        "approaching_timeout", "imminent_closure", "rate_limit_warning"
    ]
    message: str
    expires_at: datetime | None = None
    action_required: str
    seconds_remaining: int | None = None


class ConnectionClosingData(BaseModel):
    """Server notifies about connection closure."""

    reason: Literal[
        "idle_timeout",
        "max_duration",
        "api_key_revoked",
        "rate_limit",
        "simulation_complete",
        "server_maintenance",
    ]
    message: str
    close_code: int
    reconnect_allowed: bool
    session_state: str | None = None


# ===== SESSION MANAGEMENT =====


class CreateSessionData(BaseModel):
    """Client: Create new simulation session."""

    session_id: str
    symbols: list[str]
    start: datetime
    end: datetime
    data_provider: str = Field(default="polygon")
    initial_cash: Decimal



class StartSimulationRequest(BaseModel):
    """Client: Start simulation request matching server API.

    This model intentionally mirrors the server's current expected fields so both
    client and server share the same contract without adapters.
    """

    symbols: list[str]
    start_date: datetime
    end_date: datetime
    initial_capital: Decimal
    # Optional parameters
    data_provider: str | None = None
    commission_per_share: Decimal | None = None
    slippage_bps: int | None = None
    metadata: dict[str, Any] | None = None


class SessionCreatedData(BaseModel):
    """Server: Session creation confirmation."""

    session_id: str
    estimated_ticks: int
    symbols_loaded: list[str]
    # Optional extras
    data_range_actual: dict[str, Any] | None = None
    server_ready: bool | None = None


# ===== SIMULATION CONTROL =====


class SimulationStartData(BaseModel):
    """Client requests simulation start."""

    flow_control: bool = True
    max_pending_ticks: int = 1


class SimulationStartedData(BaseModel):
    """Server confirms simulation has begun."""

    session_id: str
    started_at: datetime
    flow_control_enabled: bool
    # Optional extras
    estimated_duration_sec: int | None = None
    tick_interval_ms: int | None = None


class TickData(BaseModel):
    """Server advances simulation time.

    Now includes per-tick candlestick data for one or more symbols.
    The server SHOULD populate the `candles` field on every tick.
    """

    sim_time: datetime
    sequence_id: int

    # New fields for candlestick delivery
    timeframe: Timeframe | None = Field(
        default=None, description="Timeframe of the emitted candles (e.g., 1min, 5min)"
    )
    candles: dict[str, PriceCandle] | None = Field(
        default=None,
        description="Mapping of symbol -> OHLCV candle for this tick",
    )

    # Optional extras
    market_session: Literal["pre_market", "regular", "after_hours"] | None = None
    symbols_trading: list[str] | None = None
    is_eod: bool = False


class TickAckData(BaseModel):
    """Client acknowledges tick and signals readiness."""

    sequence_id: int
    processing_status: Literal["ready", "processing", "need_time"]
    orders_pending: int = 0
    max_wait_ms: int = 1000


# ===== ORDER MANAGEMENT =====


class WSOrderType(str, Enum):
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"
    STOP_LIMIT = "stop_limit"


class OrderData(BaseModel):
    """Individual order within a batch."""

    order_id: str
    symbol: str
    side: OrderSide
    type: WSOrderType
    quantity: int = Field(gt=0)
    price: Decimal | None = None  # Limit price (for limit/stop_limit)
    stop_loss: Decimal | None = None
    take_profit: Decimal | None = None
    time_in_force: Literal["day", "gtc", "ioc"] = "day"


class OrderBatchData(BaseModel):
    """Client submits batch of orders."""

    batch_id: str
    orders: list[OrderData]
    execution_mode: Literal["atomic", "best_effort"] = "best_effort"
    parent_strategy: str | None = None


class BatchAckData(BaseModel):
    """Server acknowledges order batch."""

    batch_id: str
    accepted_orders: list[str]
    rejected_orders: dict[str, str]
    estimated_fills: dict[str, Decimal]


class ExecutionReportData(BaseModel):
    """Server reports order execution."""

    execution_id: str
    order_id: str
    symbol: str
    executed_quantity: int
    executed_price: Decimal
    commission: Decimal
    slippage_bps: int
    timestamp: datetime | None = None


# ===== ACCOUNT & PORTFOLIO =====


class PositionData(BaseModel):
    symbol: str
    quantity: int
    avg_cost: Decimal


class AccountSnapshotData(BaseModel):
    cash: Decimal
    equity: Decimal
    positions: list[PositionData]
    # Optional extras
    buying_power: Decimal | None = None
    day_pnl: Decimal | None = None
    open_orders: list[str] | None = None


# ===== ERROR HANDLING =====




def build_error(
    code: WSErrorCode | str,
    message: str,
    details: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a standardized error payload for WSMessage.data.

    This preserves the existing public shape used by the server:
    {"error_code": "...", "message": "...", "details": {...}}
    """

    payload: dict[str, Any] = {"error_code": str(code), "message": message}
    if details:
        payload["details"] = details
    return payload

class ErrorData(BaseModel):
    error_code: str
    message: str
    error_type: Literal["validation", "execution", "connection", "data", "rate_limit"]
    severity: Literal["warning", "error", "fatal"]
    recoverable: bool
    details: dict[str, Any] | None = None


# ===== SIMULATION COMPLETION =====


class SimulationEndData(BaseModel):
    session_id: str
    final_equity: Decimal
    total_trades: int
    sharpe_ratio: Decimal | None = None
    # Optional extras
    total_return_pct: Decimal | None = None
    win_rate: Decimal | None = None
    max_drawdown_pct: Decimal | None = None
    simulation_duration_sec: int | None = None
