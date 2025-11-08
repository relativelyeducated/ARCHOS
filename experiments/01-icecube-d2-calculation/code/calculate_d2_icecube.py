#!/usr/bin/env python3
"""
IceCube Neutrino Correlation Dimension (D₂) Calculator

This script calculates the correlation dimension D₂ for IceCube neutrino events
to test the Dialectical Fractal Archestructure (DFA) theory prediction: D₂ = 1.45 ± 0.10

Author: Jason King (Jackie Junaid)
Date: October 8, 2025
License: CC-BY 4.0
Repository: https://github.com/relativelyeducated/dialectical-fractal-theory
"""

import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
from typing import Tuple, List

# ============================================================================
# CONFIGURATION
# ============================================================================

# Data file path (adjust as needed)
DATA_FILE = 'data.dat'  # Format: Energy(GeV) Zenith(radians)

# Correlation dimension parameters
SAMPLE_SIZE = 10000      # Subsample for computational efficiency
R_MIN = 1e-3             # Minimum radius for correlation integral
R_MAX = 1.0              # Maximum radius
N_RADII = 50             # Number of radii to sample
FIT_EXCLUDE = 10         # Exclude last N points from fit (avoid saturation)

# Energy bins for stratified analysis (in GeV)
ENERGY_BINS = [
    (0, 1e3, 'Low (< 1 TeV)'),
    (1e3, 1e5, 'Mid (1-100 TeV)'),
    (1e7, np.inf, 'High (> 10 PeV)')
]

# Bootstrap parameters
N_BOOTSTRAP = 1000

# Clustering parameters
DBSCAN_EPS = 0.1
DBSCAN_MIN_SAMPLES = 5

# ============================================================================
# CORE FUNCTIONS
# ============================================================================

def load_icecube_data(filepath: str) -> pd.DataFrame:
    """
    Load IceCube neutrino event data.

    Expected format: Two columns (Energy, Zenith) separated by whitespace.
    - Energy in GeV
    - Zenith in radians

    Args:
        filepath: Path to data file

    Returns:
        DataFrame with columns: Energy, Zenith, Log_E, Cos_Zenith
    """
    # Load raw data
    data = pd.read_csv(filepath, sep=r'\s+', header=None, names=['Energy', 'Zenith'])

    # Preprocess features
    data['Log_E'] = np.log10(data['Energy'])
    data['Cos_Zenith'] = np.cos(data['Zenith'])

    print(f"Loaded {len(data)} events")
    print(f"Energy range: {data['Energy'].min():.2e} - {data['Energy'].max():.2e} GeV")
    print(f"Zenith range: {np.degrees(data['Zenith'].min()):.1f}° - {np.degrees(data['Zenith'].max()):.1f}°")

    return data


def calculate_correlation_dimension(events: np.ndarray,
                                    sample_size: int = SAMPLE_SIZE,
                                    r_min: float = R_MIN,
                                    r_max: float = R_MAX,
                                    n_radii: int = N_RADII,
                                    fit_exclude: int = FIT_EXCLUDE) -> Tuple[float, float]:
    """
    Calculate correlation dimension D₂ using Grassberger-Procaccia algorithm.

    The correlation integral is:
        C(r) = (1/N²) Σ Θ(r - |x_i - x_j|)

    And D₂ is the slope of log C(r) vs log r in the scaling region.

    Args:
        events: N×2 array of (log_E, cos_zenith) coordinates
        sample_size: Number of events to subsample (for efficiency)
        r_min: Minimum radius
        r_max: Maximum radius
        n_radii: Number of radii to sample
        fit_exclude: Number of points to exclude from fit (avoid saturation)

    Returns:
        (D₂, std_error): Correlation dimension and standard error
    """
    N = min(len(events), sample_size)

    # Subsample if necessary
    if len(events) > sample_size:
        indices = np.random.choice(len(events), sample_size, replace=False)
        sample = events[indices]
    else:
        sample = events

    # Compute all pairwise distances
    distances = cdist(sample, sample, metric='euclidean')

    # Correlation integral for each radius
    r_values = np.logspace(np.log10(r_min), np.log10(r_max), n_radii)
    C_r = np.array([np.sum(distances < r) / N**2 for r in r_values])

    # Log-log fit (exclude saturation region)
    log_r = np.log(r_values[:-fit_exclude])
    log_C = np.log(C_r[:-fit_exclude] + 1e-10)  # Avoid log(0)

    # Linear regression: log C = D₂ × log r + const
    coeffs, residuals, _, _, _ = np.polyfit(log_r, log_C, 1, full=True)
    D2 = coeffs[0]

    # Estimate error from residuals
    std_error = np.sqrt(residuals[0] / (len(log_r) - 2)) if len(residuals) > 0 else 0.05

    return D2, std_error


