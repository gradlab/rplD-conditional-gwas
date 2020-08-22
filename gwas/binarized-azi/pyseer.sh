#!/bin/bash
#SBATCH -n 8
#SBATCH --mem-per-cpu=3G
#SBATCH -p priority
#SBATCH -t 0-06:00
#SBATCH -o gwas/binarized-azi/pyseer.out
#SBATCH -e gwas/binarized-azi/pyseer.err
#SBATCH --mail-type=END
#SBATCH --mail-user=kevinchenma@g.harvard.edu
#SBATCH --constraint="scratch3"

source activate pyseer
python /n/data1/hsph/immid/grad/Kevin/software/pyseer/pyseer-runner.py --phenotypes metadata/gwas-strain-table-binarized.tsv     --phenotype-column AZI_SUS --lmm --output-patterns gwas/binarized-azi/unitig_patterns.txt     --covariates metadata/combined-covariates.tsv --use-covariates 2 3 25 26     --kmers /n/data1/hsph/immid/grad/gonococcus/analyses/unitigs/2019-04/unitigs/unitigs.txt --uncompressed     --similarity gwas/popstruct/combined_phylogeny_similarity.tsv > gwas/binarized-azi/pyseer-AZI-BIN-cond-dataset-23S.results.txt 
