
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from simulations import (
    estimate_area,
    estimate_pi,
    simulate_game,
    simulate_traffic,
    simulate_stock_market,
)

app = FastAPI(
    title="Monte Carlo Simulation API",
    description="Backend for the Monte Carlo Simulation Lab",
    version="1.0.0",
)

# Allow your local Bolt/Vite website to call this API.
# Restrict origins to your actual website when deploying.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


# --------------------------------------------------
# INPUT MODELS
# --------------------------------------------------


class AreaInput(BaseModel):
    n: int = Field(default=10000, ge=100, le=1_000_000)
    a: float = 0.0
    b: float = 1.0
    curve: str = Field(default="x2", pattern="^(x2|x3|sin)$")
    seed: int | None = None

class PiInput(BaseModel):
    points: int = Field(default=10000, ge=100, le=1_000_000)
    seed: int | None = None


class GameInput(BaseModel):
    games: int = Field(default=10000, ge=1, le=100_000)
    rounds: int = Field(default=10, ge=1, le=100)
    seed: int | None = None


class TrafficInput(BaseModel):
    rate: float = Field(default=3.0, ge=0, le=10)
    threshold: int = Field(default=5, ge=1, le=10)
    minutes: int = Field(default=1000, ge=1, le=100_000)
    seed: int | None = None


# --------------------------------------------------
# HOME / HEALTH CHECK
# --------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "Monte Carlo Simulation API is running",
        "modules": [
            "/simulate/area",
            "/simulate/pi",
            "/simulate/game",
            "/simulate/traffic",
        ],
    }


# --------------------------------------------------
# MODULE 1: AREA UNDER A CURVE
# --------------------------------------------------


@app.post("/simulate/area")
def run_area(data: AreaInput):
    if data.a != 0.0 or data.b != 1.0:
        raise HTTPException(
            status_code=400,
            detail="This simulation currently supports only a=0 and b=1."
        )

    try:
        result = estimate_area(
            points=data.n,
            curve=data.curve,
            seed=data.seed,
        )
        return result
    except ValueError as error:
        raise HTTPException(
            status_code=400, detail=str(error)
        ) from error
    except Exception as error:
        print("Area simulation traceback:", repr(error))
        raise HTTPException(
            status_code=500,
            detail="Area simulation failed. Check the backend terminal."
        ) from error


# --------------------------------------------------
# MODULE 2: ESTIMATION OF PI
# --------------------------------------------------

@app.post("/simulate/pi")
def run_pi(data: PiInput):
    try:
        return estimate_pi(
            points=data.points,
            seed=data.seed,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=400, detail=str(error)
        ) from error
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail="Pi simulation failed",
        ) from error


# --------------------------------------------------
# MODULE 3: PROBABILITY GAME
# --------------------------------------------------

@app.post("/simulate/game")
def run_game(data: GameInput):
    try:
        return simulate_game(
            games=data.games,
            rounds=data.rounds,
            seed=data.seed,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=400, detail=str(error)
        ) from error
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail="Probability game simulation failed",
        ) from error


# --------------------------------------------------
# MODULE 4: TRAFFIC SIMULATION
# --------------------------------------------------

@app.post("/simulate/traffic")
def run_traffic(data: TrafficInput):
    try:
        return simulate_traffic(
            rate=data.rate,
            threshold=data.threshold,
            minutes=data.minutes,
            seed=data.seed,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=400, detail=str(error)
        ) from error
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail="Traffic simulation failed",
        ) from error

# ============================================================
# MODULE 5: STOCK MARKET SIMULATION API
# ============================================================

class StockInput(BaseModel):
    initial_price: float = Field(default=100.0, gt=0)
    annual_return: float = Field(default=0.08, ge=-1, le=1)
    annual_volatility: float = Field(default=0.20, ge=0, le=2)
    days: int = Field(default=252, ge=1, le=2520)
    simulations: int = Field(default=1000, ge=1, le=10000)
    seed: int | None = None


@app.post("/simulate/stock")
def run_stock(data: StockInput):
    try:
        return simulate_stock_market(
            initial_price=data.initial_price,
            annual_return=data.annual_return,
            annual_volatility=data.annual_volatility,
            days=data.days,
            simulations=data.simulations,
            seed=data.seed,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error
    except Exception as error:
        print("Stock simulation error:", repr(error))
        raise HTTPException(
            status_code=500,
            detail="Stock market simulation failed.",
        ) from error
