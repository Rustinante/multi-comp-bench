import argparse
import os
import sys
import time
from subprocess import check_call

from generate_individual_subset import generate_subset
from util import path_to_cmd, print_time


def run(gcta_path, plink_path, bfile, pheno_path, num_people, out_id):
    info = (f'gcta_path: {gcta_path}\n'
            f'plink_path: {plink_path}\n'
            f'bfile: {bfile}\n'
            f'pheno_path: {pheno_path}\n'
            f'num_people: {num_people}\n'
            f'out: {out_id}')

    print(info)
    sys.stdout.flush()

    os.makedirs('file_cache', exist_ok=True)
    out_path = os.path.join('file_cache', out_id)
    print(f'out_path: {out_path}')
    chrom_set = set()
    with open(f'{bfile}.bim', 'r') as bim_file:
        for line in bim_file:
            toks = line.split()
            chrom = toks[0]
            chrom_set.add(chrom)
    print(f'{len(chrom_set)} chromosomes in total')
    chrom_list = sorted(list(chrom_set))

    _, pheno_temp = generate_subset(plink_path=plink_path, bfile=bfile, num_people=num_people, out=out_path,
                                    pheno_path=pheno_path)
    print(f'subset pheno file: {pheno_temp}')

    print_time()
    start_time = time.time()
    for chrom in chrom_list:
        print(f'chr{chrom}')
        check_call(
            [path_to_cmd(gcta_path), '--bfile', out_path, '--chr', chrom, '--make-grm', '--out', f'{out_path}_{chrom}'])
        print_time()

    grm_dt = time.time() - start_time
    print(f'GRM computation took {grm_dt} seconds')

    grm_catalog = os.path.join('file_cache', f'{out_id}_grm_catalog.txt')
    with open(grm_catalog, 'w') as file:
        for chrom in chrom_list:
            file.write(f'{out_path}_{chrom}\n')

    start_time = time.time()
    print('\n=> running GCTA reml')
    print_time()
    os.makedirs('output', exist_ok=True)
    gcta_out_path = os.path.join('output', f'gcta_{out_id}_{num_people}')
    check_call([path_to_cmd(gcta_path), '--reml', '--mgrm', grm_catalog, '--pheno', pheno_temp, '--out', gcta_out_path])

    gcta_dt = time.time() - start_time
    print(f'GCTA reml took: {gcta_dt} seconds')
    print_time()
    print(f'Total time: {grm_dt + gcta_dt} seconds')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('gcta_path', type=str)
    parser.add_argument('bfile', type=str)
    parser.add_argument('plink_path', type=str, help='path to the plink executable')
    parser.add_argument('num_people', type=int, help='the number of individuals to be used in the benchmark')
    parser.add_argument('--pheno', type=str, required=True, help='path to the phenotype files')
    parser.add_argument('--out-id', '-o', type=str, required=True, help='an indentifier for logging output')
    args = parser.parse_args()
    run(gcta_path=args.gcta_path, plink_path=args.plink_path,
        bfile=args.bfile, pheno_path=args.pheno, num_people=args.num_people, out_id=args.out_id)
