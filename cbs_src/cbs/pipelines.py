from itemadapter import ItemAdapter
import mysql.connector
import time


class MySQLPipeline:
    def __init__(self, mysql_host, mysql_user, mysql_password, mysql_db):
        self.mysql_host = mysql_host
        self.mysql_user = mysql_user
        self.mysql_password = mysql_password
        self.mysql_db = mysql_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mysql_host=crawler.settings.get("MYSQL_HOST"),
            mysql_user=crawler.settings.get("MYSQL_USER"),
            mysql_password=crawler.settings.get("MYSQL_PASSWORD"),
            mysql_db=crawler.settings.get("MYSQL_DB"),
        )

    def open_spider(self, spider):

        retry_count = 0

        while retry_count != 5:
            try:

                self.conn = mysql.connector.connect(
                    host=self.mysql_host,
                    user=self.mysql_user,
                    password=self.mysql_password,
                    database=self.mysql_db,
                )
                self.cursor = self.conn.cursor()

                # Check if the table exists and create it if necessary
                self.create_table_if_not_exists()
                retry_count = 5
            except Exception as e:
                print(e)
                print("RETRYING CONNECTION TO MYSQL")
                print(f"ATTEMPTS LEFT = {retry_count}/5")
                retry_count += 1
                time.sleep(5)

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        # Check if the URL already exists in the database
        sql_select = "SELECT id FROM cbs_items WHERE url = %s"
        self.cursor.execute(sql_select, (item["url"],))
        result = self.cursor.fetchone()

        if result:
            print("Item already exists, skipping insertion.")
            return item
        # Insert the data into the table
        sql = "INSERT INTO cbs_items (title, publish_date, url, description, content) VALUES (%s, %s, %s, %s, %s)"
        values = (
            item["title"],
            item["publish_date"],
            item["url"],
            item["description"],
            item["content"],
        )
        self.cursor.execute(sql, values)
        self.conn.commit()
        return item

    def create_table_if_not_exists(self):
        # Check if the table exists
        table_name = "cbs_items"
        self.cursor.execute("SHOW TABLES LIKE %s", (table_name,))
        table_exists = bool(self.cursor.fetchone())

        if not table_exists:
            # Define the SQL query to create the table
            create_table_sql = """
                CREATE TABLE cbs_items (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    title VARCHAR(255),
                    publish_date TEXT,
                    url VARCHAR(255),
                    description TEXT,
                    content TEXT
                )
            """
            # Execute the SQL query to create the table
            self.cursor.execute(create_table_sql)
            self.conn.commit()
