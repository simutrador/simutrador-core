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
    OrderBatchData,
    OrderData,
    PositionData,
    SessionCreatedData,
    SimulationEndData,
    SimulationStartData,
    SimulationStartedData,
    TickAckData,
    TickData,
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
    "ConnectionReadyData",
    "ConnectionWarningData",
    "ConnectionClosingData",
    "CreateSessionData",
    "SessionCreatedData",
    "SimulationStartData",
    "SimulationStartedData",
    "TickData",
    "TickAckData",
    "OrderData",
    "OrderBatchData",
    "BatchAckData",
    "ExecutionReportData",
    "PositionData",
    "AccountSnapshotData",
    "ErrorData",
    "SimulationEndData",
]
