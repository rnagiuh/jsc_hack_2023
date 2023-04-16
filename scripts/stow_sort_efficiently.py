import csv
import sys
import numpy as np
from typing import List, Tuple
import matplotlib.pyplot as plt

# Define a Bin class to store cargo items with the same temperature 
# and track the remaining capacity
class Bin:
    def __init__(self, capacity: float, temperature: float):
        self.capacity = capacity
        self.temperature = temperature
        self.remaining = capacity
        self.items = []
    
    # Try to add an item to the bin if it has enough remaining 
    # capacity and the same temperature
    def add_item(self, item: Tuple[float, float]) -> bool:
        weight, item_temperature = item
        if weight <= self.remaining and self.temperature == item_temperature:
            self.items.append(item)
            self.remaining -= weight
            return True
        return False

# Read cargo data (volume and temperature) from a CSV file
def read_cargo_csv(file_path: str) -> List[Tuple[float, float]]:
    cargo_data = []
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cargo_data.append((float(row['Volume']), float(row['Temperature'])))
    return cargo_data

# Implement the First Fit Decreasing algorithm to pack the cargo items in the available bin sizes
def first_fit_decreasing(cargo_data: List[Tuple[float, float]], bin_sizes: List[float]) -> List[Bin]:
    
    # Sort the cargo items by temperature (ascending) and volume (descending)    
    sorted_data = sorted(cargo_data, key=lambda x: (x[1], -x[0]))
    bins = []

    # Loop through the sorted cargo items
    for item in sorted_data:
        item_added = False

        # Try to add the item to an existing bin        
        for bin_ in bins:
            if bin_.add_item(item):
                item_added = True
                break

        # If the item couldn't be added to any existing bin, create a new bin with the 
        # appropriate size and temperature group
        if not item_added:
            for bin_size in bin_sizes:
                new_bin = Bin(bin_size, item[1])
                if new_bin.add_item(item):
                    bins.append(new_bin)
                    break

    return bins

# Calculate the packing efficiency as the ratio of total cargo weight to total bin capacity
def calculate_efficiency(bins: List[Bin], total_cargo_weight: float) -> float:
    total_bin_capacity = sum([bin.capacity for bin in bins])
    efficiency = (total_cargo_weight / total_bin_capacity) * 100
    return efficiency

# Visualize the packing efficiency of the First Fit Decreasing algorithm compared to the 
# maximum possible efficiency
def visualize_efficiencies(bins: List[Bin], bin_sizes: List[float], max_efficiency: float):
    # Separate bins based on their temperature requirements
    cold_bins = [bin_ for bin_ in bins if bin_.temperature < 0]
    ambient_bins = [bin_ for bin_ in bins if bin_.temperature >= 0]

    # Calculate the efficiency and remaining space for each bin size and temperature requirement
    efficiency_data = {}
    remaining_space_data = {}
    for size in bin_sizes:
        efficiency_data[size] = {
            'cold': 0,
            'ambient': 0
        }
        remaining_space_data[size] = {
            'cold': 0,
            'ambient': 0
        }

        cold_bins_size = [bin_ for bin_ in cold_bins if bin_.capacity == size]
        ambient_bins_size = [bin_ for bin_ in ambient_bins if bin_.capacity == size]

        total_cargo_weight_cold = sum([size - bin_.remaining for bin_ in cold_bins_size])
        total_cargo_weight_ambient = sum([size - bin_.remaining for bin_ in ambient_bins_size])
        total_remaining_space_cold = sum([bin_.remaining for bin_ in cold_bins_size])
        total_remaining_space_ambient = sum([bin_.remaining for bin_ in ambient_bins_size])

        if cold_bins_size:
            efficiency_data[size]['cold'] = (total_cargo_weight_cold / (len(cold_bins_size) * size)) * 100
            remaining_space_data[size]['cold'] = total_remaining_space_cold
        if ambient_bins_size:
            efficiency_data[size]['ambient'] = (total_cargo_weight_ambient / (len(ambient_bins_size) * size)) * 100
            remaining_space_data[size]['ambient'] = total_remaining_space_ambient

    # Visualize the efficiencies and remaining spaces in grouped bar charts
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    bar_width = 0.35
    x_labels = [f"{size:.1f}" for size in bin_sizes]

    cold_efficiencies = [efficiency_data[size]['cold'] for size in bin_sizes]
    ambient_efficiencies = [efficiency_data[size]['ambient'] for size in bin_sizes]
    cold_remaining_spaces = [remaining_space_data[size]['cold'] for size in bin_sizes]
    ambient_remaining_spaces = [remaining_space_data[size]['ambient'] for size in bin_sizes]

    x = np.arange(len(bin_sizes))
    ax1.bar(x - bar_width / 2, cold_efficiencies, bar_width, label="Cold (< 0°C)")
    ax1.bar(x + bar_width / 2, ambient_efficiencies, bar_width, label="Ambient (≥ 0°C)")

    ax1.set_xticks(x)
    ax1.set_xticklabels(x_labels)
    ax1.set_xlabel("Bin Size")
    ax1.set_ylabel("Efficiency (%)")
    ax1.set_ylim(0, 100)
    ax1.legend()
    ax1.set_title("Packing Efficiencies")

    ax2.bar(x - bar_width / 2, cold_remaining_spaces, bar_width, label="Cold (< 0°C)")
    ax2.bar(x + bar_width / 2, ambient_remaining_spaces, bar_width, label="Ambient (≥ 0°C)")

    ax2.set_xticks(x)
    ax2.set_xticklabels(x_labels)
    ax2.set_xlabel("Bin Size")
    ax2.set_ylabel("Remaining Space")
    ax2.legend()
    ax2.set_title("Remaining Space per Bin")

    plt.tight_layout()
    plt.show()

def main(file_path: str, bin_sizes: List[float]):
    
    # Read the cargo data from the CSV file
    cargo_data = read_cargo_csv(file_path)
    # Calculate the total cargo weight
    total_cargo_weight = sum([weight for weight, _ in cargo_data])
    # Calculate the maximum possible packing efficiency
    max_efficiency = min(total_cargo_weight / min(bin_sizes), 1) * 100
    
    # Perform First Fit Decreasing on the cargo data
    bins = first_fit_decreasing(cargo_data, bin_sizes)
    
    # Calculate the packing efficiency using the First Fit Decreasing algorithm
    ffd_efficiency = calculate_efficiency(bins, total_cargo_weight)

    # Print the number of bins used and their contents, remaining capacity, and temperature
    print(f"Number of bins required: {len(bins)}")
    for i, bin_ in enumerate(bins, start=1):
        print(f"Bin {i}: {bin_.items}, Remaining capacity: {bin_.remaining}, Temperature: {bin_.temperature}")

    # Print the packing efficiency of the First Fit Decreasing algorithm and the maximum possible efficiency
    print(f"FFD Algorithm Efficiency: {ffd_efficiency:.2f}%")
    print(f"Maximum Possible Efficiency: {max_efficiency:.2f}%")

    # Visualize the packing efficiencies using a bar chart
    visualize_efficiencies(bins, bin_sizes, max_efficiency)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python bin_packing.py <csv_file_path> <bin_size_1> [<bin_size_2> ... <bin_size_n>]")
        sys.exit(1)

    file_path = sys.argv[1]
    bin_sizes = [float(size) for size in sys.argv[2:]]
    main(file_path, bin_sizes)
