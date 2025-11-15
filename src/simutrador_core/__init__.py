"""
SimuTrador Core Library

Shared models, utilities, and interfaces for the SimuTrador trading simulation platform.

This library provides:
- Pydantic models for price data, orders, and WebSocket communication
- Enums for order types, sides, and asset classifications
- Utility functions for timeframe conversion, validation, and logging
- Abstract interfaces for data providers and storage systems
"""

__version__ = "1.0.19"

# Re-export commonly used models and utilities
from simutrador_core.models import (
    AccountSnapshotData,
    # Asset classification
    AssetType,
    ExecutionReportData,
    HealthStatus,
    OrderBatchData,
    OrderData,
    OrderSide,
    # Trading models
    OrderType,
    # Core data models
    PriceCandle,
    PriceDataSeries,
    TickAckData,
    TickData,
    Timeframe,
    # WebSocket communication
    WSMessage,
    get_asset_config,
    get_resampling_offset,
)
from simutrador_core.utils import (
    # Logging utilities
    configure_third_party_loggers,
    get_default_logger,
    # Timeframe utilities
    get_pandas_frequency,
    get_resampling_rules,
    get_supported_timeframes,
    get_timeframe_minutes,
    setup_logger,
    validate_timeframe_conversion,
)

__all__ = [
    "__version__",
    # Core data models
    "PriceCandle",
    "Timeframe",
    "PriceDataSeries",
    # Trading models
    "OrderType",
    "OrderSide",
    "OrderData",
    "OrderBatchData",
    # WebSocket communication
    "WSMessage",
    "HealthStatus",
    "TickData",
    "TickAckData",
    "ExecutionReportData",
    "AccountSnapshotData",
    # Asset classification
    "AssetType",
    "get_asset_config",
    "get_resampling_offset",
    # Timeframe utilities
    "get_timeframe_minutes",
    "get_pandas_frequency",
    "validate_timeframe_conversion",
    "get_supported_timeframes",
    "get_resampling_rules",
    # Logging utilities
    "setup_logger",
    "get_default_logger",
    "configure_third_party_loggers",
]
