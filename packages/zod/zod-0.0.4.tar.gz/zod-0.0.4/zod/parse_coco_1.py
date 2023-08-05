import numpy as np


RAW_RESULTS = """
output/blur-png-imgnet-2/results-original/105338.out            |   AP   |  AP50  |  AP75  |  APs  |  APm   |  APl   |
output/blur-png-imgnet-2/results-original/105338.out            |:------:|:------:|:------:|:-----:|:------:|:------:|
output/blur-png-imgnet-2/results-original/105338.out            | 30.258 | 54.787 | 28.881 | 7.221 | 30.628 | 51.214 |
--
output/blur-png-imgnet-3/results-original/105337.out            |   AP   |  AP50  |  AP75  |  APs  |  APm   |  APl   |
output/blur-png-imgnet-3/results-original/105337.out            |:------:|:------:|:------:|:-----:|:------:|:------:|
output/blur-png-imgnet-3/results-original/105337.out            | 30.129 | 54.630 | 28.882 | 7.234 | 30.394 | 51.045 |
--
output/blur-png-imgnet/results-original/103596.out          |   AP   |  AP50  |  AP75  |  APs  |  APm   |  APl   |
output/blur-png-imgnet/results-original/103596.out          |:------:|:------:|:------:|:-----:|:------:|:------:|
output/blur-png-imgnet/results-original/103596.out          | 30.117 | 54.558 | 28.714 | 7.266 | 30.476 | 50.975 |
--
output/dnat-png-imgnet-2/results-original/105339.out            |   AP   |  AP50  |  AP75  |  APs  |  APm   |  APl   |
output/dnat-png-imgnet-2/results-original/105339.out            |:------:|:------:|:------:|:-----:|:------:|:------:|
output/dnat-png-imgnet-2/results-original/105339.out            | 30.232 | 54.731 | 28.797 | 7.282 | 30.551 | 51.227 |
--
output/dnat-png-imgnet-3/results-original/105340.out            |   AP   |  AP50  |  AP75  |  APs  |  APm   |  APl   |
output/dnat-png-imgnet-3/results-original/105340.out            |:------:|:------:|:------:|:-----:|:------:|:------:|
output/dnat-png-imgnet-3/results-original/105340.out            | 30.288 | 54.909 | 28.733 | 6.967 | 30.508 | 51.415 |
--
output/dnat-png-imgnet/results-original/103599.out          |   AP   |  AP50  |  AP75  |  APs  |  APm   |  APl   |
output/dnat-png-imgnet/results-original/103599.out          |:------:|:------:|:------:|:-----:|:------:|:------:|
output/dnat-png-imgnet/results-original/103599.out          | 30.308 | 54.931 | 28.918 | 7.208 | 30.657 | 51.281 |
--
output/original-png-imgnet-2/results-original/105335.out            |   AP   |  AP50  |  AP75  |  APs  |  APm   |  APl   |
output/original-png-imgnet-2/results-original/105335.out            |:------:|:------:|:------:|:-----:|:------:|:------:|
output/original-png-imgnet-2/results-original/105335.out            | 30.160 | 54.792 | 28.673 | 7.205 | 30.326 | 51.208 |
--
output/original-png-imgnet-3/results-original/105336.out            |   AP   |  AP50  |  AP75  |  APs  |  APm   |  APl   |
output/original-png-imgnet-3/results-original/105336.out            |:------:|:------:|:------:|:-----:|:------:|:------:|
output/original-png-imgnet-3/results-original/105336.out            | 30.181 | 54.725 | 28.575 | 7.199 | 30.477 | 51.160 |
--
output/original-png-imgnet/results-original/103602.out          |   AP   |  AP50  |  AP75  |  APs  |  APm   |  APl   |
output/original-png-imgnet/results-original/103602.out          |:------:|:------:|:------:|:-----:|:------:|:------:|
output/original-png-imgnet/results-original/103602.out          | 30.352 | 54.863 | 28.921 | 7.289 | 30.661 | 51.329 |
"""
RAW_RESULTS = [line for line in RAW_RESULTS.splitlines() if line.strip()]

# Store results (3 per experiment)
RESULTS = {
    "blur": [],
    "dnat": [],
    "original": [],
}

# Parse the raw results:
for line in RAW_RESULTS:
    if line.startswith("output/"):
        # Get the experiment name
        experiment = line.split("/")[1].split("-")[0]
        try:
            # Get all the APS
            aps = [float(x) for x in line.split("|")[1:-1]]
            # Store the results
            RESULTS[experiment].append(np.array(aps))
        except:
            continue
for k, v in RESULTS.items():
    RESULTS[k] = np.array(v)


metric_names = [name.strip() for name in RAW_RESULTS[0].split("|")[1:-1]]

print(metric_names)
print(RESULTS)

# Compute the means and standard deviations of the results
means = {}
stds = {}
for k, v in RESULTS.items():
    means[k] = np.mean(v, axis=0)
    stds[k] = np.std(v, axis=0)

# Print the means (plus minus) standard deviations as a markdown table
print("| Experiment |   AP   |  AP50  |  AP75  |  APs  |  APm   |  APl   |")
print("|:----------:|:------:|:------:|:------:|:-----:|:------:|:------:|")
for k, v in RESULTS.items():
    print(
        f"| {k} | {means[k][0]:.2f} $\pm$ {stds[k][0]:.2f} | "
        f"{means[k][1]:.2f} $\pm$ {stds[k][1]:.2f} | "
        f"{means[k][2]:.2f} $\pm$ {stds[k][2]:.2f} | "
        f"{means[k][3]:.2f} $\pm$ {stds[k][3]:.2f} | "
        f"{means[k][4]:.2f} $\pm$ {stds[k][4]:.2f} | "
        f"{means[k][5]:.2f} $\pm$ {stds[k][5]:.2f} |"
    )
