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

    os.makedirs('file_cache', exist_ok=True)
    file_cache_out_path = os.path.join('file_cache', f'{out_id}_{num_people}')
    print(info)
    print(f'file_cache_out_path: {file_cache_out_path}')
    sys.stdout.flush()

    chrom_set = set()
    with open(f'{bfile}.bim', 'r') as bim_file:
        for line in bim_file:
            toks = line.split()
            chrom = toks[0]
            chrom_set.add(chrom)
    print(f'{len(chrom_set)} chromosomes in total')
    chrom_list = sorted(list(chrom_set))

    print(f'\n=> generating data for a subset of {num_people} individuals')
    print_time()
    sys.stdout.flush()
    _, pheno_temp = generate_subset(plink_path=plink_path, bfile=bfile, num_people=num_people, out=file_cache_out_path,
                                    pheno_path=pheno_path)
    print(f'subset pheno file: {pheno_temp}')

    start_time = time.time()
    chrom_time_list = []
    for chrom in chrom_list:
        print(f'\n=> chr{chrom}')
        print_time()
        sys.stdout.flush()
        chrom_time_start = time.time()
        check_call(
            [path_to_cmd(gcta_path), '--bfile', file_cache_out_path, '--chr', chrom, '--make-grm',
             '--out', f'{file_cache_out_path}_{chrom}'])
        chrom_time_list.append((chrom, time.time() - chrom_time_start))
        print(f'\n=> chr{chrom} finished')
        print_time()
        sys.stdout.flush()

    grm_dt = time.time() - start_time
    print(f'GRM computation took {grm_dt} seconds')
    sys.stdout.flush()

    grm_catalog = os.path.join('file_cache', f'{out_id}_{num_people}_grm_catalog.txt')
    with open(grm_catalog, 'w') as file:
        for chrom in chrom_list:
            file.write(f'{file_cache_out_path}_{chrom}\n')

    os.makedirs('output', exist_ok=True)
    log_path_prefix = os.path.join('output', f'{out_id}_{num_people}')
    print(f'log_path_prefix: {log_path_prefix}')

    print('\n=> running GCTA reml')
    print_time()
    sys.stdout.flush()
    start_time = time.time()
    check_call(
        [path_to_cmd(gcta_path), '--reml', '--mgrm', grm_catalog, '--pheno', pheno_temp, '--out', log_path_prefix])

    print('\n=> GCTA reml finished')
    print_time()

    gcta_dt = time.time() - start_time
    print(f'GCTA reml took: {gcta_dt} seconds')
    print(f'Total time: {grm_dt + gcta_dt} seconds')
    sys.stdout.flush()

    bencher_file = f'{log_path_prefix}.bench'
    with open(bencher_file, 'w') as file:
        file.write(info)
        file.write('GRM computation time by chromosome:\n')
        for chrom, chrom_time in chrom_time_list:
            file.write(f'chr{chrom} {chrom_time}\n')
        file.write('-' * 10 + f'\nIn total, GRM computation took {grm_dt} sec\n')
        file.write(f'GCTA REML took {gcta_dt} sec\n')
        file.write(f'total time: {grm_dt + gcta_dt} sec\n')


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
