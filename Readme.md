# AtMoDat_CVs

This repository contains lists of mandatory/required, recommended and optional global attributes and controlled vocabularies (CVs) for values of these attributes for the ATMODAT Standard. 

The lists/CVs are stored in two formats:
* [JSON files](AtMoDat_CV_json). The structure is the same as of the [CMIP6_CVs](https://github.com/WCRP-CMIP/CMIP6_CVs/).
* [pyessv archive](pyessv-archive/atmodat)

## Disclaimer

The script to create the pyessv archive is based on this script https://github.com/ES-DOC/pyessv/blob/master/sh/writers/wcrp/cmip6/write.py (commit 1e2afa2) in the pyessv repository.

## Create pyessv archive

1. Clone this repository:
```
git clone https://github.com/AtMoDat/AtMoDat_CVs.git
```

2. Install Python 3 via conda if necessary:
```
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
sh Miniconda3-latest-Linux-x86_64.sh -p $HOME/miniconda3 -b
rm -f Miniconda3-latest-Linux-x86_64.sh
```

3. Create conda environment:
```
conda create --name atmodat_CVs -y
conda activate atmodat_CVs
```

4. Install pyessv
```
python -m pip install git+https://github.com/ES-DOC/pyessv 
```

5. Point pyessv to the "archive" where AtMoDat controlled vocabulary is supposed to be stored
```
Linux: export PYESSV_ARCHIVE_HOME=$PWD/pyessv-archive 
Windows: set PYESSV_ARCHIVE_HOME=%cd%/pyessv-archive 
```

6. Create pyessv archive
```
python create_atmodat_pyessv_archive.py --source AtMoDat_CV_json
```

## Contributors:

In alphabetic order:

* [Amandine Kaiser](https://github.com/am-kaiser), [ORCID: 0000-0002-2756-9964](https://orcid.org/0000-0002-2756-9964)
* [Anette Ganske](https://github.com/anganske), [ORCID: 0000-0003-1043-4964 
](https://orcid.org/0000-0003-1043-4964)
* Angelina Kraft, [ORCID: 0000-0002-6454-335X](https://orcid.org/0000-0002-6454-335X)
* [Daniel Heydebreck](https://github.com/neumannd), [ORCID: 0000-0001-8574-9093](https://orcid.org/0000-0001-8574-9093)
* Hannes Thiemann, [ORCID: 0000-0002-2329-8511](https://orcid.org/0000-0002-2329-8511)
* Heinke Hoeck, [ORCID: 0000-0002-0131-1404](https://orcid.org/0000-0002-0131-1404)
* Jan Kretzschmar, [ORCID: 0000-0002-8013-5831](http://orcid.org/0000-0002-8013-5831)

## Acknowledgements:

The ATMODAT Standard was created within the AtMoDat project (Atmospheric Model Data, https://www.atmodat.de). AtMoDat is funded by the German Federal Ministry for Education and Research within the framework of Atmosphaeren-Modelldaten: Datenqualitaet, Kurationskriterien und DOI-Branding (FKZ 16QK02A).
