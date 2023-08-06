# IMAXT Registration Tools


## Install Instructions

### Create virtual environment

```
python -m venv ~/Python/registration
```

### Activate environment

```
source ~/Python/registration/bin/activate
```

### Install with pip

```
pip install -U imaxt-registration-tools
```


## Usage

```
usage: imaxtreg axio2stpt [-h] --stpt STPT --axio AXIO --output OUTPUT --pdf PDF [--verbose] [--nprocs NPROCS]
                          [--sections SECTIONS]

optional arguments:
  -h, --help           show this help message and exit
  --stpt STPT          Full path to STPT dataset
  --axio AXIO          Full path to AXIO dataset
  --output OUTPUT      Destination of output correspondence table (csv, parquet, npy, pkl)
  --pdf PDF            Destination of outout PDF quality control file
  --verbose            Verbose output
  --nprocs NPROCS      Number of processes to run in parallel (default 6)
  --sections SECTIONS  Comma separated list of AXIO sections to do (default is all)
```

To run, e.g.

```
imaxtreg axio2stpt --axio /storage/processed/axio/20220208_MPR_NSG_GFP_4T1_TdTOM_inflated_lung_Day21_200x15um_Axio \
                   --stpt /storage/processed/stpt/20220208_MPR_NSG_GFP_4T1_TdTOM_inflated_lung_Day21_200x15um \
                   --out 20220208_MPR_NSG_GFP_4T1_TdTOM_inflated_lung_Day21_200x15um.csv \
                   --pdf 20220208_MPR_NSG_GFP_4T1_TdTOM_inflated_lung_Day21_200x15um.pdf \
                   --verbose
```
