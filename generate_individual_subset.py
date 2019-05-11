import argparse
from subprocess import check_call

from util import path_to_cmd


def generate_subset(plink_path, bfile, num_people, out, pheno_path=None):
    subset_fam_path = out + f'.subset_{num_people}.fam'
    print(f'\n=> creating a temp fam file for the subset of {num_people} individuals at {subset_fam_path}')
    individual_id_list = []
    with open(bfile + '.fam', 'r') as fam_file, open(subset_fam_path, 'w') as temp_fam:
        for i, line in zip(range(num_people), fam_file):
            temp_fam.write(line)
            if pheno_path is not None:
                individual_id_list.append(line.split()[1])

    check_call([path_to_cmd(plink_path), '--make-bed', '--bfile', bfile, '--keep', subset_fam_path, '--out', out])

    individual_id_set = set(individual_id_list)
    pheno_dict = {}
    subset_pheno_path = None
    if pheno_path is not None:
        subset_pheno_path = out + f'.subset_{num_people}.pheno'
        print(f'\n=> writing subset phenotypes to {subset_pheno_path}')
        with open(pheno_path, 'r') as file:
            header = file.readline()
            for line in file:
                individual_id = line.split()[1]
                if individual_id in individual_id_set:
                    pheno_dict[individual_id] = line

        with open(subset_pheno_path, 'w') as subset_pheno_file:
            subset_pheno_file.write(header)
            for iid in individual_id_list:
                subset_pheno_file.write(pheno_dict[iid])

    return subset_fam_path, subset_pheno_path


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('plink_path', type=str, help='path to the plink executable')
    parser.add_argument('bfile', type=str, help='the prefix for the bed bim fam files')
    parser.add_argument('num_people', type=int, help='the number of individuals to be used in the benchmark')
    parser.add_argument('--out', '-o', type=str, help='output bfile prefix')
    args = parser.parse_args()
    generate_subset(plink_path=args.plink_path, bfile=args.bfile, num_people=args.num_people, out=args.out)
