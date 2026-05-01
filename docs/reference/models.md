# Models

All models are Pydantic v2 `BaseModel` subclasses. They validate on construction and provide IDE completion.

---

## Position

Returned by `mt5.positions()`.

```python
from syntiq_mt5 import Position
```

| Field | Type | Description |
|---|---|---|
| `ticket` | `int` | Unique position identifier |
| `symbol` | `str` | Trading instrument |
| `type` | `PositionType` | `BUY` or `SELL` |
| `volume` | `float` | Size in lots |
| `price_open` | `float` | Entry price |
| `price_current` | `float` | Current market price |
| `sl` | `float` | Stop loss (`0.0` = not set) |
| `tp` | `float` | Take profit (`0.0` = not set) |
| `profit` | `float` | Floating P&L in account currency |
| `swap` | `float` | Accumulated swap |
| `magic` | `int` | EA identifier (`0` = manual) |
| `comment` | `str` | Order comment |
| `time` | `int` | Open time (Unix seconds) |
| `digits` | `int` | Symbol decimal places |
| `point` | `float` | Symbol point size |

**Computed properties:**

| Property | Description |
|---|---|
| `is_buy` | `True` for long positions |
| `is_sell` | `True` for short positions |
| `pip_size` | Pip size in price units (handles 3/5-digit symbols) |
| `pips_profit` | Floating P&L in pips |
| `pips_to_tp` | Distance to take profit in pips (`0.0` if TP not set) |

---

## Candle

Returned by `mt5.get_candles()`, `copy_rates_from()`, `copy_rates_range()`.

```python
from syntiq_mt5 import Candle
```

| Field | Type | Description |
|---|---|---|
| `time` | `int` | Bar open time (Unix seconds) |
| `open` | `float` | Opening price |
| `high` | `float` | Highest price |
| `low` | `float` | Lowest price |
| `close` | `float` | Closing price |
| `tick_volume` | `int` | Number of price ticks |
| `spread` | `int` | Spread in points at bar open |
| `real_volume` | `int` | Traded volume (exchange only; 0 for Forex) |

---

## Tick

Returned by `mt5.copy_ticks_from()`, `copy_ticks_range()`.

```python
from syntiq_mt5 import Tick
```

| Field | Type | Description |
|---|---|---|
| `time` | `int` | Tick time (Unix seconds) |
| `time_msc` | `int` | Tick time (milliseconds) |
| `bid` | `float` | Bid price |
| `ask` | `float` | Ask price |
| `last` | `float` | Last trade price (exchange only) |
| `volume` | `int` | Last trade volume (exchange only) |
| `flags` | `int` | `TICK_FLAG_*` bitmask |
| `volume_real` | `float` | Fractional last trade volume |

**Computed properties:** `spread`, `mid_price`, `has_bid`, `has_ask`, `has_last`

---

## TradeRequest

Passed to `mt5.order_send()` and `mt5.order_check()`.

```python
from syntiq_mt5 import TradeRequest, constants

request = TradeRequest(
    action=constants.TRADE_ACTION_DEAL,
    symbol="EURUSD",
    volume=0.10,
    type=constants.ORDER_TYPE_BUY,
    price=1.08500,
    sl=1.08000,
    tp=1.09000,
    deviation=10,
)
```

| Field | Type | Default | Description |
|---|---|---|---|
| `action` | `TradeAction` | required | Trade action type |
| `symbol` | `str` | `""` | Instrument |
| `volume` | `float` | `0.0` | Lots |
| `type` | `OrderType` | `BUY` | Order type |
| `price` | `float` | `0.0` | Execution price |
| `sl` | `float` | `0.0` | Stop loss |
| `tp` | `float` | `0.0` | Take profit |
| `deviation` | `int` | `0` | Max price deviation in points |
| `type_filling` | `OrderFilling` | `FOK` | Fill policy |
| `type_time` | `OrderTime` | `GTC` | Expiry policy |
| `comment` | `str` | `""` | Comment |
| `position` | `int` | `0` | Position ticket (for `SLTP`) |
| `order` | `int` | `0` | Order ticket (for `MODIFY`/`REMOVE`) |
| `magic` | `int` | `0` | EA identifier |

