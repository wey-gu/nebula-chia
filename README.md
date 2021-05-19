# nebula-chia

## How To Use

### ChaiBatchConvertor

#### Step 0, Installation

`nebula-chia` could be installed either via pip or from this git repo itself.

> Install via pip

```bash
python3 -m pip install nebula-chia
```
> Install from the github repo

```bash
git clone git@github.com:wey-gu/nebula-chia.git
cd nebula-chia
python3 setup.py install
```
#### Step 1, Convert Chia as CSV files

`ChiaBatchConvertor` is used to convert Chia Block Chain data into CSV files, which could then be used for nebula-importer

```bash
python3 -m pip install nebula-chia
$ ipython

# block_record_limit = 0 means unlimited
# coin_record_limit = 0 means unlimited
In [1]: from nebulachia.convertor import ChiaBatchConvertor

In [2]: c = ChaiBatchConvertor(block_record_limit=0, coin_record_limit=0, write_batch_size=10000)

In [3]: c.convert_block_record()

In [4]: c.convert_coin_record()

In [437]: ls -lth

-rw-r--r--   1 weyl  staff   173M May 19 13:01 coin_record.csv
-rw-r--r--   1 weyl  staff    77M May 19 12:59 block_record.csv
...

```