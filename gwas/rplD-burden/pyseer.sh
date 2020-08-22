#!/bin/bash
#SBATCH -n 8
#SBATCH --mem-per-cpu=3G
#SBATCH -p priority
#SBATCH -t 0-01:00
#SBATCH -o gwas/rplD-burden/pyseer.out
#SBATCH -e gwas/rplD-burden/pyseer.err
#SBATCH --mail-type=END
#SBATCH --mail-user=kevinchenma@g.harvard.edu
#SBATCH --constraint="scratch3"

source activate pyseer
python /n/data1/hsph/immid/grad/Kevin/software/pyseer/pyseer-runner.py --phenotypes metadata/gwas-strain-table-filtered.tsv     --phenotype-column AZI_LOG --lmm --output-patterns gwas/rplD-burden/unitig_patterns.txt     --covariates metadata/combined-covariates.tsv --use-covariates 2 3 25 26     --kmers gwas/rplD-burden/rplD-unitig.txt --uncompressed     --similarity gwas/popstruct/combined_phylogeny_similarity.tsv > gwas/rplD-burden/pyseer-AZI-rplD-unitig-cond-dataset-23S.results.txt 
