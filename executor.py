import argparse
from generate_individual_subset import generate_subset
from partition_by_chrom import partition
from bench_bolt_reml import bench_bolt_reml
import time
import sys


def print_time():
    print(time.strftime('%a %b %d %Y %H:%M:%S UTC%z', time.localtime()))


def run(bolt_path, plink_path, bfile, num_people, pheno_path, pheno_col, out):
    info = (f'=> generating subset individual data\n'
            f'bolt_path: {bolt_path}\n'
            f'plink_path: {plink_path}\n'
            f'bfile: {bfile}\n'
            f'num_people: {num_people}\n'
            f'pheno_filename: {pheno_path}\n'
            f'pheno_col: {pheno_col}\n'
            f'out: {out}\n')
    print(info)
    sys.stdout.flush()

    _, pheno_temp = generate_subset(plink_path=plink_path, bfile=bfile, num_people=num_people, out=out,
                                    pheno_path=pheno_path)
    print(f'subset pheno file: {pheno_temp}')

    print('=> assigning the SNP components by chromosome')
    sys.stdout.flush()
    snp_assignment_filename = out + '.snps_assignment'
    partition(out + '.bim', snp_assignment_filename)
    print('=> running BOLT-REML')
    print_time()
    sys.stdout.flush()
    dt = bench_bolt_reml(bolt_path, snp_assignment_filename, out + '.bed', out + '.bim', out + '.fam',
                         pheno_temp, pheno_col)
    with open(f'{out}.{num_people}.bench', 'w') as file:
        file.write(info)
        file.write(f'BOLT-REML took {dt} sec\n')
    print_time()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('bolt_path', type=str, help='path to the BOLT executable')
    parser.add_argument('plink_path', type=str, help='path to the plink executable')
    parser.add_argument('bfile', type=str, help='the prefix for the bed bim fam files')
    parser.add_argument('num_people', type=int, help='the number of individuals to be used in the benchmark')
    parser.add_argument('--out', '-o', help='analysis output prefix')
    parser.add_argument('--pheno', type=str, required=True, help='for the phenoFile option')
    parser.add_argument('--pheno-col', '-c', type=str, required=True,
                        help='phenotypes may be provided in a separate whitespace-delimited file '
                             '(specified with --phenoFile) with the first line containing column headers and '
                             'subsequent lines containing records, one per individual. '
                             'The first two columns must be FID and IID (the PLINK identifiers of an individual). '
                             'Any number of columns may follow; the column containing the phenotype to analyze is '
                             'specified with --phenoCol. Values of -9 and NA are interpreted as missing data. '
                             'All other values in the column should be numeric. The records in lines following the '
                             'header line need not be in sorted order and need not match the individuals in the '
                             'genotype data (i.e., fam file); BOLT-LMM and BOLT-REML will analyze only the individuals '
                             'in the intersection of the genotype and phenotype files and '
                             'will output a warning if these sets do not match.')
    args = parser.parse_args()
    run(bolt_path=args.bolt_path, plink_path=args.plink_path, bfile=args.bfile, num_people=args.num_people,
        pheno_path=args.pheno, pheno_col=args.pheno_col,
        out=f'{args.out}_{args.num_people}')
