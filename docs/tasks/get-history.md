# Get History

Retrieve historical orders and deals from the trade history.

---

## Historical orders by date range

```python
from datetime import datetime, timezone

date_from = datetime(2024, 1, 1, tzinfo=timezone.utc)
date_to   = datetime(2024, 1, 31, tzinfo=timezone.utc)

res = mt5.history_orders_get(date_from, date_to)

if res.success:
    print(f"Orders: {len(res.data)}")
    for order in res.data[:3]:
        print(f"  #{order.ticket}  {order.symbol}  {order.volume_initial} lots  state={order.state.name}")
else:
    print(f"Error {res.error_code}: {res.error_message}")
```

```text
Orders: 15
  #123456  EURUSD  0.10 lots  state=FILLED
  #123457  GBPUSD  0.05 lots  state=CANCELED
  #123458  EURUSD  0.10 lots  state=FILLED
```

---

## Historical deals by date range

```python
res = mt5.history_deals_get(date_from, date_to)

if res.success:
    print(f"Deals: {len(res.data)}")
    for deal in res.data[:3]:
        print(
            f"  #{deal.ticket}  {deal.symbol}  "
            f"profit={deal.profit:.2f}  net={deal.net_profit:.2f}"
        )
```

```text
Deals: 30
  #789012  EURUSD  profit=50.00  net=49.50
  #789013  EURUSD  profit=-20.00  net=-20.50
  #789014  GBPUSD  profit=30.00  net=29.50
```

---

## Filter by position ticket

```python
# All orders that touched position #123456
res = mt5.history_orders_get(position=123456)

# All deals that touched position #123456
res = mt5.history_deals_get(position=123456)
```

---

## Filter by symbol group

```python
res = mt5.history_deals_get(
    date_from=date_from,
    date_to=date_to,
    group="*USD*",
)
```

---

## Count only

```python
res = mt5.history_orders_total(date_from, date_to)
if res.success:
    print(f"Total orders: {res.data}")

res = mt5.history_deals_total(date_from, date_to)
if res.success:
    print(f"Total deals: {res.data}")
```

---

## Deal fields

| Field | Description |
|---|---|
| `ticket` | Unique deal identifier |
| `symbol` | Trading instrument |
| `type` | `DealType` — BUY, SELL, BALANCE, COMMISSION, etc. |
| `entry` | `DealEntry` — IN (opened), OUT (closed), INOUT (reversed) |
| `volume` | Executed volume in lots |
| `price` | Execution price |
| `profit` | Gross profit/loss |
| `commission` | Commission charged |
| `swap` | Swap charged |
| `net_profit` | `profit + commission + swap - fee` (computed) |
| `is_entry` | `True` if this deal opened a position |
| `is_exit` | `True` if this deal closed a position |

---

## Summarise P&L for a period

```python
res = mt5.history_deals_get(date_from, date_to)

if res.success:
    trade_deals = [d for d in res.data if d.is_buy or d.is_sell]
    total_net = sum(d.net_profit for d in trade_deals)
    print(f"Net P&L: {total_net:.2f}")
```
