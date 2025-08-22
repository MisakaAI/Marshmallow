import psycopg

# 数据库连接参数
conn_params = {
    "dbname": "marshmallow",
    "user": "postgres",
    "password": "",
    "host": "localhost",
    "port": 5432,
}

try:
    # 连接到PostgreSQL数据库
    with psycopg.connect(**conn_params) as conn:
        # 创建游标
        with conn.cursor() as cur:
            # 查询总记录数
            cur.execute("SELECT COUNT(id) FROM question;")
            total_count = cur.fetchone()[0]
            print(f"总记录数: {total_count}\n")

            # 创建命名游标（服务端游标）用于流式读取
            with conn.cursor(name="pagination_cursor") as server_cursor:
                # 执行分页查询
                server_cursor.execute(
                    """SELECT "id", "content" FROM "question" ORDER BY "timestamp";"""
                )

                while True:
                    # 获取单条记录
                    record = server_cursor.fetchone()
                    if record is None:
                        print("\n已到达记录末尾")
                        break

                    # 显示记录
                    print(f"\nUUID: {record[0]}")
                    print(f"内容: {record[1]}")

                    # 用户控制
                    user_input = input("\n" + "-" * 50).strip()
                    if user_input.lower() == "0":
                        print("\n程序已终止")
                        break

except psycopg.Error as e:
    print(f"数据库错误: {e}")
except Exception as e:
    print(f"程序错误: {e}")
