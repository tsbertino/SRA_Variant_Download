# SRA_Variant_Download

---

## Overview

A simple script that downloads specified SNPs from publically available data. A modified bed file (saved as a csv), and a modified SRA Run Table (csv) are taken as an input and each variant is downloaded for each individual and then merged, for later processing. 

Included are example input files using one reference SNP, rs4988235, for lactase persistence, and individuals made available publically on the SRA/ENA from [Mathieson et al. 2015](https://www.nature.com/articles/nature16152). The pipeline and files are explained further below.

---

## Input Formats

### BED File Input

The script takes two BED files as an input, [one](snpBedFile_example.bed) is a correct .bed that specifies position and reference allele, and [a modified version](bedfile_example.csv) of this that contains extra meta data saved as a csv, used for downloading and labeling. 

The pipeline will download a region +- a certain distance around the variant (`range` variable), and as many variants can be included as are needed. The default `range` is 10000. 

The basic format of the actual BED is here:

|chrom|chromStart|chromEnd|refAllele|altAllele|detail|
|-|-|-|-|-|-|
|2|136608645|136608646|G|A|rs4988235

The basic format of the modified csv is here:

|chrom|chromStart|chromEnd|refSNP|gene|detail|
|-|-|-|-|-|-|
|2|136608645|136608646|rs4988235|MCM6_LCT|Lactase_Persistence

### Accession File

The second file, the [accession file](SRA_example.csv), is a modification of an SRA RunTable, that contains all necessary information about the individual, publication, and accession/run number.

This information is reach via the [SRA Run Selector](https://www.ncbi.nlm.nih.gov/Traces/study/?), by inputting an 'Accession Number'. For Mathieson et al. 2015, this is `PRJEB11450`, found in the footnotes. 

Inputting this into the SRA Run Selector allows the option to download either strictly the accession number of all runs in the project, or the 'metadata', which contains all relevant information and is downloaded in a comma delimited text file, 'SraRunTable.txt'. ([Unmodified version included here as an example](SraRunTable.txt)).


The important fields are (as labeled in the header of the SraRunTable), 'Alias', 'Run' 'BioProject'.

I modify and save this as a csv manually, as the specifics can vary (which individuals to use, mtDNA runs, etc.)

Basic layout:

|Alias|Run|BioProject|
|-----|---|----------|
|na|na|na|

With data:

|Alias|Run|BioProject|
|-----|---|----------|
|I0049|ERR1136339|PRJEB11450|
|I0103|ERR1136348|PRJEB11450|
|I0104|ERR1136349|PRJEB11450|
|I0106|ERR1136350|PRJEB11450|
|I0357|ERR1136376|PRJEB11450|

As currently used in the script I removed the header:

||||
|-----|---|----------|
|I0049|ERR1136339|PRJEB11450|
|I0103|ERR1136348|PRJEB11450|
|I0104|ERR1136349|PRJEB11450|
|I0106|ERR1136350|PRJEB11450|
|I0357|ERR1136376|PRJEB11450|

---

## Pipeline

As it exists the script essentially does this:

Within a `/bams` directory, creates a `/merged_bams` and `/emit_all_vcfs` directory. Within the `/bams` directory, a directory is created for each individual (i.e. 'I0049'). The script uses sratoolkit `samdump` to download the aligned regions as a bam, and then merges them. This merged bam is sorted, duplicates are marked, and the whole thing is indexed, and moved into the `/merged_bams` directory. Moving into this directory, I use [GenoCaller_indent](https://github.com/kveeramah/GenoCaller_indent) to call emit all vcfs, and then sort them. This is moved into the `emit_all_vcfs` directory. Once all are done, a list of vcfs is created and I use [merge_vcf](https://github.com/kveeramah/merge_vcf) to merge them. The vcfs are labeled with the individual and publication and then can be used later.




