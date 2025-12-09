#!/usr/bin/env python3

import argparse
import os
import scanpy as sc
import muon as mu
import pandas as pd


def read_data(data_dir: str, output: str):
    """
    Reads multi-omics data from the specified input path.
    """

    data = pd.read_csv(os.path.join(data_dir, "evodevo.csv"), sep=",", index_col=0)

    # Create dictionary of AnnData objects per view
    views = data.view.unique()
    data_list = [data[data.view == m].pivot(index='sample', columns='feature', values='value') for m in views]
    mods = {views[m]:sc.AnnData(data_list[m]) for m in range(len(views))}

    # Metadata: stores time and group (= species) information for each sample
    obs = (
        data[['sample', 'time', 'group']]
            .drop_duplicates()
            .rename(columns = {'group' : 'species'})
            .set_index('sample')
    )

    # Create mudata object
    mdata = mu.MuData(mods)
    mdata.obs = mdata.obs.join(obs)

    mu.tl.mofa(mdata, n_factors=5,
            groups_label="species",
            smooth_covariate='time', smooth_warping=True,
            smooth_kwargs={"warping_ref": "Mouse", "new_values": list(range(1, 15))},
            outfile=output,
            n_iterations=25) # small nr of iterations


def main():
    """
    Main function to run MEFISTO analysis on spatio-temporal multi-omics data.
    """
    
    parser = argparse.ArgumentParser(
        description="A Python script to conduct MEFISTO analysis on spatio-temporal multi-omics data.",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        '-i', '--input_dir',
        type=str,
        default='data/',
        help="Path to the input data directory.\n(Default: data/)"
    )
    parser.add_argument(
        '-o', '--output',
        type=str,
        default='models/mefisto.hdf5',
        help="Output model file path/n(Default: models/mefisto.hdf5)"
    )

    # Read data
    args = parser.parse_args()
    data_dir = args.input_dir
    output = args.output
    
    read_data(data_dir, output)

if __name__ == "__main__":
    main()
