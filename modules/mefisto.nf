#!/usr/bin/env nextflow

process RUN_MEFIST {
    input:
        path input_ch

    output:
        path "${params.output_model}/*", emit: mefisto_ch


    script:
        """
        python3 scripts/run_mefisto.py -i "${input_ch}" -o "${params.output_model}"
        """
}

process ANALYZE_MEFISTO {
    input:
        path mefisto_ch

    output:
        path "${params.output_dir}/*"

    script:
        """
        python3 scripts/analyze_mefisto.py -i ${mofa_ch} -o "${params.output_dir}"
        """
}
