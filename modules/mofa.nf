#!/usr/bin/env nextflow

process RUN_MOFA {
    input:
        path input_ch

    output:
        path "${params.output_model}/*", emit: mofa_ch


    script:
        """
        python3 scripts/run_mofa.py -i "${input_ch}" -o "${params.output_model}"
        """
}

process ANALYZE_MOFA {
    input:
        path mofa_ch

    output:
        path "${params.output_dir}/*"

    script:
        """
        python3 scripts/analyze_mofa.py -i ${mofa_ch} -o "${params.output_dir}"
        """
}
