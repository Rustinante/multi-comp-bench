# multi-comp-bench

Requires Python 3.6 and above

Example command for benchmarking BOLT:

On the top level directory, do this
```
python3 bolt_bencher.py ../BOLT-LMM_v2.3.2/bolt ../plink-1.07-x86_64/plink ../data/uk_filter4/filter4 30000 -o filter4_30000 --pheno=../data/uk_filter4/ex.pheno --pheno-col=pheno
```

Example command for benchmarking GCTA:

On the top level directory, do this
```
python3 gcta_bencher.py ../gcta_1.92.1beta6/gcta64 ../data/uk_filter4/filter4 ../plink-1.07-x86_64/plink 30000 --pheno ../data/uk_filter4/ex.pheno -o gcta
```

Help messages:

```
[aaron@veena multi-comp-bench]$ python3 bolt_bencher.py -h
usage: bolt_bencher.py [-h] [--out OUT] --pheno PHENO --pheno-col PHENO_COL
                       bolt_path plink_path bfile num_people

positional arguments:
  bolt_path             path to the BOLT executable
  plink_path            path to the plink executable
  bfile                 the prefix for the bed bim fam files
  num_people            the number of individuals to be used in the benchmark

optional arguments:
  -h, --help            show this help message and exit
  --out OUT, -o OUT     analysis output prefix
  --pheno PHENO         for the phenoFile option
  --pheno-col PHENO_COL, -c PHENO_COL
                        phenotypes may be provided in a separate whitespace-
                        delimited file (specified with --phenoFile) with the
                        first line containing column headers and subsequent
                        lines containing records, one per individual. The
                        first two columns must be FID and IID (the PLINK
                        identifiers of an individual). Any number of columns
                        may follow; the column containing the phenotype to
                        analyze is specified with --phenoCol. Values of -9 and
                        NA are interpreted as missing data. All other values
                        in the column should be numeric. The records in lines
                        following the header line need not be in sorted order
                        and need not match the individuals in the genotype
                        data (i.e., fam file); BOLT-LMM and BOLT-REML will
                        analyze only the individuals in the intersection of
                        the genotype and phenotype files and will output a
                        warning if these sets do not match.
```

```
[aaron@veena multi-comp-bench]$ python3 gcta_bencher.py -h
usage: gcta_bencher.py [-h] --pheno PHENO --out-id OUT_ID
                       gcta_path bfile plink_path num_people

positional arguments:
  gcta_path
  bfile
  plink_path            path to the plink executable
  num_people            the number of individuals to be used in the benchmark

optional arguments:
  -h, --help            show this help message and exit
  --pheno PHENO         path to the phenotype files
  --out-id OUT_ID, -o OUT_ID
                        an indentifier for logging output
```
