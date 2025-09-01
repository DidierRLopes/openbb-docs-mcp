from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from functools import wraps
import asyncio
import json
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import yfinance as yf
from datetime import datetime, timedelta
from typing import Optional

WIDGETS = {}

def register_widget(widget_config):
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            return await func(*args, **kwargs)
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        
        endpoint = widget_config.get("endpoint")
        if endpoint:
            if "widgetId" not in widget_config:
                widget_config["widgetId"] = endpoint
            widget_id = widget_config["widgetId"]
            WIDGETS[widget_id] = widget_config

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper
    return decorator

app = FastAPI(
    title="Monte Carlo Simulation Widget",
    description="OpenBB widget for Monte Carlo stock price simulation",
    version="0.0.1"
)

origins = [
    "https://pro.openbb.co",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Info": "Monte Carlo Simulation Widget"}

@app.get("/widgets.json")
def get_widgets():
    return WIDGETS

def monte_carlo_simulation(ticker: str, start_date: str, use_volatility_adjustment: bool, num_simulations: int = 1000, num_days: int = 252):
    try:
        stock = yf.Ticker(ticker)
        end_date = datetime.now().strftime('%Y-%m-%d')
        hist_data = stock.history(start=start_date, end=end_date)
        
        if hist_data.empty:
            return None, "No data available for the specified ticker and date range"
        
        daily_returns = hist_data['Close'].pct_change().dropna()
        
        if use_volatility_adjustment:
            mean_return = daily_returns.mean() * 0.8
            volatility = daily_returns.std() * 1.2
        else:
            mean_return = daily_returns.mean()
            volatility = daily_returns.std()
        
        last_price = hist_data['Close'].iloc[-1]
        
        simulation_results = []
        for _ in range(num_simulations):
            prices = [last_price]
            for _ in range(num_days):
                random_return = np.random.normal(mean_return, volatility)
                new_price = prices[-1] * (1 + random_return)
                prices.append(new_price)
            simulation_results.append(prices)
        
        return simulation_results, None
    except Exception as e:
        return None, str(e)

@register_widget({
    "widgetId": "monte_carlo_simulation",
    "name": "Monte Carlo Stock Simulation",
    "description": "Monte Carlo simulation for stock price forecasting",
    "category": "Finance",
    "subCategory": "Analysis",
    "type": "chart",
    "endpoint": "/monte_carlo_simulation",
    "gridData": {"w": 40, "h": 15},
    "runButton": True,
    "raw": True,
    "params": [
        {
            "paramName": "ticker",
            "label": "Stock Ticker",
            "type": "text",
            "description": "Stock symbol (e.g., AAPL, MSFT)",
            "value": "AAPL",
            "show": True
        },
        {
            "paramName": "start_date",
            "label": "Start Date",
            "type": "date", 
            "description": "Historical data start date",
            "value": "2023-01-01",
            "show": True
        },
        {
            "paramName": "use_volatility_adjustment",
            "label": "Volatility Adjustment",
            "type": "boolean",
            "description": "Apply volatility adjustment to simulation",
            "value": False,
            "show": True
        }
    ]
})
@app.get("/monte_carlo_simulation")
async def monte_carlo_endpoint(
    ticker: str = "AAPL",
    start_date: str = "2023-01-01", 
    use_volatility_adjustment: bool = False,
    raw: bool = False,
    theme: str = "dark"
):
    simulation_results, error = monte_carlo_simulation(ticker, start_date, use_volatility_adjustment)
    
    if error:
        return {"error": error}
    
    if raw:
        return simulation_results
    
    days = list(range(len(simulation_results[0])))
    
    fig = go.Figure()
    
    for i, simulation in enumerate(simulation_results[:50]):
        fig.add_trace(go.Scatter(
            x=days,
            y=simulation,
            mode='lines',
            line=dict(width=1, color='rgba(100, 150, 200, 0.1)'),
            showlegend=False,
            hoverinfo='skip'
        ))
    
    percentiles = np.array([np.percentile([sim[day] for sim in simulation_results], [5, 25, 50, 75, 95]) 
                           for day in range(len(simulation_results[0]))])
    
    fig.add_trace(go.Scatter(
        x=days, y=percentiles[:, 2],
        mode='lines', name='Median (50th)',
        line=dict(color='red', width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=days, y=percentiles[:, 0],
        mode='lines', name='5th Percentile',
        line=dict(color='blue', width=2, dash='dash')
    ))
    
    fig.add_trace(go.Scatter(
        x=days, y=percentiles[:, 4],
        mode='lines', name='95th Percentile', 
        line=dict(color='blue', width=2, dash='dash'),
        fill='tonexty', fillcolor='rgba(0, 100, 200, 0.1)'
    ))
    
    fig.update_layout(
        title=f"Monte Carlo Simulation for {ticker.upper()}",
        xaxis_title="Days",
        yaxis_title="Price ($)",
        template="plotly_white",
        height=500
    )
    
    return json.loads(fig.to_json())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)