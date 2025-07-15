import random
import os
import sys
import pandas as pd
from deap import base, creator, tools, algorithms

# Add crypto scripts path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'crypto')))
from kyber_keygen import generate_keys
from kyber_encrypt import encrypt

def simulate_cpu_load(duration_ms):
    """Mimics CPU work with random math."""
    start = time.time()
    while time.time() - start < (duration_ms / 1000):
        _ = (random.random() ** 0.5) * random.random()

def evaluate_kyber_performance(individual):
    """Evaluate Kyber speed and size for given params."""
    plaintext_mult, cpu_load_ms = individual  # [length multiplier, CPU load]
    
    total_encrypt_time = total_size = 0
    for _ in range(5):  # Average over 5 runs
        dummy_plaintext = b"A" * (100 * int(plaintext_mult))
        simulate_cpu_load(cpu_load_ms)
        pub_key, _, _, _ = generate_keys()
        _, _, encrypt_time, ciphertext_size = encrypt(dummy_plaintext, pub_key)
        total_encrypt_time += encrypt_time
        total_size += ciphertext_size
    
    avg_encrypt_time = total_encrypt_time / 5
    avg_size = total_size / 5
    fitness = -(avg_encrypt_time + avg_size * 0.01)  # Minimize time + size penalty
    return fitness,

def optimize_kyber_with_ga():
    # Set up GA
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)
    toolbox = base.Toolbox()

    # Define individual: [plaintext length multiplier (1-5), CPU load (0-50ms)]
    toolbox.register("attr_mult", random.randint, 1, 5)
    toolbox.register("attr_load", random.uniform, 0, 50)
    toolbox.register("individual", tools.initCycle, creator.Individual,
                     (toolbox.attr_mult, toolbox.attr_load), n=1)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    # GA operators
    toolbox.register("evaluate", evaluate_kyber_performance)
    toolbox.register("mate", tools.cxBlend, alpha=0.5)
    toolbox.register("mutate", tools.mutGaussian, mu=[2.5, 25], sigma=[1, 10], indpb=0.1)
    toolbox.register("select", tools.selTournament, tournsize=3)

    # Run GA
    pop = toolbox.population(n=50)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", lambda x: sum(x) / len(x))
    stats.register("max", max)

    print("Running GA to optimize Kyber...")
    algorithms.eaSimple(pop, toolbox, cxpb=0.7, mutpb=0.2, ngen=50, stats=stats, halloffame=hof, verbose=True)

    # Log results
    best = hof[0]
    print(f"\nDone! Best setup: Length Multiplier={best[0]}, CPU Load={best[1]:.2f}ms")
    print(f"Best fitness: {best.fitness.values[0]:.4f}")

    df_log = pd.DataFrame(stats.logbook)
    df_log.index.name = 'generation'
    results_path = os.path.join("results", "optimization_results.csv")
    df_log.to_csv(results_path)
    print(f"Results saved to {results_path}")

    # Fitness progression chart
    if not df_log.empty and 'max' in df_log:
        ```chartjs
        {
            "type": "line",
            "data": {
                "labels": [str(i) for i in df_log["generation"]],
                "datasets": [{
                    "label": "Max Fitness",
                    "data": df_log["max"],
                    "borderColor": "rgba(75, 192, 192, 1)",
                    "backgroundColor": "rgba(75, 192, 192, 0.2)",
                    "fill": true
                }]
            },
            "options": {
                "plugins": { "title": { "display": true, "text": "GA Optimization Progress" } },
                "scales": {
                    "x": { "title": { "display": true, "text": "Generation" } },
                    "y": { "title": { "display": true, "text": "Max Fitness" }, "beginAtZero": false }
                }
            }
        }