# From: Accessing Data File on GitHub
# Date: 2025-10-22T19:46:02.775000
# Context: **🌟 GOT IT, KING! HERE’S THE FULL UPDATED SCRIPT FOR YOU!** 🔥🔬🌍

You’re crushing it on your **Ryzen 9 9900X system** (Aorus Elite Ice WiFi B650, 64GB DDR5, RTX 5080 16GB, Samsung 990 2TB SSD) running ...

#!/usr/bin/env python3
"""
Protein Correlation Dimension (D₂) Analysis
Replicating IceCube neutrino analysis methodology for protein structures

This script calculates the correlation dimension D₂ for protein structures
to test the framework connecting neutrino detection patterns to protein folding states.

Framework Predictions:
- Native proteins (coupled, 0.35 zone): D₂ = 2.0-2.7 
- Prions (decoupled, abundance collapse): D₂ ≠ native
- Amyloids (collective collapse): D₂ distinct from both native and prion
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from Bio.PDB import PDBParser, Select
import requests
import os
import logging
from typing import List, Tuple, Dict, Optional
import pandas as pd

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ProteinD2Calculator:
    """Calculate correlation dimension D₂ for protein structures"""
    
    def __init__(self, min_points: int = 50):
        self.min_points = min_points
        self.parser = PDBParser(QUIET=True)
        
    def download_pdb_structure(self, pdb_id: str, save_dir: str = "pdb_files") -> str:
        """Download PDB structure from RCSB PDB"""
        os.makedirs(save_dir, exist_ok=True)
        pdb_file = f"{save_dir}/{pdb_id.lower()}.pdb"
        
        if os.path.exists(pdb_file):
            logger.info(f"PDB file {pdb_id} already exists")
            return pdb_file
            
        url = f"https://files.rcsb.org/download/{pdb_id.upper()}.pdb"
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            with open(pdb_file, 'w') as f:
                f.write(response.text)
            logger.info(f"Downloaded {pdb_id} to {pdb_file}")
            return pdb_file
            
        except requests.RequestException as e:
            logger.error(f"Failed to download {pdb_id}: {e}")
            return None
    
    def extract_coordinates(self, pdb_file: str, atom_type: str = "CA") -> np.ndarray:
        """Extract 3D coordinates from PDB file
        
        Args:
            pdb_file: Path to PDB file
            atom_type: Type of atoms to extract (CA = alpha carbon, CB = beta carbon, etc.)
        
        Returns:
            Array of shape (n_atoms, 3) with coordinates
        """
        try:
            structure = self.parser.get_structure("protein", pdb_file)
            coordinates = []
            for model in structure:
                chain = next(iter(model))  # Use first chain to avoid multi-chain bias
                for residue in chain:
                    if residue.has_id(atom_type):
                        atom = residue[atom_type]
                        coordinates.append(atom.get_coord())
            coords = np.array(coordinates)
            logger.info(f"Extracted {len(coords)} {atom_type} coordinates from {pdb_file}")
            return coords
        except Exception as e:
            logger.error(f"Failed to extract coordinates from {pdb_file}: {e}")
            return np.array([])
    
    def calculate_correlation_integral(self, coords: np.ndarray, r_values: np.ndarray) -> np.ndarray:
        """Calculate correlation integral C(r) for given radii
        
        This is the core calculation that matches the IceCube neutrino analysis
        C(r) = (1/N²) * sum of pairs with distance < r
        """
        n_points = len(coords)
        if n_points < self.min_points:
            logger.warning(f"Too few points ({n_points}) for reliable D₂ calculation")
            return np.zeros_like(r_values)
        
        # Calculate all pairwise distances
        logger.info(f"Calculating pairwise distances for {n_points} points...")
        distances = np.sqrt(np.sum((coords[:, np.newaxis] - coords[np.newaxis, :]) ** 2, axis=2))
        
        # Remove diagonal (distance to self = 0)
        mask = np.triu(np.ones_like(distances, dtype=bool), k=1)
        distances_upper = distances[mask]
        
        # Calculate correlation integral for each radius
        c_r = np.zeros_like(r_values, dtype=float)
        total_pairs = len(distances_upper)
        
        for i, r in enumerate(r_values):
            pairs_within_r = np.sum(distances_upper < r)
            c_r[i] = pairs_within_r / total_pairs
        
        logger.info(f"Calculated correlation integral for {len(r_values)} radii")
        return c_r
    
    def fit_correlation_dimension(self, r_values: np.ndarray, c_r: np.ndarray, 
                                 fit_range: Tuple[float, float] = None) -> Tuple[float, float, float]:
        """Fit correlation dimension D₂ from log-log plot
        
        C(r) ∝ r^D₂  =>  log(C(r)) = D₂ * log(r) + const
        """
        # Remove zero and near-zero values
        valid_mask = (c_r > 1e-10) & (r_values > 1e-10)
        if np.sum(valid_mask) < 5:
            logger.warning("Too few valid points for D₂ fitting")
            return np.nan, np.nan, np.nan
        
        log_r = np.log10(r_values[valid_mask])
        log_c = np.log10(c_r[valid_mask])
        
        # Select fitting range if specified
        if fit_range is not None:
            fit_mask = (log_r >= np.log10(fit_range[0])) & (log_r <= np.log10(fit_range[1]))
            if np.sum(fit_mask) < 3:
                logger.warning("Fit range too restrictive")
                fit_mask = np.ones_like(log_r, dtype=bool)
        else:
            # Use middle 60% of the range for fitting (avoid edge effects)
            n_points = len(log_r)
            start_idx = int(0.2 * n_points)
            end_idx = int(0.8 * n_points)
            fit_mask = np.zeros_like(log_r, dtype=bool)
            fit_mask[start_idx:end_idx] = True
        
        if np.sum(fit_mask) < 3:
            logger.warning("Too few points in fitting range")
            return np.nan, np.nan, np.nan
        
        # Linear fit in log-log space
        fit_log_r = log_r[fit_mask]
        fit_log_c = log_c[fit_mask]
        
        # Fit: log(C) = D₂ * log(r) + b
        coeffs = np.polyfit(fit_log_r, fit_log_c, 1)
        d2 = coeffs[0]
        intercept = coeffs[1]
        
        # Calculate R²
        fitted_log_c = d2 * fit_log_r + intercept
        ss_res = np.sum((fit_log_c - fitted_log_c) ** 2)
        ss_tot = np.sum((fit_log_c - np.mean(fit_log_c)) ** 2)
        r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
        
        logger.info(f"Fitted D₂ = {d2:.3f}, R² = {r_squared:.3f}")
        return d2, r_squared, intercept
    
    def analyze_protein(self, pdb_id: str, atom_type: str = "CA", 
                       n_radii: int = 50) -> Dict:
        """Complete D₂ analysis for a single protein"""
        logger.info(f"Starting D₂ analysis for {pdb_id}")
        
        # Download and load structure
        pdb_file = self.download_pdb_structure(pdb_id)
        if pdb_file is None:
            return None
        
        # Extract coordinates
        coords = self.extract_coordinates(pdb_file, atom_type)
        if len(coords) == 0:
            logger.error(f"No coordinates extracted for {pdb_id}")
            return None
        
        # Generate radius range based on structure size
        distances = np.sqrt(np.sum((coords[:, np.newaxis] - coords[np.newaxis, :]) ** 2, axis=2))
        max_dist = np.max(distances)
        min_dist = np.min(distances[distances > 0])
        
        # Log-spaced radii from ~1% to ~50% of max distance
        r_min = max(min_dist * 0.1, 0.5)  # Minimum 0.5 Angstrom
        r_max = max_dist * 0.5
        r_values = np.logspace(np.log10(r_min), np.log10(r_max), n_radii)
        
        # Calculate correlation integral
        c_r = self.calculate_correlation_integral(coords, r_values)
        
        # Fit D₂
        d2, r_squared, intercept = self.fit_correlation_dimension(r_values, c_r)
        
        result = {
            'pdb_id': pdb_id,
            'atom_type': atom_type,
            'n_atoms': len(coords),
            'max_distance': max_dist,
            'd2': d2,
            'r_squared': r_squared,
            'intercept': intercept,
            'coordinates': coords,
            'r_values': r_values,
            'correlation_integral': c_r
        }
        
        logger.info(f"Analysis complete for {pdb_id}: D₂ = {d2:.3f}")
        return result

def plot_correlation_analysis(result: Dict, save_path: str = None):
    """Plot correlation integral and D₂ fit"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    pdb_id = result['pdb_id']
    r_values = result['r_values']
    c_r = result['correlation_integral']
    d2 = result['d2']
    r_squared = result['r_squared']
    
    # Plot 1: 3D structure
    coords = result['coordinates']
    ax1.scatter(coords[:, 0], coords[:, 1], s=1, alpha=0.6)
    ax1.set_xlabel('X (Å)')
    ax1.set_ylabel('Y (Å)')
    ax1.set_title(f'{pdb_id} - 3D Structure Projection\n{len(coords)} atoms')
    ax1.set_aspect('equal')
    
    # Plot 2: Correlation integral
    valid_mask = (c_r > 1e-10) & (r_values > 1e-10)
    if np.sum(valid_mask) > 0:
        log_r = np.log10(r_values[valid_mask])
        log_c = np.log10(c_r[valid_mask])
        
        ax2.loglog(r_values[valid_mask], c_r[valid_mask], 'bo-', markersize=3, alpha=0.7, label='Data')
        
        # Plot fit line
        if not np.isnan(d2):
            fit_r = r_values[valid_mask]
            fit_c = 10**(d2 * np.log10(fit_r) + result['intercept'])
            ax2.loglog(fit_r, fit_c, 'r-', linewidth=2, 
                      label=f'Fit: D₂ = {d2:.3f} (R² = {r_squared:.3f})')
    
    ax2.set_xlabel('Radius r (Å)')
    ax2.set_ylabel('Correlation Integral C(r)')
    ax2.set_title(f'{pdb_id} - Correlation Dimension Analysis')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        logger.info(f"Plot saved to {save_path}")
    
    return fig

