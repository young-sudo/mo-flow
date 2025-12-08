#!/usr/bin/env python3

import argparse
import os
import mofax as mofa
import seaborn as sns
import matplotlib.pyplot as plt

def output_results(model_path: str, output_dir: str):
    """
    Reads MOFA+ model, visualizes results, and produces output files.
    """
    model = mofa.mofa_model(model_path)

    os.makedirs(output_dir, exist_ok=True)
    model_summary = repr(model)

    # Write to a text file
    summary_path = os.path.join(output_dir, "model_summary.txt")
    with open(summary_path, "w") as f:
        f.write(model_summary + "\n")
    
    # Save R2 figure
    fig = mofa.plot_r2(model, x='View', vmax=15)
    fig.savefig(os.path.join(output_dir, "r2_by_view.png"), dpi=300, bbox_inches="tight")
    plt.close(fig)

    # Variance by factor table
    var = model.get_r2().groupby(['View']).sum()
    var['Factors'] = 'n_factors = 15' # default 15 factors
    var.to_csv(os.path.join(output, "variance.csv"))

    # Variance per modality barplot
    plt.figure(figsize=(8, 6))
    sns.barplot(data=var, x='View', y='R2', hue='Factors')

    outpath = os.path.join(output_dir, "r2_barplot.png")
    plt.savefig(outpath, dpi=300, bbox_inches="tight")
    plt.close()

    # Plotting the samples in the learned factor space
    # Coloring by Gender metadata by default
    mofa.plot_factors(model, x = "Factor1", y="Factor2",  size=20, color = "Gender")
    outpath = os.path.join(output_dir, "factors_F1_F2_Gender.png")
    fig.savefig(outpath, dpi=300, bbox_inches="tight")
    plt.close(fig)

    # Factor 1 - highest feature weights (get_weights)
    mofa.plot_weights(model, views=['mRNA', 'mutations', 'drugs'],
                      factors=0, zero_line=True, ncols=3, label_size=10);
    outpath = os.path.join(output_dir, "F1_weights.png")
    fig.savefig(outpath, dpi=300, bbox_inches="tight")
    plt.close(fig)

    # Check IGHV mutation and trisomy12
    # Coloring the samples according to IGHV status
    model.metadata.IGHV = (
    model.metadata.IGHV.astype(str).
            replace({'1.0': 'mutated', '0.0': 'unmutated'}).
            astype('category').cat.reorder_categories(["mutated", "unmutated", "nan"])
    )

    mofa.plot_factors(model, x = "Factor1", y="Factor2",  size=20, color = "IGHV")
    outpath = os.path.join(output_dir, "F1_ighv.png")
    fig.savefig(outpath, dpi=300, bbox_inches="tight")
    plt.close(fig)

    mofa.plot_factors(model, x=0, y=2, color=["IGHV", "trisomy12"], size=20,  palette="Set2")
    outpath = os.path.join(output_dir, "F1_ighv_tri12.png")
    fig.savefig(outpath, dpi=300, bbox_inches="tight")
    plt.close(fig)


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
        help="Path to the input model.\n(Default: models/CLL.hdf5)"
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
