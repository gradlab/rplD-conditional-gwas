#!/usr/bin/env python

import sys
import argparse
import os
from datetime import datetime

def get_args():
    parser = argparse.ArgumentParser(description='Parse rRNA VCFs')
    parser.add_argument("dir23S", help="23S VCFs directory")
    parser.add_argument("dir16S", help="16S VCFs directory")
    return parser.parse_args()

args = get_args()

def parse_23S(sample):
    with open(f"{args.dir23S}/{sample}_pilon.vcf", "r") as infile:
        for line in infile:
            if line[0] != "#":
                line = line.strip().split()
                POS = line[1]
                INFO = line[7]
                if POS == "2603":
                    freqs_2603 = INFO.split(";")[6].split("=")[1].split(",")
                elif POS == "2051":
                    freqs_2051 = INFO.split(";")[6].split("=")[1].split(",")
        return {"2603":freqs_2603, "2051":freqs_2051}

def call_copy_number(freq_dict, position):
    copy_dict = {}
    for sample in freq_dict:
        if position == "2603":
            res_read_count = int(freq_dict[sample][position][3])
        else:
            res_read_count = int(freq_dict[sample][position][2])
        if res_read_count < 5:
            res_count = 0
        elif res_read_count < 38:
            res_count = 1
        elif res_read_count < 63:
            res_count = 2
        elif res_read_count < 88:
            res_count = 3
        else:
            res_count = 4
        copy_dict[sample] = res_count
    return copy_dict


def parse_16S(sample):
    with open(f"{args.dir16S}/{sample}_pilon.vcf", "r") as infile:
        for line in infile:
            if line[0] != "#":
               line = line.strip().split()
               POS = line[1]
               ALT = line[4]
               if POS == "1184":
                   if ALT == ".":
                       c1192t = "C"
                   else:
                       c1192t = ALT
               if POS == "464":
                   if ALT == ".":
                       g478t = "G"
                   else:
                       g478t = ALT
    return {"1192":c1192t, "478":g478t}

def write_itol_23S(copy_number_dict, colors, variant):
    with open(f"itol_{variant}.txt", "w") as itolfile:
        itolfile.write(f"DATASET_COLORSTRIP\nSEPARATOR TAB\nDATASET_LABEL\t{variant}\n")
        itolfile.write(f"COLOR\t{colors[-1]}\nLEGEND_TITLE\t{variant}\n")
        color_string = "\t".join(colors)
        itolfile.write(f"LEGEND_SHAPES\t1\t1\t1\t1\t1\nLEGEND_COLORS\t{color_string}\n")
        itolfile.write(f"LEGEND_LABELS\t0\t1\t2\t3\t4\n")
        itolfile.write("BORDER_WIDTH\t0.25\nBORDER_COLOR\t#CCCCCC\nDATA\n")
        for s in copy_number_dict:
            itolfile.write(f"{s}\t{colors[copy_number_dict[s]]}\t{str(copy_number_dict[s])}\n")

def write_itol_16S(allele_dict, colors, variant):
    with open(f"itol_{variant}.txt", "w") as itolfile:
        itolfile.write(f"DATASET_COLORSTRIP\nSEPARATOR TAB\nDATASET_LABEL\t{variant}\n")
        itolfile.write(f"COLOR\t{colors[1]}\nLEGEND_TITLE\t{variant}\n")
        color_string = "\t".join(colors)
        itolfile.write(f"LEGEND_SHAPES\t1\t1\nLEGEND_COLORS\t{color_string}\n")
        if variant == "16S_C1192T":
            itolfile.write(f"LEGEND_LABELS\tC\tT\n")
        else:
            itolfile.write(f"LEGEND_LABELS\tG\tT\n")
        itolfile.write("BORDER_WIDTH\t0.25\nBORDER_COLOR\t#CCCCCC\nDATA\n")
        for s in allele_dict:
            pos = ''.join(d for d in variant.split("_")[-1] if d.isdigit())
            if allele_dict[s][pos] == "C" and variant == "16S_C1192T":
                color = colors[0]
            elif allele_dict[s][pos] == "G" and variant == "16S_G478T":
                color = colors[0]
            elif allele_dict[s][pos] == "T" and variant == "16S_C1192T":
                color = colors[1]
            elif allele_dict[s][pos] == "T" and variant == "16S_G478T":
                color = colors[1]
            else:
                print(f"{variant} has new alternate allele, please edit script")
                sys.exit(0)
            itolfile.write(f"{s}\t{color}\t{str(allele_dict[s][pos])}\n")

def write_summary_table(A2059G, C2611T, alleles_16S):
    with open("rRNA_allele_summary.txt", "w") as outfile:
        outfile.write("sample\t23S_A2059G\t23S_C2611T\t16S_C1192T\t16S_G478T\n")
        for s in A2059G:
            pos_1192_16S = alleles_16S[s]["1192"]
            pos_478_16S = alleles_16S[s]["478"]
            outfile.write(f"{s}\t{A2059G[s]}\t{C2611T[s]}\t{pos_1192_16S}\t{pos_478_16S}\n")

samples = [f.strip("_pilon.vcf") for f in os.listdir(args.dir23S)]
dict_23S_freqs = {}
dict_16S_alleles = {}
for sample_name in samples:
    dict_23S_freqs[sample_name] = parse_23S(sample_name)
    dict_16S_alleles[sample_name] = parse_16S(sample_name)

copy_number_dict_A2059G = call_copy_number(dict_23S_freqs, "2051")
copy_number_dict_C2611T = call_copy_number(dict_23S_freqs, "2603")
write_itol_23S(copy_number_dict_A2059G, ["#ffffff", "#ffffcc", "#c2e699", "#78c679", "#238443"], "23S_A2059G")
write_itol_23S(copy_number_dict_C2611T, ["#ffffff", "#f6eff7", "#bdc9e1", "#67a9cf", "#02818a"], "23S_C2611T")
write_itol_16S(dict_16S_alleles, ["#b2e2e2", "#238b45"], "16S_C1192T")
write_itol_16S(dict_16S_alleles, ["#bae4bc", "#2b8cbe"], "16S_G478T")
write_summary_table(copy_number_dict_A2059G, copy_number_dict_C2611T, dict_16S_alleles)
