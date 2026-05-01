# Market Book

Subscribe to and read Level 2 (Depth of Market) order book data.

---

## Subscribe, read, release

```python
# 1. Subscribe
add = mt5.market_book_add("EURUSD")
if not add.success or not add.data:
    print("Market book not available for this symbol")
else:
    # 2. Read the current snapshot
    res = mt5.market_book_get("EURUSD")
    if res.success:
        print(f"Book entries: {len(res.data)}")
        for entry in res.data:
            side = "BUY " if entry.is_buy else "SELL"
            kind = "market" if entry.is_market else "limit "
            print(f"  {side} {kind}  {entry.price:.5f}  {entry.volume_real} lots")

    # 3. Release when done
    mt5.market_book_release("EURUSD")
```

```text
Book entries: 10
  SELL limit   1.08480  2.50 lots
  SELL limit   1.08475  1.00 lots
  SELL limit   1.08470  3.00 lots
  BUY  limit   1.08455  1.50 lots
  BUY  limit   1.08450  2.00 lots
```

---

## BookEntry fields

| Field | Type | Description |
|---|---|---|
| `type` | `BookType` | `SELL`, `BUY`, `SELL_MARKET`, `BUY_MARKET` |
| `price` | `float` | Price level |
| `volume` | `int` | Volume at this level (integer lots) |
| `volume_real` | `float` | Volume at this level (fractional lots) |
| `is_buy` | `bool` | `True` for buy-side entries |
| `is_sell` | `bool` | `True` for sell-side entries |
| `is_market` | `bool` | `True` for market orders (vs limit orders) |

---

## Separate bids and asks

```python
res = mt5.market_book_get("EURUSD")

if res.success:
    bids = [e for e in res.data if e.is_buy]
    asks = [e for e in res.data if e.is_sell]

    best_bid = max(bids, key=lambda e: e.price, default=None)
    best_ask = min(asks, key=lambda e: e.price, default=None)

    if best_bid and best_ask:
        print(f"Best bid: {best_bid.price}  Best ask: {best_ask.price}")
```

---

!!! note
    Market book data is not available for all symbols or brokers. `market_book_add()` returns `data=False` when the symbol does not support DOM. Always check `add.data` before calling `market_book_get()`.
