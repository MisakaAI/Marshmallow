# 数据库
from sqlmodel import SQLModel, create_engine

# DATABASE_URL = "postgresql+psycopg://<user>:<password>@<hostname>/<database>"
DATABASE_URL = "postgresql+psycopg://postgres:password@127.0.0.1/marshmallow"

# 创建数据库引擎，连接到指定的数据库地址
# echo=True 时，会在控制台输出执行的所有 SQL 语句，方便调试和查看数据库操作
engine = create_engine(DATABASE_URL, echo=False)


def init_db():
    """
    初始化数据库表结构：
    根据 SQLModel 中定义的所有模型元数据，自动创建数据库中不存在的表
    该操作在程序启动时执行一次，确保数据库表准备好
    """
    SQLModel.metadata.create_all(engine)

## 生产环境强烈推荐用 Alembic 进行迁移管理

# 安装
# pip install alembic

# 初始化
# alembic init alembic

# 修改 alembic.ini 中的数据库连接字符串为你的 DATABASE_URL
# 修改 alembic/env.py，导入模型元数据，示例

# from sqlmodel import SQLModel
# from app.models import *  # 导入所有模型
# target_metadata = SQLModel.metadata

# 生成迁移脚本
# alembic revision --autogenerate -m "描述这次修改"

# 执行迁移
# alembic upgrade head