def calculate_d2_bootstrap(events: np.ndarray, n_bootstrap: int = N_BOOTSTRAP) -> Tuple[float, float]:
    """
    Calculate D₂ with bootstrap error estimation.

    Args:
        events: N×2 array of events
        n_bootstrap: Number of bootstrap resamples

    Returns:
        (mean_D₂, std_D₂): Mean and standard deviation over bootstrap samples
    """
    d2_samples = []

    for _ in range(n_bootstrap):
        # Resample with replacement
        indices = np.random.choice(len(events), len(events), replace=True)
        resampled = events[indices]

        # Calculate D₂
        d2, _ = calculate_correlation_dimension(resampled)
        d2_samples.append(d2)

    return np.mean(d2_samples), np.std(d2_samples)


def energy_stratified_d2(data: pd.DataFrame, bins: List[Tuple]) -> pd.DataFrame:
    """
    Calculate D₂ for different energy ranges.

    Args:
        data: DataFrame with Energy, Log_E, Cos_Zenith columns
        bins: List of (E_min, E_max, label) tuples

    Returns:
        DataFrame with columns: Energy_Range, D₂, Error, N_events
    """
    results = []

    for e_min, e_max, label in bins:
        # Filter events
        mask = (data['Energy'] >= e_min) & (data['Energy'] < e_max)
        subset = data[mask]

        if len(subset) < 100:
            print(f"Warning: Only {len(subset)} events in {label} bin, skipping")
            continue

        # Calculate D₂
        events = subset[['Log_E', 'Cos_Zenith']].values
        d2, error = calculate_correlation_dimension(events)

        results.append({
            'Energy_Range': label,
            'E_min_GeV': e_min,
            'E_max_GeV': e_max,
            'D2': d2,
            'Error': error,
            'N_events': len(subset)
        })

        print(f"{label}: D₂ = {d2:.2f} ± {error:.2f} ({len(subset)} events)")

    return pd.DataFrame(results)


def angular_correlation(data: pd.DataFrame) -> Tuple[float, float]:
    """
    Calculate angular correlation power-law exponent.

    DFA predicts: C(θ) ∝ θ^(-α) with α ≈ 0.45

    Args:
        data: DataFrame with Zenith column

    Returns:
        (slope, error): Power-law exponent and error
    """
    zenith = data['Zenith'].values

    # Compute pairwise angular differences
    zenith_diff = np.abs(zenith[:, None] - zenith[None, :])

    # Select small angles (< 10° ≈ 0.17 rad) to avoid large-scale structure
    theta_small = zenith_diff[(zenith_diff > 1e-3) & (zenith_diff < 0.17)]

    if len(theta_small) < 10:
        print("Warning: Insufficient small-angle pairs")
        return np.nan, np.nan

    # Histogram of angles
    counts, bin_edges = np.histogram(theta_small, bins=20)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    # Power-law fit: log(counts) = -α × log(θ) + const
    log_theta = np.log10(bin_centers)
    log_counts = np.log10(counts + 1)

    coeffs = np.polyfit(log_theta, log_counts, 1)
    slope = -coeffs[0]  # Negative because counts decay

    # Crude error estimate
    error = 0.05

    return slope, error


def cluster_analysis(events: np.ndarray, eps: float = DBSCAN_EPS,
                    min_samples: int = DBSCAN_MIN_SAMPLES) -> Tuple[int, np.ndarray]:
    """
    Perform DBSCAN clustering to identify event clusters.

    Args:
        events: N×2 array
        eps: DBSCAN neighborhood radius
        min_samples: Minimum points per cluster

    Returns:
        (n_clusters, cluster_sizes): Number of clusters and size distribution
    """
    db = DBSCAN(eps=eps, min_samples=min_samples).fit(events)
    labels = db.labels_

    # Count clusters (excluding noise label -1)
    unique_labels = set(labels)
    n_clusters = len(unique_labels) - (1 if -1 in unique_labels else 0)

    # Cluster size distribution
    cluster_sizes = [np.sum(labels == label) for label in unique_labels if label != -1]

    return n_clusters, np.array(cluster_sizes)


