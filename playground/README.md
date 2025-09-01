# Monte Carlo Stock Simulation Widget

A self-contained OpenBB widget that performs Monte Carlo simulations for stock price forecasting.

## Features

- **3 Parameters:**
  - `ticker` (text): Stock symbol (e.g., AAPL, MSFT)
  - `start_date` (date): Historical data start date for analysis
  - `use_volatility_adjustment` (boolean): Apply volatility adjustment to simulation

- **Dual Output Modes:**
  - **Chart Mode** (default): Interactive Plotly visualization showing simulation paths and percentiles
  - **Raw Data Mode**: Pure simulation data arrays (1000 simulations × 253 days each)

- **Run Button**: Manual execution control for Monte Carlo simulations

## Installation & Setup

1. **Install dependencies with uv:**
   ```bash
   cd playground
   uv sync
   ```

2. **Run the widget server:**
   ```bash
   uv run python main.py
   ```

3. **Access the widget:**
   - Server runs on `http://localhost:8000`
   - Widget configuration: `http://localhost:8000/widgets.json`
   - Widget endpoint: `http://localhost:8000/monte_carlo_simulation`

## Usage

### Chart Mode (Default)
```
GET /monte_carlo_simulation?ticker=AAPL&start_date=2023-01-01&use_volatility_adjustment=false
```

### Raw Data Mode
```
GET /monte_carlo_simulation?ticker=AAPL&start_date=2023-01-01&use_volatility_adjustment=false&raw=true
```

## Widget Configuration

The widget is automatically registered with OpenBB Workspace and includes:
- Type: chart (plotly)
- Grid size: 40×15
- Run button enabled
- Raw data toggle enabled
- Category: Finance/Analysis
- All parameters configurable in UI

## Monte Carlo Simulation Details

- Fetches historical stock data using yfinance
- Calculates daily returns and volatility
- Runs 1000 simulations over 252 trading days (1 year)
- Volatility adjustment reduces mean return by 20% and increases volatility by 20%
- Chart shows 50 simulation paths plus 5th, 25th, 50th, 75th, and 95th percentiles
- Raw data returns pure simulation arrays (1000 simulations × 253 price points each)