---

## TradeResult

Returned by `mt5.order_send()` and `mt5.order_check()`.

```python
from syntiq_mt5 import TradeResult
```

| Field | Type | Description |
|---|---|---|
| `retcode` | `int` | MT5 return code |
| `deal` | `int` | Deal ticket (`0` if none) |
| `order` | `int` | Order ticket (`0` if none) |
| `volume` | `float` | Executed volume |
| `price` | `float` | Execution price |
| `bid` | `float` | Bid at execution time |
| `ask` | `float` | Ask at execution time |
| `comment` | `str` | Broker comment |

**Computed properties:**

| Property | Description |
|---|---|
| `is_successful` | `True` for retcodes 10008, 10009, 10010 |
| `is_rejected` | `True` for retcode 10006 |
| `requires_requote` | `True` for retcode 10004 |

---

## Deal

Returned by `mt5.history_deals_get()`.

```python
from syntiq_mt5 import Deal
```

| Field | Type | Description |
|---|---|---|
| `ticket` | `int` | Unique deal identifier |
| `symbol` | `str` | Instrument |
| `type` | `DealType` | BUY, SELL, BALANCE, COMMISSION, etc. |
| `entry` | `DealEntry` | IN, OUT, INOUT, OUT_BY |
| `volume` | `float` | Executed volume |
| `price` | `float` | Execution price |
| `profit` | `float` | Gross profit/loss |
| `commission` | `float` | Commission charged |
| `swap` | `float` | Swap charged |
| `fee` | `float` | Additional fee |
| `time` | `int` | Execution time (Unix seconds) |

**Computed properties:** `net_profit`, `is_entry`, `is_exit`, `is_reversal`, `is_close_by`, `is_buy`, `is_sell`

---

## AccountInfo

Returned by `mt5.account_info()`.

```python
from syntiq_mt5 import AccountInfo
```

| Field | Type | Description |
|---|---|---|
| `login` | `int` | Account number |
| `name` | `str` | Account holder name |
| `server` | `str` | Broker server |
| `currency` | `str` | Account currency |
| `leverage` | `int` | Leverage (e.g. `100` for 1:100) |
| `balance` | `float` | Account balance |
| `equity` | `float` | Balance + floating P&L |
| `margin` | `float` | Margin in use |
| `margin_free` | `float` | Available margin |
| `margin_level` | `float` | Equity / margin × 100 |
| `profit` | `float` | Total floating P&L |
| `trade_allowed` | `bool` | Trading enabled |

**Computed properties:** `margin_used_percent`, `equity_to_balance_ratio`

---

## LoginCredential

```python
from syntiq_mt5 import LoginCredential
from pydantic import SecretStr

creds = LoginCredential(
    login=12345678,
    password=SecretStr("your-password"),  # never logged or serialised
    server="Broker-Demo",
    path=None,  # optional: path to terminal64.exe
)
```

| Field | Type | Description |
|---|---|---|
| `login` | `int` | MT5 account number |
| `password` | `SecretStr` | Account password (masked in logs) |
| `server` | `str` | Broker server name |
| `path` | `str \| None` | Path to `terminal64.exe` (optional) |

---

## Result[T]

Returned by every client method. See [Result\[T\]](../core/results.md) for full documentation.

```python
from syntiq_mt5 import Result
```

| Field | Type | Description |
|---|---|---|
| `success` | `bool` | `True` if operation succeeded |
| `data` | `T \| None` | Return value (set on success) |
| `error_code` | `int \| None` | MT5 error code (set on failure) |
| `error_message` | `str \| None` | Error description (set on failure) |
| `context` | `str \| None` | MT5 API function name |
| `operation` | `str \| None` | Logical operation name |
