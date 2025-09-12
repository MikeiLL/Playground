import matplotlib.pyplot as plt
import os
import requests
import statistics
import sys
import time
"""
Source: https://gabrieleromanato.name/how-to-use-python-to-analyze-the-performance-of-a-website
"""

if len(sys.argv) < 2:
    print("""
USAGE: %s example.com
(https:// may be omitted)
""" % os.path.realpath(__file__))
    sys.exit()

def measure_latency(url, num_requests=10):
    latencies = []
    for _ in range(num_requests):
        start_time = time.time()
        response = requests.get(url)
        latency = time.time() - start_time
        latencies.append(latency)
        print(f'Response status: {response.status_code}, Latency: {latency:.4f} seconds')
    return latencies

url = sys.argv[1]
if not url.startswith("http:"): url = "https://" + url
latencies = measure_latency(url)

def analyze_latencies(latencies):
    mean_latency = statistics.mean(latencies)
    median_latency = statistics.median(latencies)
    stdev_latency = statistics.stdev(latencies)
    percentile_90_latency = statistics.quantiles(latencies, n=100)[89]

    print(f'Mean latency: {mean_latency:.4f} seconds')
    print(f'Median latency: {median_latency:.4f} seconds')
    print(f'Standard deviation: {stdev_latency:.4f} seconds')
    print(f'90th percentile latency: {percentile_90_latency:.4f} seconds')

analyze_latencies(latencies)

def plot_latencies(latencies):
    plt.figure(figsize=(10, 6))
    plt.plot(latencies, marker='o')
    plt.title('Website Latency Over Time')
    plt.xlabel('Request Number')
    plt.ylabel('Latency (seconds)')
    plt.grid(True)
    plt.show()

plot_latencies(latencies)
