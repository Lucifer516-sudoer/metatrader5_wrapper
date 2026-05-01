# Constants

All MT5 constants are available through `syntiq_mt5.constants`. Never use raw integers.

```python
from syntiq_mt5 import constants
```

---

## Trade Actions

Used in `TradeRequest.action`.

| Constant | Value | Description |
|---|---|---|
| `TRADE_ACTION_DEAL` | 1 | Market order — execute immediately |
| `TRADE_ACTION_PENDING` | 5 | Place a pending order |
| `TRADE_ACTION_SLTP` | 6 | Modify SL/TP on an open position |
| `TRADE_ACTION_MODIFY` | 7 | Modify a pending order |
| `TRADE_ACTION_REMOVE` | 8 | Delete a pending order |
| `TRADE_ACTION_CLOSE_BY` | 10 | Close a position by an opposite one |

---

## Order Types

Used in `TradeRequest.type`.

| Constant | Value | Description |
|---|---|---|
| `ORDER_TYPE_BUY` | 0 | Market buy |
| `ORDER_TYPE_SELL` | 1 | Market sell |
| `ORDER_TYPE_BUY_LIMIT` | 2 | Buy limit (pending) |
| `ORDER_TYPE_SELL_LIMIT` | 3 | Sell limit (pending) |
| `ORDER_TYPE_BUY_STOP` | 4 | Buy stop (pending) |
| `ORDER_TYPE_SELL_STOP` | 5 | Sell stop (pending) |
| `ORDER_TYPE_BUY_STOP_LIMIT` | 6 | Buy stop-limit (pending) |
| `ORDER_TYPE_SELL_STOP_LIMIT` | 7 | Sell stop-limit (pending) |
| `ORDER_TYPE_CLOSE_BY` | 8 | Close by opposite position |

---

## Order Filling

Used in `TradeRequest.type_filling`.

| Constant | Value | Description |
|---|---|---|
| `ORDER_FILLING_FOK` | 0 | Fill or Kill — execute fully or cancel |
| `ORDER_FILLING_IOC` | 1 | Immediate or Cancel — fill available, cancel rest |
| `ORDER_FILLING_RETURN` | 2 | Return remainder as a new order |
| `ORDER_FILLING_BOC` | 3 | Book or Cancel — passive fill only |

---

## Order Time

Used in `TradeRequest.type_time`.

| Constant | Value | Description |
|---|---|---|
| `ORDER_TIME_GTC` | 0 | Good Till Cancelled |
| `ORDER_TIME_DAY` | 1 | Good Till End of Day |
| `ORDER_TIME_SPECIFIED` | 2 | Good Till specified datetime |
| `ORDER_TIME_SPECIFIED_DAY` | 3 | Good Till specified day (23:59:59) |

---

## Position Types

| Constant | Value | Description |
|---|---|---|
| `POSITION_TYPE_BUY` | 0 | Long position |
| `POSITION_TYPE_SELL` | 1 | Short position |

---

## Timeframes

Used in `get_candles()`, `copy_rates_from()`, `copy_rates_range()`.

### Minutes

| Constant | Period |
|---|---|
| `TIMEFRAME_M1` | 1 min |
| `TIMEFRAME_M2` | 2 min |
| `TIMEFRAME_M3` | 3 min |
| `TIMEFRAME_M4` | 4 min |
| `TIMEFRAME_M5` | 5 min |
| `TIMEFRAME_M6` | 6 min |
| `TIMEFRAME_M10` | 10 min |
| `TIMEFRAME_M12` | 12 min |
| `TIMEFRAME_M15` | 15 min |
| `TIMEFRAME_M20` | 20 min |
| `TIMEFRAME_M30` | 30 min |

### Hours

| Constant | Period |
|---|---|
| `TIMEFRAME_H1` | 1 hour |
| `TIMEFRAME_H2` | 2 hours |
| `TIMEFRAME_H3` | 3 hours |
| `TIMEFRAME_H4` | 4 hours |
| `TIMEFRAME_H6` | 6 hours |
| `TIMEFRAME_H8` | 8 hours |
| `TIMEFRAME_H12` | 12 hours |

### Days and longer

| Constant | Period |
|---|---|
| `TIMEFRAME_D1` | 1 day |
| `TIMEFRAME_W1` | 1 week |
| `TIMEFRAME_MN1` | 1 month |

**Example:**

```python
res = mt5.get_candles("EURUSD", timeframe=constants.TIMEFRAME_H4, count=100)
```

---

