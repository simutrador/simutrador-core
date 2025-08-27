"""
SimuTrador Core Models

Shared Pydantic models used across all SimuTrador components.
"""

# Price data models
# Asset types
from .asset_types import (
    ASSET_TYPE_CONFIGS,
    LONDON_FOREX_SESSION,
    US_EQUITY_SESSION,
    AssetType,
    AssetTypeConfig,
    MarketSession,
    get_asset_config,
    get_resampling_offset,
    is_24_7_market,
    should_use_session_alignment,
)

# Enums
from .enums import (
    OrderSide,
    OrderType,
    TradeResult,
)
from .price_data import (
    DataUpdateStatus,
    PaginationInfo,
    PriceCandle,
    PriceDataSeries,
    PriceQuote,
    Timeframe,
)

# WebSocket communication models
from .websocket import (
    AccountSnapshotData,
    BatchAckData,
    ConnectionClosingData,
    ConnectionReadyData,
    ConnectionWarningData,
    CreateSessionData,
    ErrorData,
    ExecutionReportData,
    HealthStatus,
    OrderBatchData,
    OrderData,
    PositionData,
    SessionCreatedData,
    SimulationEndData,
    SimulationStartData,
    SimulationStartedData,
    TickAckData,
    TickData,
    TokenRequest,
    TokenResponse,
    UserLimitsResponse,
    UserPlan,
    WSMessage,
)

__all__ = [
    # Price data
    "Timeframe",
    "PriceCandle",
    "PaginationInfo",
    "PriceDataSeries",
    "PriceQuote",
    "DataUpdateStatus",
    # Enums
    "OrderType",
    "OrderSide",
    "TradeResult",
    # Asset types
    "AssetType",
    "MarketSession",
    "AssetTypeConfig",
    "US_EQUITY_SESSION",
    "LONDON_FOREX_SESSION",
    "ASSET_TYPE_CONFIGS",
    "get_asset_config",
    "get_resampling_offset",
    "should_use_session_alignment",
    "is_24_7_market",
    # WebSocket models
    "WSMessage",
    "HealthStatus",
    # Authentication models
    "TokenRequest",
    "TokenResponse",
    "UserLimitsResponse",
    "UserPlan",
    # Connection models
    "ConnectionReadyData",
    "ConnectionWarningData",
    "ConnectionClosingData",
    # Session models
    "CreateSessionData",
    "SessionCreatedData",
    "SimulationStartData",
    "SimulationStartedData",
    "TickData",
    "TickAckData",
    # Order models
    "OrderData",
    "OrderBatchData",
    "BatchAckData",
    "ExecutionReportData",
    # Portfolio models
    "PositionData",
    "AccountSnapshotData",
    # Error and completion models
    "ErrorData",
    "SimulationEndData",
]
