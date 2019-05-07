import argparse
import time
import os
from subprocess import check_call
from util import path_to_cmd


def run(gcta_path, bfile, out):
    out = os.path.join('file_cache', out)
    print(f'out_path: {out}')
    chrom_set = set()
    with open(f'{bfile}.bim', 'r') as bim_file:
        for line in bim_file:
            toks = line.split()
            chrom = toks[0]
            chrom_set.add(chrom)
    print(f'{len(chrom_set)} chromosomes in total')
    chrom_list = sorted(list(chrom_set))

    start_time = time.time()
    for chrom in chrom_list:
        print(f'chr{chrom}')
        check_call([path_to_cmd(gcta_path), '--bfile', bfile, '--chr', chrom, '--make-grm', '--out', f'{out}_{chrom}'])

    grm_dt = time.time() - start_time


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('gcta_path', type=str)
    parser.add_argument('bfile', type=str)
    parser.add_argument('--out', '-o', type=str)
    args = parser.parse_args()
    run(args.gcta_path, args.bfile, args.out)
