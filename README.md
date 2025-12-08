# Multi-omic interpretable spatio-temporal factor analysis workflow

*by Younginn Park*

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Scanpy](https://img.shields.io/badge/Scanpy-f46e32?style=for-the-badge&logo=python&logoColor=white)
![MOFA2](https://img.shields.io/badge/MOFA2-157c74?style=for-the-badge&logo=python&logoColor=white)
![MEFISTO](https://img.shields.io/badge/Mefisto-15905f?style=for-the-badge&logo=python&logoColor=white)
![Nextflow](https://img.shields.io/badge/Nextflow-DSL2-23CC85?style=for-the-badge&logo=nextflow&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

<p align="center">
    <img src="https://raw.githubusercontent.com/young-sudo/mo-flow/main/img/DL_logo_header.png" alt="DL_logo">
</p>

This project was inspired by the 4EU+ Deep Learning in Life Sciences lab by prof. Britta Velten (Heidelberg University).

Aim of the project is to transform the original coursework into a reproducible workflow that can be executed reliably across different environments beyond Google Colab.

Project involves frameworks MOFA2 and MEFISTO.
1. Application of MOFA to a multi-omics data set (gene expression, methylation, mutations and drug responses)
2. Application of MEFISTO to a longitudinal data set (gene expression measurement samples over developmental time in multiple species and organs)

# Usage

**Project in Active Development**

# Methods

_Based on 4EU+ DeepLife coursework materials_

## MOFA

<p align="center" style="margin-top: 10px; margin-bottom: 15px;">
    <img src="https://raw.githubusercontent.com/young-sudo/mo-flow/main/img/mofa.png" alt="mofa_r2" width=400>
    <br>
    <img src="https://raw.githubusercontent.com/young-sudo/mo-flow/main/img/mofa_prob_factor_model.png" alt="mofa_prob" width=400>
    <br>
    <img src="https://raw.githubusercontent.com/young-sudo/mo-flow/main/img/mofa_precision_med.png" alt="mofa_pm" width=400>
    <br>
    <small>(1) Multi-modal factor analysis (MOFA) diagram. (2) The probabilistic factor model behind MOFA. (3) Example use case of MOFA's variance decomposition, inspection of weights, and dimensionality reduced visualization of samples capabilities - Precision Medicine</small>
</p>

The following section shows how to use the `muon` package to apply the factor model MOFA (Multi-Omics Factor Analysis) to integrate multi-omics data. The code is based on [this](https://muon-tutorials.readthedocs.io/en/latest/CLL.html) tutorial. We apply MOFA to a multi-omics data set, in which various data modalities have been measured in primary cancer cells of 200 individual patients with chronic lymphocytic leukemia (CLL). For more details on the data please see a detailed analysis in the [original publication](https://www.huber.embl.de/pub/pdf/Dietrich2018.pdf).

Count matrices and metadata of the multi-omics CLL study are publicly available as part of the [MOFAdata R package](http://bioconductor.org/packages/release/data/experiment/html/MOFAdata.html). For the purpose of this notebook, those matrices were saved in individual `.csv` files in the `data/` folder. Please make sure to add this folder to your local directory. The data set consists of the following four modalities:  
1. mRNA: normalized expression of 5000 variable genes
2. methylation: methylation state of 4248 CpG locations
3. mutations: occurrence of insertions or deletions at 69 DNA regions
4. drugs: ex vivo drug sensitivity measurements for 310 drugs

The data per modality is stored in the `AnnData` format (more infos about the Anndata structure [here](https://anndata.readthedocs.io/en/latest/)). This format is typically also used in single cell analysis, e.g. by the package `scanpy`. The value matrices can be accessed using `.X`, the row names are stored under `.obs_names` and the column names under `.var_names`.

A data frame with some additional information about each patient which includes:
- Gender: m (male), f (female)
- Age: age in years
- TTT: time (in years) between taking the sample to the next treatment
- TTD: time (in years) between taking the sample to patients' death
- treatedAfter: True/False indicating whether patient has been treated
- Died: True/False indicating whether the patient died

To create a multi-modal data object from the dictionary containing the four single modalities, we use the package `muon`. `muon` allows to directly run MOFA on this `MuData` object. If you want to learn more about `muon`, check out its [documentation](https://muon.readthedocs.io/en/latest/notebooks/quickstart_mudata.html) or [paper](https://link.springer.com/article/10.1186/s13059-021-02577-8).

**Multi-omics factor analysis** (MOFA) integration can be run on a MuData object with a single command:

```
mu.tl.mofa()
```

<p align="center" style="margin-top: 10px; margin-bottom: 10px;">
    <img src="https://raw.githubusercontent.com/young-sudo/mo-flow/main/img/mofa_r2.png" alt="mofa_r2" width=400>
    <br>
    <img src="https://raw.githubusercontent.com/young-sudo/mo-flow/main/img/mofa_factors_metadata.png" alt="f1_weights" width=500>
    <br>
    <small>Factor variability plot (R2) and factor space plots with metadata features indicated by color, shape, and size</small>
</p>

### Results

Let's have a look at the model output and analyse what is captured in the latent factors. For this, we are using the `mofax` package to load our trained model and then plot the amount of variance that each factor explains across the data modalities.

<p align="center" style="margin-top: 10px; margin-bottom: 10px;">
    <img src="https://raw.githubusercontent.com/young-sudo/mo-flow/main/img/f1_weights.png" alt="f1_weights" width=700>
    <br>
    <small>Factor 1 feature weight plots with the features with the highest absolute weights labeled</small>
</p>

We can see that in the mutations modality IGHV has a much higher absolute weight than all other features. Additionally, the top weights from the RNA modality are likely to represent the same latent process as IGHV status:

- ENSG00000198046 &rarr; ZNF667 — lnc‐ZNF667‐AS1 [is associated with poor survival and is a promising prognostic biomarker](https://onlinelibrary.wiley.com/doi/abs/10.1111/ijlh.13167)
- ENSG00000186522 &rarr; SEPT10 – its expression [correlates with IGHV status](https://www.nature.com/articles/2404220) (however [there are some caveats](https://www.nature.com/articles/2404867))
- ENSG00000198142 &rarr; SOWAHC – it [has been identified as a prognostic marker for other cancers](https://www.spandidos-publications.com/mmr/21/3/1285)

Focusing on the drug response, we notice PF477736 (D_078), AZD7762 (D_020), AT13387 (D_017), and dasatinib (D_050) have the major association with this factor. Those are the exact top associations with the IGHV status [described in the original paper](https://www.huber.embl.de/pub/pdf/Dietrich2018.pdf).

<p align="center" style="margin-top: 10px; margin-bottom: 10px;">
    <img src="https://raw.githubusercontent.com/young-sudo/mo-flow/main/img/F1_F2_ighv_tri12.png" alt="f1_f2" width=600>
    <br>
    <small>Samples visualized in a factor space with Factors 1 and 2 acting as main axes and features IGHV and trisomy 12 used for visualization.</small>
</p>

## MEFISTO

MEFISTO (A Method for the Functional Integration of Spatial and Temporal Omics data)

<p align="center" style="margin-top: 10px; margin-bottom: 10px;">
    <img src="https://raw.githubusercontent.com/young-sudo/mo-flow/main/img/mefisto.png" alt="mefisto" width=600>
    <br>
    <small>MEFISTO diagram</small>
</p>

# References

Argelaguet, R., Velten, B., Arnol, D. et al. Multi‐Omics Factor Analysis—a framework for unsupervised integration of multi‐omics data sets. Mol Syst Biol 14, MSB178124 (2018). [https://doi.org/10.15252/msb.20178124](https://doi.org/10.15252/msb.20178124)

Argelaguet, R., Arnol, D., Bredikhin, D., Deloro, Y., Velten, B., Marioni, J. C., & Stegle, O. (2020). MOFA+: a statistical framework for comprehensive integration of multi-modal single-cell data. Genome biology, 21(1), 111. [https://doi.org/10.1186/s13059-020-02015-1](https://doi.org/10.1186/s13059-020-02015-1)

Velten, B., Braunger, J.M., Argelaguet, R. et al. Identifying temporal and spatial patterns of variation from multimodal data using MEFISTO. Nat Methods 19, 179–186 (2022). [https://doi.org/10.1038/s41592-021-01343-9](https://doi.org/10.1038/s41592-021-01343-9)
