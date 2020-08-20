#!/bin/bash
#SBATCH -n 8
#SBATCH --mem-per-cpu=3G
#SBATCH -p priority
#SBATCH -t 0-06:00
#SBATCH -o gwas/cond-dataset/pyseer.out
#SBATCH -e gwas/cond-dataset/pyseer.err
#SBATCH --mail-type=END
#SBATCH --mail-user=kevinchenma@g.harvard.edu
#SBATCH --constraint="scratch2"

source activate pyseer
python /n/data1/hsph/immid/grad/Kevin/software/pyseer/pyseer-runner.py --phenotypes metadata/gwas-strain-table-filtered.tsv     --phenotype-column AZI_LOG --lmm --output-patterns gwas/cond-dataset/unitig_patterns.txt     --covariates metadata/gwas-strain-table-filtered.tsv --use-covariates 2 3     --kmers /n/data1/hsph/immid/grad/gonococcus/analyses/unitigs/2019-04/unitigs/unitigs.txt --uncompressed     --similarity gwas/popstruct/combined_phylogeny_similarity.tsv > gwas/cond-dataset/pyseer-AZI-cond-dataset.results.txt 
