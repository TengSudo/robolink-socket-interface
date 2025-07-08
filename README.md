# robolink-socket-comm

A simple Python client to connect and communicate with Robolink RL-DCi robots over TCP using the CRI protocol.

## ⚙️ Features

- Connects to robot via TCP (default: 192.168.3.11:3920)
- Sends `ALIVEJOG` messages periodically
- Queries robot version (`GetVersion`)
- Reconnects automatically on failure
- Clean shutdown on exit

## 📦 Requirements

- Python 3.7+
- No external libraries required (uses `socket`, `time`)

## 🚀 Usage

```bash
python connect.py
