import argparse
from subprocess import check_call
import os


def generate_subset(plink_path, bfile, num_people, out):
    if plink_path.startswith('.') or plink_path.startswith('/'):
        cmd = plink_path
    else:
        cmd = os.path.join('.', plink_path)

    keep = bfile + f'.subset_{num_people}.temp'
    print(f'creating a temp fam file for the subset of {num_people} individuals at {keep}')
    with open(bfile + '.fam', 'r') as fam_file, open(keep, 'w') as temp_fam:
        for i, line in zip(range(num_people), fam_file):
            temp_fam.write(line)

    check_call([cmd, '--make-bed', '--bfile', bfile, '--keep', keep, '--out', out])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('plink_path', type=str, help='path to the plink executable')
    parser.add_argument('bfile', type=str, help='the prefix for the bed bim fam files')
    parser.add_argument('num_people', type=int, help='the number of individuals to be used in the benchmark')
    parser.add_argument('--out', '-o', type=str, help='output bfile prefix')
    args = parser.parse_args()
    generate_subset(plink_path=args.plink_path, bfile=args.bfile, num_people=args.num_people, out=args.out)
