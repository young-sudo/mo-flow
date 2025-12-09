#!/usr/bin/env nextflow

nextflow.enable.dsl=2

include { RUN_MOFA; ANALYZE_MOFA } from './modules/mofa.nf'
include { RUN_MEFISTO; ANALYZE_MEFISTO } from './modules/mefisto.nf'

params.mode = params.mode ?: null
params.input_dir = params.input_dir ?: "data"
params.output_model = params.output_model ?: "models/model.hdf5"
params.output_dir = params.output_dir ?: "results"

if ( params.help ) {
    log.info """
    Usage:
      nextflow run main.nf -profile conda --mode mapper --input_reads reads.fasta --input_reference ref.fasta

    Parameters:
       -profile           standard|conda|docker|singularity|slurm
      --mode              mapper|assembler
      --input_dir         dir path
      --output_model      output model path
      --output_dir        dir path
    """
    exit 0
}

// validate mode
if (!params.mode) {
    error "Missing required parameter: --mode. Must be 'mofa' or 'mefisto'."
}

if ( params.mode != 'mofa' && params.mode != 'mefisto' ) {
    throw new IllegalArgumentException("Invalid mode: ${params.mode}. Allowed values: mofa, mefisto")
}

// helper channels
mofa_ch = Channel.fromPath("${params.input_dir}/")
mefisto_ch = Channel.fromPath("${params.input_dir}/")

workflow {
    if ( params.mode == 'mofa' ) {
        mofa_model_ch = RUN_MOFA(mofa_ch)
        ANALYZE_MOFA(mofa_model_ch)
    } else {
        mefisto = RUN_MEFISTO(mefisto_ch)
        ANALYZE_MEFISTO()
    }
}
