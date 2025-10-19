"""
Enums for the Trading Simulator API.
"""

from enum import Enum


class OrderType(str, Enum):
    """Order type enumeration."""

    MARKET = "MKT"
    LIMIT = "LMT"


class OrderSide(str, Enum):
    """Order side enumeration."""

    BUY = "buy"
    SELL = "sell"


class TradeResult(str, Enum):
    """Trade result enumeration."""

    TAKE_PROFIT = "tp"
    STOP_LOSS = "sl"
    TIMEOUT = "timeout"


class SessionState(str, Enum):
    """Session state enumeration for simulation sessions."""

    INITIALIZING = "initializing"
    READY = "ready"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    ERROR = "error"



class WSErrorCode(str, Enum):
    """Standard WebSocket error codes shared across client and server.

    Keep values aligned with server error_code strings to avoid breaking API.
    """

    INVALID_PARAMS = "INVALID_PARAMS"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    SERVICE_BUSY = "SERVICE_BUSY"
    SESSION_CREATE_FAILED = "SESSION_CREATE_FAILED"
    NOT_IMPLEMENTED = "NOT_IMPLEMENTED"
    UNKNOWN_TYPE = "UNKNOWN_TYPE"
    AUTH_FAILED = "AUTH_FAILED"
    RATE_LIMITED = "RATE_LIMITED"
    HANDLER_TIMEOUT = "HANDLER_TIMEOUT"