## Copy Ticks Flags

Used in `copy_ticks_from()` and `copy_ticks_range()`.

| Constant | Value | Description |
|---|---|---|
| `COPY_TICKS_ALL` | 6 | All ticks |
| `COPY_TICKS_INFO` | 2 | Bid/ask changes only |
| `COPY_TICKS_TRADE` | 4 | Last price and volume changes only |

---

## Tick Flags

Bitmask values in `Tick.flags` indicating what changed.

| Constant | Value | Description |
|---|---|---|
| `TICK_FLAG_BID` | 2 | Bid price changed |
| `TICK_FLAG_ASK` | 4 | Ask price changed |
| `TICK_FLAG_LAST` | 8 | Last price changed |
| `TICK_FLAG_VOLUME` | 16 | Volume changed |
| `TICK_FLAG_BUY` | 32 | Last deal was a buy |
| `TICK_FLAG_SELL` | 64 | Last deal was a sell |

---

## Trade Return Codes

Returned in `TradeResult.retcode` after `order_send()` or `order_check()`.

### Success

| Constant | Value | Description |
|---|---|---|
| `TRADE_RETCODE_PLACED` | 10008 | Pending order placed |
| `TRADE_RETCODE_DONE` | 10009 | Request completed |
| `TRADE_RETCODE_DONE_PARTIAL` | 10010 | Request partially completed |

`TradeResult.is_successful` returns `True` for all three.

### Rejection / error

| Constant | Value | Description |
|---|---|---|
| `TRADE_RETCODE_REQUOTE` | 10004 | Price changed — requote required |
| `TRADE_RETCODE_REJECT` | 10006 | Request rejected |
| `TRADE_RETCODE_CANCEL` | 10007 | Cancelled by trader |
| `TRADE_RETCODE_ERROR` | 10011 | Processing error |
| `TRADE_RETCODE_TIMEOUT` | 10012 | Request timed out |
| `TRADE_RETCODE_INVALID` | 10013 | Invalid request |
| `TRADE_RETCODE_INVALID_VOLUME` | 10014 | Invalid volume |
| `TRADE_RETCODE_INVALID_PRICE` | 10015 | Invalid price |
| `TRADE_RETCODE_INVALID_STOPS` | 10016 | Invalid SL/TP |
| `TRADE_RETCODE_TRADE_DISABLED` | 10017 | Trading disabled |
| `TRADE_RETCODE_MARKET_CLOSED` | 10018 | Market closed |
| `TRADE_RETCODE_NO_MONEY` | 10019 | Insufficient funds |
| `TRADE_RETCODE_PRICE_CHANGED` | 10020 | Price changed |
| `TRADE_RETCODE_PRICE_OFF` | 10021 | No quotes |
| `TRADE_RETCODE_INVALID_EXPIRATION` | 10022 | Invalid expiration |
| `TRADE_RETCODE_ORDER_CHANGED` | 10023 | Order state changed |
| `TRADE_RETCODE_TOO_MANY_REQUESTS` | 10024 | Too many requests |
| `TRADE_RETCODE_NO_CHANGES` | 10025 | No changes in request |
| `TRADE_RETCODE_SERVER_DISABLES_AT` | 10026 | Autotrading disabled by server |
| `TRADE_RETCODE_CLIENT_DISABLES_AT` | 10027 | Autotrading disabled by client |
| `TRADE_RETCODE_LOCKED` | 10028 | Request locked |
| `TRADE_RETCODE_FROZEN` | 10029 | Order/position frozen |
| `TRADE_RETCODE_INVALID_FILL` | 10030 | Invalid fill type |
| `TRADE_RETCODE_CONNECTION` | 10031 | No connection |
| `TRADE_RETCODE_ONLY_REAL` | 10032 | Real accounts only |
| `TRADE_RETCODE_LIMIT_ORDERS` | 10033 | Order limit reached |
| `TRADE_RETCODE_LIMIT_VOLUME` | 10034 | Volume limit reached |
| `TRADE_RETCODE_INVALID_ORDER` | 10035 | Invalid order type |
| `TRADE_RETCODE_POSITION_CLOSED` | 10036 | Position already closed |

**Example:**

```python
res = mt5.order_send(request)
if res.success and not res.data.is_successful:
    if res.data.retcode == constants.TRADE_RETCODE_NO_MONEY:
        print("Insufficient funds")
    elif res.data.retcode == constants.TRADE_RETCODE_REQUOTE:
        print(f"Requote — new price: {res.data.ask}")
```
