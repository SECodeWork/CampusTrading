# 数据库初始化指南

本文档提供了CampusTrading项目数据库的初始化步骤和注意事项。

## 前提条件

在开始之前，请确保您已完成以下准备工作：

1. **安装MySQL服务器**：确保您的系统上已安装MySQL服务器，并且服务正在运行。
   - Windows用户可以从[MySQL官网](https://dev.mysql.com/downloads/mysql/)下载并安装。
   - 安装时，请记住设置的root用户密码。

2. **安装依赖**：确保项目所需的Python依赖已安装。
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

## 数据库配置说明

项目的数据库配置位于`config/development.py`文件中。默认配置如下：

```python
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost:3306/campus_trading_dev'
```

这表示：
- **用户名**：root
- **密码**：root
- **主机**：localhost
- **端口**：3306
- **数据库名**：campus_trading_dev

如果您的MySQL配置不同，请修改上述配置。

## 数据库初始化步骤

我们提供了一个自动化的初始化脚本`init_db.py`，它会完成以下任务：

1. 检查并创建数据库（如果不存在）
2. 初始化数据库迁移仓库
3. 创建数据库表结构
4. 初始化基础数据（学校、校区、专业、商品分类等）

### 执行初始化脚本

在`backend`目录下运行以下命令：

```bash
python init_db.py
```

脚本执行过程中会显示各个步骤的状态。如果一切顺利，您将看到类似以下输出：

```
===== 数据库初始化脚本 =====
正在检查数据库是否存在...
数据库 campus_trading_dev 已存在。

正在初始化数据库迁移...
正在应用数据库迁移...
数据库迁移成功！

正在初始化基础数据...
基础数据初始化成功！

===== 数据库初始化完成 =====
数据库连接信息: mysql+pymysql://root:root@localhost:3306/campus_trading_dev
您可以通过运行 'python run.py' 启动后端服务。
```

## 手动初始化步骤（可选）

如果您想手动执行数据库初始化，可以按照以下步骤进行：

### 1. 创建数据库

使用MySQL命令行工具或phpMyAdmin等工具创建数据库：

```sql
CREATE DATABASE campus_trading_dev CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 2. 初始化迁移仓库

如果还没有初始化迁移仓库，执行以下命令：

```bash
flask db init
```

### 3. 创建初始迁移

```bash
flask db migrate -m "Initial migration"
```

### 4. 应用迁移

```bash
flask db upgrade
```

### 5. 初始化基础数据

您可以手动运行我们提供的初始化脚本中的`init_base_data()`函数，或者在Python控制台中执行类似的代码。

## 常见问题

### 1. MySQL连接错误

如果遇到连接错误，请检查：
- MySQL服务是否正在运行
- 用户名和密码是否正确
- 数据库名是否已创建
- MySQL是否允许root用户从localhost连接

### 2. 迁移错误

如果遇到迁移错误，可能的原因：
- 模型定义有问题
- 迁移仓库已损坏

尝试删除`migrations`目录，然后重新初始化：

```bash
rm -rf migrations
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 3. 数据库表已存在

如果您看到错误消息表明表已存在，可以先删除数据库并重新创建：

```sql
DROP DATABASE campus_trading_dev;
CREATE DATABASE campus_trading_dev CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

然后重新运行初始化脚本。

## 启动后端服务

数据库初始化完成后，可以启动后端服务：

```bash
python run.py
```

## 后续数据库维护

### 添加新模型后更新数据库

当您添加新的模型或修改现有模型后，可以通过以下命令更新数据库：

```bash
flask db migrate -m "描述您的更改"
flask db upgrade
```

### 回滚迁移

如果需要回滚到之前的数据库状态：

```bash
flask db downgrade
```

## 注意事项

1. **生产环境**：在生产环境中，请使用强密码并创建专用的数据库用户，而不是使用root用户。
2. **备份**：定期备份您的数据库，特别是在应用迁移之前。
3. **数据库性能**：随着数据量的增长，考虑添加适当的索引以提高查询性能。

如果您在数据库初始化过程中遇到任何问题，请参考上述常见问题部分，或联系开发团队寻求帮助。