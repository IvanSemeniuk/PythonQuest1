import threading
import time
import random
import sys


# Warehouse class
# Represents a supply warehouse storing medical units.
# Each warehouse has a lock to prevent race conditions
# when multiple runners attempt to steal simultaneously.
# The steal() method simulates various possible outcomes:
# - successful theft (with random stolen amount),
# - failed attempt (nothing stolen),
# - capture event (runner is caught and stops).
# The warehouse never allows the meds count to go negative.

class Warehouse:
    def __init__(self, name, meds):
        self.name = name
        self.meds = meds
        self.lock = threading.Lock()

    def steal(self, amount):
        """
        Simulate a single theft attempt.
        Outcome types:
        - 'success': runner steals a random amount (1..requested),
        - 'fail': no meds stolen,
        - 'caught': runner is caught and must stop.
        """
        outcome = random.choice(["success", "fail", "caught"])

        if outcome == "caught":
            return ("caught", 0)

        elif outcome == "fail":
            return ("fail", 0)

        elif outcome == "success":
            stolen = min(self.meds, random.randint(1, amount))
            self.meds -= stolen
            return ("success", stolen)


# Runner class (Thread)
# Each runner represents a thief operating in a separate thread.
# A runner performs 10 theft attempts on a warehouse.
# For each attempt:
# - generates a random theft amount,
# - locks the warehouse to perform the steal safely,
# - updates personal earnings,
# - updates progress status shared with the main thread.
# If the runner gets caught, it immediately stops.

class Runner(threading.Thread):
    price_per_unit = 5  # earnings per stolen medical unit

    def __init__(self, name, warehouse, progress_dict):
        super().__init__()
        self.name = name
        self.warehouse = warehouse
        self.earnings = 0
        self.progress_dict = progress_dict

    def run(self):
        total_attempts = 10

        for i in range(total_attempts):
            amount = random.randint(10, 30)

            with self.warehouse.lock:
                result, stolen = self.warehouse.steal(amount)

                if result == "success":
                    self.earnings += stolen * self.price_per_unit

                elif result == "caught":
                    self.progress_dict[self.name] = f"CAUGHT at attempt {i+1}"
                    break

            self.progress_dict[self.name] = f"{i+1}/{total_attempts}"

            time.sleep(random.uniform(0.1, 0.5))

        if "CAUGHT" not in self.progress_dict[self.name]:
            self.progress_dict[self.name] += " (done)"


# Progress bar display
# Continuously clears and redraws the terminal to show
# the live progress of each runner. This allows observing
# thread activity in real time.

def display_progress(progress_dict):
    sys.stdout.write("\033[2J\033[H")
    print("=== RUNNER PROGRESS ===")
    for runner, status in progress_dict.items():
        print(f"{runner:<12}: {status}")
    print("========================")


# Single simulation run
def simulate():
    warehouses = [
        Warehouse("Depot A", random.randint(100, 300)),
        Warehouse("Depot B", random.randint(100, 300)),
        Warehouse("Depot C", random.randint(100, 300)),
        Warehouse("Depot D", random.randint(100, 300)),
    ]

    progress = {}

    runners = []
    for i in range(5):
        wh = random.choice(warehouses)
        name = f"Runner_{i+1}"
        progress[name] = "0/10"
        r = Runner(name, wh, progress)
        runners.append(r)

    for r in runners:
        r.start()

    while any(r.is_alive() for r in runners):
        display_progress(progress)
        time.sleep(0.2)

    display_progress(progress)

    print("\n=== FINAL REPORT ===")
    total_earnings = sum(r.earnings for r in runners)

    print("\nRemaining meds per warehouse:")
    for wh in warehouses:
        print(f"{wh.name}: {wh.meds} units left")

    print("\nEarnings per runner:")
    for r in runners:
        print(f"{r.name}: earned {r.earnings}")

    print(f"\nTOTAL EARNED: {total_earnings}")
    print("======================")
    return total_earnings


# Run multiple simulations
if __name__ == "__main__":
    for sim in range(3):
        print(f"\n\n########### SIMULATION {sim+1} ###########")
        simulate()
        time.sleep(2)
