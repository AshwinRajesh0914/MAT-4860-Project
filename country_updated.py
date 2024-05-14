import math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
import random
from concurrent.futures import ThreadPoolExecutor

class Country:
    def __init__(self, name, gold=10, elixir=10, dark_elixir=10):
        self.name = name
        self.gold = gold
        self.elixir = elixir
        self.dark_elixir = dark_elixir

    def __repr__(self):
        return f"{self.name} (Gold: {self.gold}, Elixir: {self.elixir}, Dark Elixir: {self.dark_elixir})"

    def steal(self, choices, amount):
        """Randomly steals a resource from one of the chosen countries."""
        if not choices:
            print(f"{self.name} has no valid targets to steal from.")
            return

        target = random.choice(choices)
        resource_types = ['gold', 'elixir', 'dark_elixir']
        resource_type = random.choice(resource_types)

        target_amount = getattr(target, resource_type, 0)
        amount_to_steal = min(amount, target_amount)

        setattr(self, resource_type, getattr(self, resource_type) + amount_to_steal)
        setattr(target, resource_type, max(0, target_amount - amount_to_steal))

        print(f"{self.name} stole {amount_to_steal} {resource_type} from {target.name}.")

    def collect_resource(self, pool, amount, resource_type='gold'):
        """Collects resources from a shared pool."""
        available = pool.get(resource_type, 0)
        amount_collected = min(amount, available)
        setattr(self, resource_type, getattr(self, resource_type) + amount_collected)
        pool[resource_type] = max(0, available - amount_collected)

    def make_choice(self, action, pool, choices, amount):
        """Handles the resource action logic for a country."""
        if action == 'resource':
            self.collect_resource(pool, amount, 'gold')
        elif action == 'steal':
            self.steal(choices, amount)
        else:
            pass  # idle

    def total_resources(self):
        """Returns the total sum of all resources held by the country."""
        return self.gold + self.elixir + self.dark_elixir

def competition(A, B, C, Resource, steal_amount, resource_amount):
    actions = ['idle', 'steal', 'resource']
    counter = 0

    while len([country for country in [A, B, C] if country.total_resources() > 0]) > 1:
        counter += 1
        print(f"Iteration: {counter}")

        active_countries = [country for country in [A, B, C] if country.total_resources() > 0]

        for country in [A, B, C]:
            if country in active_countries:
                action = random.choice(actions)
                others = [c for c in active_countries if c != country]
                country.make_choice(action, Resource, others, steal_amount)

        print(A)
        print(B)
        print(C)
        print("-" * 30)

    # Determine the winner
    resource_values = {A.name: A.total_resources(), B.name: B.total_resources(), C.name: C.total_resources()}
    winner = max(resource_values, key=resource_values.get)

    if list(resource_values.values()).count(max(resource_values.values())) > 1:
        return "Draw"
    return winner



def run_simulation(index):
    A = Country("A", gold=10, elixir=10, dark_elixir=10)
    B = Country("B", gold=20, elixir=20, dark_elixir=20)
    C = Country("C", gold=5, elixir=5, dark_elixir=5)
    Resource = {'gold': 50, 'elixir': 50, 'dark_elixir': 50}
    result = competition(A, B, C, Resource, 5, 3)
    print(f"Simulation {index} result: {result}")
    return result

import time

def main():
    start_time = time.time()
    num_simulations = 50
    max_workers = 12

    from multiprocessing import Pool
    with Pool(processes=max_workers) as pool:
        results = pool.map(run_simulation, range(num_simulations))

    elapsed_time = time.time() - start_time
    print(f"Total execution time: {elapsed_time:.2f} seconds")
    # Convert results to a histogram
    from collections import Counter
    import pandas as pd
    import matplotlib.pyplot as plt

    letter_counts = Counter(results)
    df = pd.DataFrame.from_dict(letter_counts, orient='index')
    df.plot(kind='bar')
    plt.show()

if __name__ == "__main__":
    main()