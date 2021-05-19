# nebula-chia

## How To Use

### ChaiBatchConvertor

`ChaiBatchConvertor` is used to convert Chia Block Chain data into CSV files, which could then be used for nebula-importer

```bash
$ ipython

# block_record_limit = 0 means unlimited
# coin_record_limit = 0 means unlimited
In [1]: c = ChaiBatchConvertor(block_record_limit=0, coin_record_limit=0, write_batch_size=10000)

In [2]: c.convert_block_record()

In [3]: c.convert_coin_record()

In [437]: ls -lth

-rw-r--r--   1 weyl  staff   173M May 19 13:01 coin_record.csv
-rw-r--r--   1 weyl  staff    77M May 19 12:59 block_record.csv
...

```