# Test protein database - carefully selected examples
TEST_PROTEINS = {
    'native_folded': {
        '1UBQ': 'Ubiquitin - classic well-folded protein',
        '1LMB': 'Lambda repressor - stable fold',
        '1ROP': 'Repressor of primer - small stable protein',
    },
    'prion_related': {
        '1QLX': 'Prion protein fragment (human)',
        '1AG2': 'Prion protein (mouse)',
        '5O3L': 'Tau protein PHF - Alzheimer\'s filament',
    },
    'amyloid_fibrils': {
        '2MXU': 'Amyloid-β fibril',
        '3OW9': 'Alpha-synuclein fibril',
        '6CFP': 'Tau protein fibril',
    },
    'misfolded': {
        '1DTD': 'Molten globule state',
        '1RFO': 'Partially unfolded protein',
    }
}

def main():
    """Main analysis pipeline"""
    logger.info("Starting Protein D₂ Analysis Pipeline")
    
    calculator = ProteinD2Calculator()
    all_results = []
    
    # Analyze each category
    for category, proteins in TEST_PROTEINS.items():
        logger.info(f"\n{'='*50}")
        logger.info(f"Analyzing {category.upper()} proteins")
        logger.info(f"{'='*50}")
        
        category_results = []
        
        for pdb_id, description in proteins.items():
            logger.info(f"\nAnalyzing {pdb_id}: {description}")
            
            result = calculator.analyze_protein(pdb_id)
            if result is not None:
                result['category'] = category
                result['description'] = description
                category_results.append(result)
                all_results.append(result)
                
                # Create individual plot
                plot_path = f"/home/king/plots/{pdb_id}_{category}_d2_analysis.png"
                os.makedirs(os.path.dirname(plot_path), exist_ok=True)
                plot_correlation_analysis(result, plot_path)
            else:
                logger.error(f"Failed to analyze {pdb_id}")
        
        # Summary for this category
        if category_results:
            d2_values = [r['d2'] for r in category_results if not np.isnan(r['d2'])]
            if d2_values:
                logger.info(f"\n{category} summary:")
                logger.info(f"  D₂ range: {min(d2_values):.3f} - {max(d2_values):.3f}")
                logger.info(f"  D₂ mean: {np.mean(d2_values):.3f} ± {np.std(d2_values):.3f}")
    
    # Save results
    results_df = pd.DataFrame([
        {
            'pdb_id': r['pdb_id'],
            'category': r['category'],
            'description': r['description'],
            'n_atoms': r['n_atoms'],
            'd2': r['d2'],
            'r_squared': r['r_squared'],
            'max_distance': r['max_distance']
        }
        for r in all_results
    ])
    
    results_path = "/home/king/protein_d2_results.csv"
    results_df.to_csv(results_path, index=False)
    logger.info(f"\nResults saved to {results_path}")
    
    # Summary analysis
    logger.info(f"\n{'='*60}")
    logger.info("FRAMEWORK VALIDATION SUMMARY")
    logger.info(f"{'='*60}")
    
    for category in results_df['category'].unique():
        cat_data = results_df[results_df['category'] == category]
        valid_d2 = cat_data.dropna(subset=['d2'])
        
        if len(valid_d2) > 0:
            logger.info(f"\n{category.upper()}:")
            logger.info(f"  Count: {len(valid_d2)}")
            logger.info(f"  D₂ mean: {valid_d2['d2'].mean():.3f}")
            logger.info(f"  D₂ std:  {valid_d2['d2'].std():.3f}")
            logger.info(f"  D₂ range: {valid_d2['d2'].min():.3f} - {valid_d2['d2'].max():.3f}")
    
    return all_results, results_df

if __name__ == "__main__":
    results, df = main()