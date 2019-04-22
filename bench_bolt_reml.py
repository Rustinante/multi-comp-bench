import argparse
import time
from subprocess import check_call
import os


def bench_bolt_reml(exe_path, snp_assignment_filename, bed_filename, bim_filename, fam_filename,
                    pheno_filename, pheno_col):
    time_stamp = time.time()
    if exe_path.startswith('.') or exe_path.startswith('/'):
        cmd = exe_path
    else:
        cmd = os.path.join('.', exe_path)

    check_call([cmd, '--reml',
                '--modelSnps', snp_assignment_filename,
                '--bed', bed_filename,
                '--bim', bim_filename,
                '--fam', fam_filename,
                '--phenoFile', pheno_filename,
                '--phenoCol', pheno_col])
    dt = time.time() - time_stamp
    print(f'bolt-reml took: {dt:.2f} seconds')
    return dt


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('exe_path', type=str)
    parser.add_argument('--snp-assign', '-s', type=str, required=True,
                        help='The file assigning each SNP to a variance component, '
                             'in which each whitespace-delimited line contains a SNP ID (typically an rs number) '
                             'followed by the name of the variance component to which it belongs.')
    parser.add_argument('--bed', type=str, required=True)
    parser.add_argument('--bim', type=str, required=True)
    parser.add_argument('--fam', type=str, required=True)
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
    bench_bolt_reml(args.exe_path, args.snp_assign, args.bed, args.bim, args.fam, args.pheno, args.pheno_col)
