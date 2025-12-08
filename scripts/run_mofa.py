#!/usr/bin/env python3

import argparse
import scanpy as sc
import muon as mu
import pandas as pd


def read_data(data_dir: str, metadata_path: str, output: str):
    """
    Reads multi-omics data from the specified input path.
    """

    mods = {i:sc.AnnData(pd.read_csv(f"{data_dir}{i}.csv", index_col=0).T)
            for i in ("mRNA", "methylation", "mutations", "drugs")}

    # Load CLL patient metadata
    CLL_metadata = pd.read_csv(metadata_path,
                           sep="\t", index_col="sample")
    
    # Create multi-modal data
    mdata = mu.MuData(mods)
    # add metadata
    mdata.obs = mdata.obs.join(CLL_metadata)

    # Run MOFA
    # use_obs: how to treat missing values
    mu.tl.mofa(mdata, use_obs='union', #likelihoods=['gaussian', 'gaussian', 'gaussian', 'gaussian']
           n_factors=15, convergence_mode='medium',
           outfile=output)


def main():
    """
    Main function to run MOFA+ analysis on multi-omics data.
    """
    
    parser = argparse.ArgumentParser(
        description="A Python script to conduct MOFA+ analysis on multi-omics data.",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        '-i', '--input_dir',
        type=str,
        default='data/',
        help="Path to the input data directory.\n(Default: data/)"
    )
    parser.add_argument(
        '-m', '--metadata',
        type=str,
        default='data/sample_metadata.txt',
        help="Additional information about each patient/n(Default: data/sample_metadata.txt)"
    )
    parser.add_argument(
        '-o', '--output',
        type=str,
        default='models/CLL.hdf5',
        help="Output model file path/n(Default: models/CLL.hdf5)"
    )

    # Read data
    args = parser.parse_args()
    data_dir = args.input_dir
    meta_path = args.metadata
    output = args.output
    
    read_data(data_dir, meta_path, output)

if __name__ == "__main__":
    main()
