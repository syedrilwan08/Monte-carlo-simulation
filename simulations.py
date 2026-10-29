import math
import random


def _percentage_error(estimate, exact_value):
    """Return percentage error, safely handling a zero reference value."""
    if exact_value == 0:
        return 0.0 if estimate == 0 else None
    return abs(estimate - exact_value) / abs(exact_value) * 100


# MODULE 1: AREA UNDER A CURVE
def estimate_area(points=10000, curve="x2", seed=None):
    if not 100 <= points <= 1_000_000:
        raise ValueError("Points must be between 100 and 1,000,000.")
    if curve not in ("x2", "x3", "sin"):
        raise ValueError("Curve must be x2, x3, or sin.")

    rng = random.Random(seed)
    below = 0
    sample_x, sample_y, sample_inside, convergence = [], [], [], []
    interval = max(1, points // 500)

    if curve == "x2":
        exact_area, curve_label = 1 / 3, "y = x^2"
    elif curve == "x3":
        exact_area, curve_label = 1 / 4, "y = x^3"
    else:
        exact_area, curve_label = 2 / math.pi, "y = sin(pi*x/2)"

    for i in range(points):
        x, y = rng.random(), rng.random()
        fx = x ** 2 if curve == "x2" else x ** 3 if curve == "x3" else math.sin(math.pi * x / 2)
        inside = y <= fx
        if inside:
            below += 1
        if i < min(points, 2000):
            sample_x.append(x)
            sample_y.append(y)
            sample_inside.append(inside)
        if (i + 1) % interval == 0 or i == points - 1:
            convergence.append({"samples": i + 1, "estimate": below / (i + 1)})

    estimate = below / points
    return {
        "module": "Area Under a Curve",
        "curve": curve,
        "curve_label": curve_label,
        "samples": points,
        "points_below": below,
        "estimate": estimate,
        "exact_area": exact_area,
        "absolute_error": abs(estimate - exact_area),
        "percentage_error": _percentage_error(estimate, exact_area),
        "sample_x": sample_x,
        "sample_y": sample_y,
        "sample_inside": sample_inside,
        "convergence": convergence,
    }


# MODULE 2: ESTIMATION OF PI
def estimate_pi(points=10000, seed=None):
    if not 100 <= points <= 1_000_000:
        raise ValueError("Points must be between 100 and 1,000,000.")
    rng = random.Random(seed)
    inside = 0
    sample_x, sample_y, sample_inside, running_estimates = [], [], [], []
    interval = max(1, points // 500)

    for i in range(points):
        x, y = rng.random(), rng.random()
        is_inside = x * x + y * y <= 1
        if is_inside:
            inside += 1
        if i < min(points, 2000):
            sample_x.append(x)
            sample_y.append(y)
            sample_inside.append(is_inside)
        if (i + 1) % interval == 0 or i == points - 1:
            running_estimates.append(4 * inside / (i + 1))

    estimate = 4 * inside / points
    return {
        "module": "Estimation of Pi",
        "samples": points,
        "inside_points": inside,
        "estimate": estimate,
        "reference_pi": math.pi,
        "absolute_error": abs(estimate - math.pi),
        "percentage_error": _percentage_error(estimate, math.pi),
        "sample_x": sample_x,
        "sample_y": sample_y,
        "sample_inside": sample_inside,
        "convergence": running_estimates,
        "convergence_samples": [
            min((i + 1) * interval, points) for i in range(len(running_estimates))
        ],
    }

# MODULE 3: PROBABILITY GAME
def play_one_game(rounds=10, rng=None):
    if rng is None:
        rng = random.Random()
    score = 10
    for _ in range(rounds):
        die = rng.randint(1, 6)
        if die <= 2:
            score -= 2
        elif die <= 4:
            score += 1
        elif die == 5:
            score += 3
        else:
            score += 5
    return score
def simulate_game(games=10000, rounds=10, seed=None):
    if not 1 <= games <= 100_000:
        raise ValueError("Games must be between 1 and 100,000.")
    if not 1 <= rounds <= 100:
        raise ValueError("Rounds must be between 1 and 100.")

    rng = random.Random(seed)
    final_scores, running_probabilities = [], []
    successes = 0
    interval = max(1, games // 500)

    for i in range(games):
        score = play_one_game(rounds, rng)
        final_scores.append(score)
        if score > 10:
            successes += 1
        if (i + 1) % interval == 0 or i == games - 1:
            running_probabilities.append(successes / (i + 1))

    probability = successes / games
    score_counts = {}
    for score in final_scores:
        score_counts[score] = score_counts.get(score, 0) + 1
    sorted_scores = sorted(score_counts)
    failures = games - successes

    return {
        "module": "Probability Game",
        "games": games,
        "rounds": rounds,
        "starting_score": 10,
        "successful_games": successes,
        "failed_games": failures,
        "success_probability": probability,
        "success_percentage": probability * 100,
        "failure_probability": failures / games,
        "failure_percentage": failures / games * 100,
        "average_final_score": sum(final_scores) / games,
        "minimum_final_score": min(final_scores),
        "maximum_final_score": max(final_scores),
        "final_scores": final_scores,
        "score_values": sorted_scores,
        "score_frequencies": [score_counts[s] for s in sorted_scores],
        "convergence": running_probabilities,
        "convergence_games": [
            min((i + 1) * interval, games) for i in range(len(running_probabilities))
        ],
    }


# MODULE 4: TRAFFIC SIMULATION
def simulate_traffic(rate=3.0, threshold=5, minutes=1000, seed=None):
    if not 0 <= rate <= 10:
        raise ValueError("Arrival rate must be between 0 and 10.")
    if not 1 <= threshold <= 10:
        raise ValueError("Threshold must be between 1 and 10.")
    if not 1 <= minutes <= 100_000:
        raise ValueError("Minutes must be between 1 and 100,000.")

    rng = random.Random(seed)
    arrivals_per_minute, running_probabilities = [], []
    congested_minutes = 0
    interval = max(1, minutes // 500)
    arrival_probability = min(rate / 10, 1.0)

    for i in range(minutes):
        arrivals = sum(1 for _ in range(10) if rng.random() < arrival_probability)
        arrivals_per_minute.append(arrivals)
        if arrivals >= threshold:
            congested_minutes += 1
        if (i + 1) % interval == 0 or i == minutes - 1:
            running_probabilities.append(congested_minutes / (i + 1))

    probability = congested_minutes / minutes
    arrival_counts = {}
    for count in arrivals_per_minute:
        arrival_counts[count] = arrival_counts.get(count, 0) + 1
    sorted_arrivals = sorted(arrival_counts)

    return {
        "module": "Traffic Simulation",
        "arrival_rate": rate,
        "congestion_threshold": threshold,
        "minutes_simulated": minutes,
        "congested_minutes": congested_minutes,
        "non_congested_minutes": minutes - congested_minutes,
        "congestion_probability": probability,
        "congestion_percentage": probability * 100,
        "non_congestion_percentage": (1 - probability) * 100,
        "average_arrivals": sum(arrivals_per_minute) / minutes,
        "arrivals_per_minute": arrivals_per_minute,
        "arrival_values": sorted_arrivals,
        "arrival_frequencies": [arrival_counts[x] for x in sorted_arrivals],
        "convergence": running_probabilities,
        "convergence_minutes": [
            min((i + 1) * interval, minutes) for i in range(len(running_probabilities))
        ],
    }

# ============================================================
# MODULE 5: STOCK MARKET SIMULATION
# Monte Carlo simulation of possible stock price paths
# ============================================================

def simulate_stock_market(
    initial_price=100.0,
    annual_return=0.08,
    annual_volatility=0.20,
    days=252,
    simulations=1000,
    seed=None,
):
    if initial_price <= 0:
        raise ValueError("Initial price must be greater than 0.")
    if not -1 <= annual_return <= 1:
        raise ValueError("Annual return must be between -1 and 1.")
    if not 0 <= annual_volatility <= 2:
        raise ValueError("Annual volatility must be between 0 and 2.")
    if not 1 <= days <= 2520:
        raise ValueError("Days must be between 1 and 2520.")
    if not 1 <= simulations <= 10000:
        raise ValueError("Simulations must be between 1 and 10000.")

    rng = random.Random(seed)
    dt = 1 / 252
    drift = (annual_return - 0.5 * annual_volatility ** 2) * dt
    daily_volatility = annual_volatility * math.sqrt(dt)

    final_prices = []
    sample_paths = []
    daily_price_sums = [0.0] * (days + 1)
    above_start = 0
    paths_to_save = min(simulations, 30)

    for sim in range(simulations):
        price = initial_price
        path = [price]
        daily_price_sums[0] += price

        for day in range(1, days + 1):
            z = rng.gauss(0, 1)
            price *= math.exp(drift + daily_volatility * z)
            daily_price_sums[day] += price

            if sim < paths_to_save:
                path.append(price)

        final_prices.append(price)

        if price > initial_price:
            above_start += 1

        if sim < paths_to_save:
            sample_paths.append(path)

    sorted_prices = sorted(final_prices)
    average_path = [
        total / simulations for total in daily_price_sums
    ]

    return {
        "module": "Stock Market Simulation",
        "initial_price": initial_price,
        "annual_return_assumption": annual_return,
        "annual_volatility": annual_volatility,
        "days_simulated": days,
        "simulations": simulations,
        "average_final_price": sum(final_prices) / simulations,
        "median_final_price": (
            sorted_prices[simulations // 2]
            if simulations % 2
            else (
                sorted_prices[simulations // 2 - 1]
                + sorted_prices[simulations // 2]
            ) / 2
        ),
        "best_final_price": sorted_prices[-1],
        "worst_final_price": sorted_prices[0],
        "probability_finish_above_start": above_start / simulations,
        "probability_finish_above_start_percentage": (
            above_start / simulations * 100
        ),
        "average_price_path": average_path,
        "sample_paths": sample_paths,
        "final_price_distribution": final_prices,
        "day_numbers": list(range(days + 1)),
    }



# OPTIONAL HELPER: compare independent pi runs (no new API route required)
def compare_pi_runs(points=10000, runs=5, seed=None):
    if not 100 <= points <= 1_000_000:
        raise ValueError("Points must be between 100 and 1,000,000.")
    if not 1 <= runs <= 100:
        raise ValueError("Runs must be between 1 and 100.")
    master_rng = random.Random(seed)
    results = [
        estimate_pi(points=points, seed=master_rng.randrange(0, 2**32))
        for _ in range(runs)
    ]
    estimates = [result["estimate"] for result in results]
    mean_estimate = sum(estimates) / runs
    return {
        "module": "Estimation of Pi - Repeated Runs",
        "points_per_run": points,
        "runs": runs,
        "estimates": estimates,
        "mean_estimate": mean_estimate,
        "reference_pi": math.pi,
        "absolute_error_of_mean": abs(mean_estimate - math.pi),
        "percentage_error_of_mean": _percentage_error(mean_estimate, math.pi),
    }
