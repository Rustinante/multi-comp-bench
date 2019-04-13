import argparse


def chrom_to_number(chrom):
    def to_int(tail):
        if tail.isnumeric():
            return int(tail)
        else:
            if tail.lower() == 'X':
                return 23
            elif tail.lower() == 'Y':
                return 24
            else:
                raise ValueError(f'unrecognized chromosome: {chrom}')

    if chrom.lower().startswith('chr'):
        return to_int(chrom[3:])
    else:
        return to_int(chrom)


def partition(bim_filename, out):
    with open(bim_filename, 'r') as file, open(out, 'w') as out_file:
        for line in file:
            toks = line.split()
            chrom = toks[0]
            rsid = toks[1]
            out_file.write(f'{rsid} {chrom_to_number(chrom)}\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('bim_file', type=str)
    parser.add_argument('--out', '-o', type=str)
    args = parser.parse_args()
    partition(args.bim_file, args.out)
