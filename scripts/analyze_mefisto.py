#!/usr/bin/env python3

import argparse
import os
import muon as mu
import mofax as mofa
import scanpy as sc
import matplotlib.pyplot as plt

def output_results(model_path: str, output_dir: str):
    """
    Reads MEFISTO model, visualizes results, and produces output files.
    """
    mdata = mofa.mofa_model(model_path)

    os.makedirs(output_dir, exist_ok=True)
    model_summary = repr(mdata)

    # Write to a text file
    summary_path = os.path.join(output_dir, "model_summary.txt")
    with open(summary_path, "w") as f:
        f.write(model_summary + "\n")
    
    # Visualize in the factor space, color by species
    fig = mu.pl.mofa(mdata, color="species", size = 250)
    fig.savefig(os.path.join(output_dir, "mefisto_factor_species.png"), dpi=300, bbox_inches="tight")
    plt.close(fig)

    # Visualize in the factor space, color by time (warped - adjust for sample imbalances)
    fig = mu.pl.mofa(mdata, color="time_warped", size = 250)
    fig.savefig(os.path.join(output_dir, "mefisto_factor_time.png"), dpi=300, bbox_inches="tight")
    plt.close(fig)

    # Visualize aligned time warped against time
    fig = sc.pl.scatter(mdata, x="time", y="time_warped", color="species", size=200)
    fig.savefig(os.path.join(output_dir, "mefisto_factor_time.png"), dpi=300, bbox_inches="tight")
    plt.close(fig)


    # Visualize interpolated factors
    fig = mofa.plot_interpolated_factors(mdata, factors=range(mdata.nfactors),
                                ncols=5, size=70)
    fig.savefig(os.path.join(output_dir, "mefisto_interpolated.png"), dpi=300, bbox_inches="tight")
    plt.close(fig)
    
    # Plot smoothness of factors
    fig = mofa.plot_smoothness(mdata)
    fig.savefig(os.path.join(output_dir, "mefisto_smoothness.png"), dpi=300, bbox_inches="tight")
    plt.close(fig)

    # Plot sharedness of factors
    fig = mofa.plot_sharedness(mdata)
    fig.savefig(os.path.join(output_dir, "mefisto_sharedness.png"), dpi=300, bbox_inches="tight")
    plt.close(fig)


    # Visualize Factor1 over time warped
    mdata.obs["Factor1"] = mdata.obsm["X_mofa"][:,0]
    sc.pl.scatter(mdata, x="time_warped", y="Factor1", color="species", size=200)



def main():
    """
    Main function to analyze MOFA+ results on multi-omics data.
    """
    parser = argparse.ArgumentParser(
    description="A Python script to conduct MOFA+ analysis on multi-omics data.",
    formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        '-i', '--input',
        type=str,
        default='models/CLL.hdf5',
        help="Path to the input model.\n(Default: models/mefisto.hdf5)"
    )
    parser.add_argument(
        '-o', '--output_dir',
        type=str,
        default='results',
        help="Output directory path for results/n(Default: results)"
    )

    args = parser.parse_args()
    model_path = args.input_dir
    output_dir = args.output_dir
    output_results(model_path, output_dir)

if __name__ == "__main__":
    main()
