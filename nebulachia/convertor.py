import os
import sqlite3

from chia.consensus.block_record import BlockRecord
from chia.util.ints import uint32, uint64


DEFAULT_DB_PATH = "~/.chia/mainnet/db/blockchain_v1_mainnet.sqlite"
DEFAULT_BLOCK_RECORD_LIMIT = 10000
DEFAULT_COIN_RECORD_LIMIT = 10000

BLOCKRECORD_FILENAME = "block_record.csv"
COINRECORD_FILENAME = "coin_record.csv"
DEFAULT_OUTPUT_PATH = os.getcwd()
CSV_WRITE_BATCH = 10000


class ChiaBatchConvertor:
    def __init__(self, db_path=None, output_path=None,
                 block_record_limit=None, coin_record_limit=None,
                 write_batch_size=None):
        """
        Initilization for ChiaBatchConvertor.
        """
        if db_path is None:
            db_path = os.path.expanduser(DEFAULT_DB_PATH)
        self.db_path = db_path
        self.db_con = sqlite3.connect(self.db_path)

        if output_path is None:
            output_path = DEFAULT_OUTPUT_PATH
        self.output_path = output_path

        if block_record_limit is None:
            block_record_limit = DEFAULT_BLOCK_RECORD_LIMIT
        self.block_limit = block_record_limit

        if coin_record_limit is None:
            coin_record_limit = DEFAULT_COIN_RECORD_LIMIT
        self.coin_limit = coin_record_limit

        if write_batch_size is None:
            write_batch_size = CSV_WRITE_BATCH
        self.write_batch_size = write_batch_size

    def convert_block_record(self):
        """
        Parse block record and convert the record into CSV lines.
        """
        file_path = f"{ self.output_path }/{ BLOCKRECORD_FILENAME }"
        block_record_query = "SELECT * FROM block_records"

        if self.block_limit > 0:
            block_record_query = block_record_query + f" LIMIT { self.block_limit }"
        cur = self.db_con.cursor()
        rows_iterator = cur.execute(block_record_query)

        self._csv_writer(
            file_path, rows_iterator,
            self.block_record_row, self.write_batch_size)


    def convert_coin_record(self):
        """
        Parse coin record and convert the record into CSV lines.
        """
        file_path = f"{ self.output_path }/{ COINRECORD_FILENAME }"
        coin_record_query = "SELECT * FROM coin_record"

        if self.coin_limit > 0:
            coin_record_query = coin_record_query + f" LIMIT { self.coin_limit }"
        cur = self.db_con.cursor()
        rows_iterator = cur.execute(coin_record_query)

        self._csv_writer(
            file_path, rows_iterator,
            self.coin_record_row, self.write_batch_size)

    @staticmethod
    def _csv_writer(file_path, iterator, row_formator, buffer_size):
        with open(file_path, mode='w') as file:
            writer = csv.writer(
                file, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
            csv_buffer = list()
            for row in iterator:
                csv_buffer.append(row_formator(row))
                if len(csv_buffer) > buffer_size:
                    writer.writerows(csv_buffer)
                    del csv_buffer[:]
            if csv_buffer:
                writer.writerows(csv_buffer)
                del csv_buffer[:]

    @staticmethod
    def _to_bool(value):
        """
        tinyint to string bool in lower case.
        """
        return "false" if value in [0, "0"] else "true"

    def block_record_row(self, row):
        """
        Parse row and return a CSV block record row list.

        CREATE TABLE block_records(
          header_hash text PRIMARY KEY, 
          prev_hash text, 
          height bigint,
          block blob,
          sub_epoch_summary blob, 
          is_peak tinyint, 
          is_block tinyint)

        Block Record CSV Head:
            0           1         2(int) 3(bool) 4(bool)
            header_hash|prev_hash|height|is_peak|is_block|

            5(int)
            deficit|

            6
            challenge_block_info_hash|

            7
            farmer_puzzle_hash|

            8(int)
            fees|

            9
            prev_transaction_block_hash|

            10
            prev_transaction_block_height|

            11             12(int)
            required_iters|signage_point_index|

            13(timestamp)
            timestamp
        """
        rec = BlockRecord.from_bytes(row[3])
        row_list = (
            row[0], row[1], str(row[2]), self._to_bool(row[5]), self._to_bool(row[6]),
            str(rec.deficit.real),
            str(rec.challenge_block_info_hash) if rec.challenge_block_info_hash else str(),
            str(rec.farmer_puzzle_hash) if rec.farmer_puzzle_hash else str(),
            str(0 if rec.fees is None else rec.fees),
            str(rec.prev_transaction_block_hash) if rec.prev_transaction_block_hash else str(),
            str(rec.prev_transaction_block_height),
            str(rec.required_iters), str(rec.signage_point_index),
            str(0 if rec.timestamp is None else rec.timestamp)
            )
        return row_list

    def _height_to_hash(self, height):
        cur = self.db_con.cursor()
        if height == 0:
            return "0"
        query_string = f"SELECT * FROM block_records WHERE height = { height }"
        query_result = list(cur.execute(query_string))
        if query_result:
            return query_result[0][1]
        else:
            print(f"[ERROR] failed during { query_string }")
            raise

    def coin_record_row(self, row):
        """
        Parse row and return a CSV block coin row list.

        CREATE TABLE coin_record(
          coin_name text PRIMARY KEY,
          confirmed_index bigint,
          spent_index bigint,
          spent int,
          coinbase int,
          puzzle_hash text,
          coin_parent text,
          amount blob,
          timestamp bigint)

        Coin Record CSV Head:
            0         1(int)          2(int)      3(bool)
            coin_name|confirmed_index|spent_index|spent|

            4(bool)  5           6           7(int)
            coinbase|puzzle_hash|coin_parent|amount|

            8(timestamp)
            timestamp|

            9              10
            confirmed_hash|spent_hash
        """
        row_list = (
            row[0], str(row[1]), str(row[2]), self._to_bool(row[3]),
            self._to_bool(row[4]), row[5], row[6], str(uint64.from_bytes(row[7])),
            str(row[8]),
            self._height_to_hash(row[1]), self._height_to_hash(row[2])
            )
        return row_list
