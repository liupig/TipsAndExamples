import time
import psycopg2
# from configuration import (PG_DATABASE, PG_HOST, PG_PASSWORD, PG_PORT, PG_USER)

INSERT_LIMIT_NUM = 60000


class Case(object):
    def source_data_table_case(self):
        """
        源数据表中必须包含ID字段，ID作为每条字段的唯一识别符。PG中需实现id的自增长
        CATEGORY字段不做强要求，如果需要再一个表中存多种类型的数据，需要该字段
        :return:
        """
        text = """
        # PG中需实现id的自增长
        CREATE SEQUENCE IF NOT EXISTS upms_area_id_seq START 101;
        1)
        CREATE TABLE SOURCE_DATA_TABLE(
           ID INT NOT NULL DEFAULT nextval('upms_area_id_seq'::regclass),
           CATEGORY  VARCHAR(50) NOT NULL,
           ...
        );
        2)
        CREATE TABLE SOURCE_DATA_TABLE(
            ID INT NOT NULL DEFAULT nextval('upms_area_id_seq'::regclass),
            CATEGORY  VARCHAR(50),
            PROVINCE VARCHAR(50) NOT NULL,
            CITY VARCHAR(50),
            DISTRICT VARCHAR(50)
        );
        """
        print(text)

    def status_table_case(self):
        """
        状态表表结构统一如下，只需更改表名即可。
        :return:
        """
        text = """
                CREATE TABLE STATUS_TABLE_CASE(
                   ID INT NOT NULL,
                   STATUS    INT   NOT NULL,
                   START_TIME INT   NOT NULL,
                   END_TIME  INT,
                   TASK_NAME    VARCHAR(50) NOT NULL,
                   unique(ID,TASK_NAME)
                );
                """
        print(text)

    def use_case(self):
        text = """
        PG = PGInitialize(PG_DATABASE, PG_USER, PG_PASSWORD, PG_HOST, PG_PORT)
        task_executor = TaskExecutor("test_task", "SOURCE_DATA_TABLE", "STATUS_TABLE_CASE", PG)
        task_executor.order_by_field_list = ["PROVINCE"]
        task_executor.update_basic_data()
        task_executor.run_job(udf, 100, 5)
        """
        print(text)


class PGInitialize(object):
    def __init__(self, pg_database, pg_user, pg_password, pg_host, pg_port):
        self.conn = psycopg2.connect(database=pg_database, user=pg_user, password=pg_password,
                                     host=pg_host, port=pg_port)
        self.cursor = self.conn.cursor()

    def select(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def update_returning(self, sql):
        self.cursor.execute(sql)
        self.conn.commit()
        return self.cursor.fetchall()

    def update(self, sql):
        self.cursor.execute(sql)
        self.conn.commit()

    def insert(self, sql):
        self.cursor.execute(sql)
        self.conn.commit()


class TaskExecutor(object):
    def __init__(self, task_name, source_data_table, status_table, pg):
        """

        :param task_name: task
        :param source_data_table:
        :param status_table:
        :param pg: postgresql db
        """
        self.task_name = task_name
        self.source_data_table = source_data_table
        self.status_table = status_table
        self.pg = pg
        self.category = None
        self.order_by_field_list = None

    def set_sort_fields(self, fields):
        self.order_by_field_list = fields

    def get_unprocessed_data(self, period, limit_num=1, output_fields=None):
        """

        :param limit_num:
        :param output_fields:
        :param period:  时间周期，单位：秒
        :return:
        """
        current_time = time.time()
        time_interval = current_time - period
        output_fields = ','.join([f"t1.{f}" for f in output_fields]) if output_fields else f"t1.*"
        order_by_text = "ORDER BY id" if self.order_by_field_list else ""

        sql = f"UPDATE {self.status_table} t1 SET status=1, start_time={current_time} " \
              f"from (SELECT * FROM {self.status_table} " \
              f"WHERE task_name='{self.task_name}' AND status=0 OR (status=1 and {time_interval} > start_time " \
              f"AND end_time=0) " \
              f"{order_by_text} LIMIT {limit_num}) t2 " \
              f"WHERE t1.id=t2.id and t1.task_name=t2.task_name " \
              f"RETURNING {output_fields}"

        return self.pg.update_returning(sql)

    def update_status(self, data_id):
        """

        :param data_id: data id in table
        :return:
        """
        sql = f"UPDATE {self.status_table} SET status=2, end_time={time.time()} " \
              f"WHERE id={data_id} AND task_name='{self.task_name}'"

        self.pg.update(sql)

    def update_basic_data(self):
        start_time = time.time()
        category = 'WHERE category=' + self.category if self.category else ''
        select_mun_sql = f"select count(1) from {self.source_data_table}"

        order_by_text = ("ORDER BY " + ', '.join(self.order_by_field_list)) if self.order_by_field_list else ""

        data_sum = self.pg.select(select_mun_sql)[0][0]
        for i in range(int(data_sum / INSERT_LIMIT_NUM) + 1):
            select_sql = f"select id from {self.source_data_table} {category} " \
                         f"{order_by_text} LIMIT {INSERT_LIMIT_NUM} OFFSET {i}"

            data_ids = self.pg.select(select_sql)
            if data_ids:
                values_list = [(index[0], 0, start_time, 0, self.task_name) for index in data_ids]
                values_text = str(values_list)[1:-1]

                insert_sql = f"INSERT INTO {self.status_table} (ID, STATUS, START_TIME, END_TIME, TASK_NAME) VALUES " \
                             f"{values_text} ON CONFLICT ON CONSTRAINT {self.status_table}_id_task_name_key DO NOTHING"

                self.pg.insert(insert_sql)

    def run_job(self, user_defined_functions, period, cycle_index):
        """

        :param user_defined_functions:
        :param period:
        :param cycle_index:
        :return:
        """
        for i in range(cycle_index):
            data = self.get_unprocessed_data(period)
            if data:
                data_id, status = user_defined_functions(data)
                if status:
                    self.update_status(data_id)
            else:
                break


def run_task(udf, pg_database, pg_user, pg_password, pg_host, pg_port, task_name, source_data_table,
             status_table, period, cycle_index, order_by_field_list=[]):
    """

    :param udf: User-defined functions
    :param pg_database:
    :param pg_user:
    :param pg_password:
    :param pg_host:
    :param pg_port:
    :param task_name:
    :param source_data_table:
    :param status_table:
    :param order_by_field_list: order by field list  like: ["PROVINCE"]
    :param period:  time period, Unit s
    :param cycle_index: cycle index
    :return:
    """
    PG = PGInitialize(pg_database, pg_user, pg_password, pg_host, pg_port)
    task_executor = TaskExecutor(task_name, source_data_table, status_table, PG)
    task_executor.order_by_field_list = order_by_field_list
    task_executor.update_basic_data()
    task_executor.run_job(udf, period, cycle_index)