# ============================================================================
# VISUALIZATION
# ============================================================================

def plot_event_distribution(data: pd.DataFrame, output_file: str = 'icecube_distribution.png'):
    """Plot event distribution in (log E, cos θ) space."""
    plt.figure(figsize=(10, 7))
    plt.scatter(data['Log_E'], data['Cos_Zenith'], alpha=0.3, s=1)
    plt.xlabel('Log₁₀(Energy [GeV])')
    plt.ylabel('Cos(Zenith)')
    plt.title('IceCube Neutrino Event Distribution')
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_file, dpi=150)
    print(f"Saved: {output_file}")


def plot_correlation_integral(events: np.ndarray, output_file: str = 'correlation_integral.png'):
    """Plot correlation integral C(r) vs r."""
    N = min(len(events), SAMPLE_SIZE)
    sample = events[np.random.choice(len(events), N, replace=False)] if len(events) > N else events

    distances = cdist(sample, sample, metric='euclidean')
    r_values = np.logspace(np.log10(R_MIN), np.log10(R_MAX), N_RADII)
    C_r = np.array([np.sum(distances < r) / N**2 for r in r_values])

    # Fit
    log_r = np.log(r_values[:-FIT_EXCLUDE])
    log_C = np.log(C_r[:-FIT_EXCLUDE] + 1e-10)
    coeffs = np.polyfit(log_r, log_C, 1)
    D2 = coeffs[0]

    plt.figure(figsize=(10, 7))
    plt.loglog(r_values, C_r, 'o', label='Data', markersize=4)
    plt.loglog(r_values[:-FIT_EXCLUDE], np.exp(coeffs[1]) * r_values[:-FIT_EXCLUDE]**D2,
               'r--', label=f'Fit: D₂ = {D2:.2f}')
    plt.xlabel('Radius r')
    plt.ylabel('Correlation Integral C(r)')
    plt.title('Grassberger-Procaccia Correlation Dimension')
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_file, dpi=150)
    print(f"Saved: {output_file}")


# ============================================================================
# MAIN ANALYSIS
# ============================================================================

def main():
    """Run complete IceCube D₂ analysis."""

    print("=" * 70)
    print("IceCube Neutrino Correlation Dimension Analysis")
    print("Dialectical Fractal Archestructure (DFA) Theory Test")
    print("=" * 70)
    print()

    # Load data
    print("Loading data...")
    data = load_icecube_data(DATA_FILE)
    events = data[['Log_E', 'Cos_Zenith']].values
    print()

    # Primary D₂ calculation
    print("Calculating total D₂...")
    D2, D2_error = calculate_correlation_dimension(events)
    print(f"Total D₂ = {D2:.2f} ± {D2_error:.2f}")
    print(f"DFA Prediction: D₂ = 1.45 ± 0.10")
    print(f"Difference: {abs(D2 - 1.45):.2f} ({abs(D2 - 1.45) / 0.10:.1f}σ)")
    print()

    # Energy-stratified D₂
    print("Energy-stratified analysis...")
    stratified_results = energy_stratified_d2(data, ENERGY_BINS)
    print()

    # Angular correlation
    print("Angular correlation analysis...")
    alpha, alpha_error = angular_correlation(data)
    print(f"Angular slope: α = {alpha:.2f} ± {alpha_error:.2f}")
    print(f"DFA Prediction: α = 0.45 ± 0.05")
    print()

    # Clustering
    print("Cluster analysis...")
    n_clusters, cluster_sizes = cluster_analysis(events)
    print(f"Number of clusters: {n_clusters}")
    print(f"DFA Prediction: N/4 = 456/4 = 114 clusters")
    print(f"Mean cluster size: {np.mean(cluster_sizes):.1f}")
    print()

    # Visualization
    print("Generating plots...")
    plot_event_distribution(data)
    plot_correlation_integral(events)
    print()

    # Summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Measured D₂: {D2:.2f} ± {D2_error:.2f}")
    print(f"Predicted D₂: 1.45 ± 0.10")
    print(f"Agreement: {'✅ CONFIRMED' if abs(D2 - 1.45) < 0.15 else '❌ DISCREPANT'}")
    print("=" * 70)


if __name__ == '__main__':
    main()
