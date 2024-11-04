# Binlog2SQL Web

## 项目简介

**Binlog2SQL Web** 是一个基于 Django 框架的 Web 应用，用于解析 MySQL binlog 日志并生成对应的 SQL 语句。该工具对数据库管理员和开发者在进行数据库binlog获取、恢复误操作和数据闪回、回滚方面提供了极大的便利。

## 功能特性

- **Binlog 解析**：通过提交 MySQL binlog 日志文件，生成 SQL 语句，方便用户查看和使用。
- **回滚 SQL**：支持生成数据变更的反向 SQL，用于数据回滚操作。
- **简洁的 Web 界面**：提供易用的表单界面，无需编写复杂的命令即可轻松解析 Binlog。
- **实时交互**：Web 端提供表单提交和结果展示，实时显示解析结果。

## 项目结构

```plaintext
.
├── README.md                   # 项目说明文件
├── config.toml                 # 项目配置文件
├── db.sqlite3                  # 默认数据库文件
├── manage.py                   # Django 项目管理文件
├── requirements.txt            # 项目依赖文件
├── binlog2sql_web              # 核心项目目录
│   ├── settings.py             # Django 项目设置
│   ├── urls.py                 # 路由配置
│   ├── views.py                # 视图函数
│   ├── templates               # HTML 模板
│   │   ├── index.html          # 项目主页
│   │   └── binlog_form.html    # Binlog 表单页
│   ├── source_code             # Binlog2SQL 源代码
│   │   ├── binlog2sql.py       # Binlog 解析主程序
│   │   └── binlog2sql_util.py  # 辅助工具
└── ...
```

## 安装与运行
1. 克隆项目
```
git clone https://github.com/你的用户名/Binlog2SQL-Web.git
cd binlog2sql-web
```
2. 创建虚拟环境并安装依赖
```
python3 -m venv venv
source venv/bin/activate  # 对于 Windows 使用 `venv\Scripts\activate`
pip install -r requirements.txt
```
3. 运行迁移和启动项目
```
python3 manage.py runserver
```
4. 访问项目
打开浏览器，访问 http://127.0.0.1:8000/ 以进入项目主页。

## 使用方法
项目主页：进入项目主页，点击“进入 Binlog2SQL 表单”按钮，进入表单页面。
填写表单：在 binlog_form 页面中，填写 MySQL 连接信息、Binlog 文件信息和其他选项。
提交解析：点击“Run Binlog2SQL”按钮以启动解析任务，解析结果将显示在页面上。
清除结果：可以使用“Clear Output”按钮清除解析结果。


## 示例
表单填写示例
在 binlog_form.html 页面中，可以填写以下内容进行解析：
```
主机名：127.0.0.1
端口：3306 
用户名：root #注意权限问题：这里如果是别的用户需要 GRANT super,replication slave,replicaiton client ON *.* to 你的用户@'这个项目运行的网络段/IP';
密码：yourpassword
数据库名：test_db
表名：test_table
Binlog 起始文件：mysql-bin.000001
起始时间：2024-01-01 10:00:00
结束时间：2024-01-01 12:00:00
```
### 返回结果示例
```
INSERT INTO `test_table` (`id`, `name`) VALUES (1, 'Alice');
UPDATE `test_table` SET `name` = 'Bob' WHERE `id` = 1;
DELETE FROM `test_table` WHERE `id` = 1;

```

## 注意事项
权限要求：
连接 MySQL 时，需要对指定数据库有 super,replication slave,replicaiton client  权限以获取 Binlog 日志。
时区设置：
系统将自动将 UTC 时间转换为东八区时间，以确保一致性。

## 贡献
欢迎提交 Issue 和 Pull Request，以帮助我们改进项目！

## 许可证
该项目采用 MIT 许可证，详细信息请参见 [LICENSE](https://opensource.org/license/mit) 文件。

