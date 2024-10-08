# event-shop

## How to get started

1. Install docker, docker compose, make

2. Create .env file in repo dir with TOKEN (telegram bot token) and OWNER (user with admin powers id)

```bash
TOKEN=123456:ABCDEF
OWNER=1234567890
```

1. Start all

```bash
make up
```

## Other make commands

Stop all

```bash
make down
```

Get logs

```bash
make logs
```

Delete all data

```bash
make flush
```

---

how to use monitor (bash):

export MONITOR_TOKEN=ABCDEF:123456
export MONITOR_CHAT=1234567890
pip install aiogram
python3 monitor/main.py
