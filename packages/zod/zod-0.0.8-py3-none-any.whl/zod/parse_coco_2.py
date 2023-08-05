import numpy as np


RAW_RESULTS = """
output/blur-png-imgnet-2/results-original/105338.out-| category   | AP     | category          | AP     | category   | AP     |
output/blur-png-imgnet-2/results-original/105338.out:|:-----------|:-------|:------------------|:-------|:-----------|:-------|
output/blur-png-imgnet-2/results-original/105338.out-| Vehicle    | 42.456 | VulnerableVehicle | 26.042 | Pedestrian | 22.275 |
--
output/blur-png-imgnet-3/results-original/105337.out-| category   | AP     | category          | AP     | category   | AP     |
output/blur-png-imgnet-3/results-original/105337.out:|:-----------|:-------|:------------------|:-------|:-----------|:-------|
output/blur-png-imgnet-3/results-original/105337.out-| Vehicle    | 42.366 | VulnerableVehicle | 25.844 | Pedestrian | 22.178 |
--
output/blur-png-imgnet/results-original/103596.out-| category   | AP     | category          | AP     | category   | AP     |
output/blur-png-imgnet/results-original/103596.out:|:-----------|:-------|:------------------|:-------|:-----------|:-------|
output/blur-png-imgnet/results-original/103596.out-| Vehicle    | 42.398 | VulnerableVehicle | 25.738 | Pedestrian | 22.217 |
--
output/dnat-png-imgnet-2/results-original/105339.out-| category   | AP     | category          | AP     | category   | AP     |
output/dnat-png-imgnet-2/results-original/105339.out:|:-----------|:-------|:------------------|:-------|:-----------|:-------|
output/dnat-png-imgnet-2/results-original/105339.out-| Vehicle    | 42.509 | VulnerableVehicle | 25.711 | Pedestrian | 22.477 |
--
output/dnat-png-imgnet-3/results-original/105340.out-| category   | AP     | category          | AP     | category   | AP     |
output/dnat-png-imgnet-3/results-original/105340.out:|:-----------|:-------|:------------------|:-------|:-----------|:-------|
output/dnat-png-imgnet-3/results-original/105340.out-| Vehicle    | 42.471 | VulnerableVehicle | 25.957 | Pedestrian | 22.436 |
--
output/dnat-png-imgnet/results-original/103599.out-| category   | AP     | category          | AP     | category   | AP     |
output/dnat-png-imgnet/results-original/103599.out:|:-----------|:-------|:------------------|:-------|:-----------|:-------|
output/dnat-png-imgnet/results-original/103599.out-| Vehicle    | 42.463 | VulnerableVehicle | 26.046 | Pedestrian | 22.416 |
--
output/original-png-imgnet-2/results-original/105335.out-| category   | AP     | category          | AP     | category   | AP     |
output/original-png-imgnet-2/results-original/105335.out:|:-----------|:-------|:------------------|:-------|:-----------|:-------|
output/original-png-imgnet-2/results-original/105335.out-| Vehicle    | 42.343 | VulnerableVehicle | 25.841 | Pedestrian | 22.297 |
--
output/original-png-imgnet-3/results-original/105336.out-| category   | AP     | category          | AP     | category   | AP     |
output/original-png-imgnet-3/results-original/105336.out:|:-----------|:-------|:------------------|:-------|:-----------|:-------|
output/original-png-imgnet-3/results-original/105336.out-| Vehicle    | 42.384 | VulnerableVehicle | 25.867 | Pedestrian | 22.294 |
--
output/original-png-imgnet/results-original/103602.out-| category   | AP     | category          | AP     | category   | AP     |
output/original-png-imgnet/results-original/103602.out:|:-----------|:-------|:------------------|:-------|:-----------|:-------|
output/original-png-imgnet/results-original/103602.out-| Vehicle    | 42.497 | VulnerableVehicle | 26.182 | Pedestrian | 22.378 |
"""
RAW_RESULTS = [line for line in RAW_RESULTS.splitlines() if line.strip()]


# Store results (3 per experiment)
RESULTS = {
    "blur": [],
    "dnat": [],
    "original": [],
}

category_names = []
# Parse the raw results:
for line in RAW_RESULTS:
    if line.startswith("output/") and "Vehicle" in line:
        # Get the experiment name
        experiment = line.split("/")[1].split("-")[0]
        items = line.split("|")[1:-1]
        items = [item.strip() for item in items]
        names = items[::2]
        if not category_names:
            category_names = names
        else:
            assert set(category_names) == set(names)
        aps = [float(item) for item in items[1::2]]
        RESULTS[experiment].append(aps)

for k, v in RESULTS.items():
    RESULTS[k] = np.array(v)


print(category_names)
print(RESULTS)

# Compute the means and standard deviations of the results
means = {}
stds = {}
for k, v in RESULTS.items():
    means[k] = np.mean(v, axis=0)
    stds[k] = np.std(v, axis=0)

# Print the means (plus minus) standard deviations as a markdown table
print("| Experiment | " + " | ".join(category_names) + " |")
print("|:----------:|" + ":-------:|" * len(category_names))
for k, v in means.items():
    print(
        "| " + k + " | " + " | ".join([f"{x:.2f} $\pm$ {y:.2f}" for x, y in zip(v, stds[k])]) + " |"
    )
