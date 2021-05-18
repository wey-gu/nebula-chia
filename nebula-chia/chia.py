import os
import sqlite3

from chia.consensus.block_record import BlockRecord
from chia.types.blockchain_format.coin import Coin


DEFAULT_DB_PATH = "~/.chia/mainnet/db/blockchain_v1_mainnet.sqlite"
DEFAULT_BLOCK_RECORD_LIMIT = 10000
BLOCKRECORD_FILENAME = "block_record.csv"
COINRECORD_FILENAME = "coin_record.csv"
DEFAULT_OUTPUT_PATH = os.getcwd()
CSV_WRITE_BATCH = 1000


class ChaiBatchConvertor:
    def __init__(self, db_path=None, output_path=None,
                 block_record_limit=None, write_batch_size=None):
        """
        Initilization for ChaiBatchConvertor.
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
        self.limit = block_record_limit

        if write_batch_size is None:
            write_batch_size = CSV_WRITE_BATCH
        self.write_batch_size = write_batch_size

    def block_record_convertor(self):
        """
        Parse block record and convert the record into CSV lines.
        """
        file_path = f"{ self.output_path }/{ BLOCKRECORD_FILENAME }"
        block_record_query = "SELECT * FROM block_records"

        if self.limit > 0:
            block_record_query = f"{ block_record_query } LIMIT { self.limit }"
        cur = self.db_con.cursor()
        rows_iterator = cur.execute(block_record_query)

        self.csv_writer(
            file_path, rows_iterator,
            self.block_record_row, self.write_batch_size)


    def coin_record_convertor(self):
        """
        Parse coin record and convert the record into CSV lines.
        """
        pass

    def csv_writer(self, file_path, iterator, row_formator, buffer_size):
        with open(file_path, mode='w') as file:
            writer = csv.writer(
                file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_buffer = list()
            for row in cur.execute(block_record_query):
                csv_buffer.append(row_formator(row))
                if len(csv_buffer) > buffer_size:
                    writer.writerows(csv_buffer)
                    del csv_buffer[:]
            if csv_buffer:
                writer.writerows(csv_buffer)
                del csv_buffer[:]

    def block_record_row(self, row):
        """
        Parse row and return a CSV block record row string.
        """
        return row_string