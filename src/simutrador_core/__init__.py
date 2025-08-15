"""
SimuTrador Core Library

Shared models, utilities, and interfaces for the SimuTrador trading simulation platform.

This library provides:
- Pydantic models for price data, orders, and WebSocket communication
- Enums for order types, sides, and asset classifications
- Utility functions for timeframe conversion and validation
- Abstract interfaces for data providers and storage systems
"""

__version__ = "1.0.0"

# Re-export commonly used models and utilities
from .models import (
    AccountSnapshotData,
    # Asset classification
    AssetType,
    ExecutionReportData,
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
    "TickData",
    "TickAckData",
    "ExecutionReportData",
    "AccountSnapshotData",
    # Asset classification
    "AssetType",
    "get_asset_config",
    "get_resampling_offset",
]
