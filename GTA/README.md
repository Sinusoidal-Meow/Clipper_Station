# GTA ClipForge

Gaming stream clip operations tool.

## Quick Start

```powershell
# Create virtual environment
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

# Start dashboard
.\.venv\Scripts\python.exe -m clipforge serve

# Open http://127.0.0.1:8800
```

## Available Commands

- `serve` - Start the dashboard server
- `run URL --brand gta --clips 5` - Process a VOD
- `connect youtube --brand gta` - Connect YouTube OAuth
- `gen-key` - Generate encryption key
- `list` - List clips for a brand
- `gatt` - Show API commands

## Ports

- Dashboard: http://127.0.0.1:8800
- Status: 8800