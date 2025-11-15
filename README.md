# 彩票网站项目

## 项目概述

本项目是一个基于Django和Docker构建的在线彩票网站，提供用户注册、彩票购买、开奖管理等功能。

## 功能特性

### 用户功能
- 用户注册和登录
- 账户充值
- 彩票购买（手动选号和机选）
- 查看购买历史
- 中奖查询和兑奖
- 个人资料管理

### 管理员功能
- 彩票类型管理
- 开奖期次管理
- 执行开奖操作
- 销售统计报告
- 用户管理
- 中奖确认

### 系统特性
- 响应式Web界面
- 安全的用户认证
- 自动中奖检测
- 交易记录追踪
- Docker容器化部署

## 技术栈

- **后端框架**: Django 3.2.25
- **数据库**: PostgreSQL (生产环境) / SQLite (开发环境)
- **前端**: Bootstrap 5 + HTML/CSS/JavaScript
- **容器化**: Docker + Docker Compose
- **Python版本**: 3.7+

## 项目结构

```
lottery_project/
├── accounts/              # 用户账户应用
├── lottery/               # 彩票核心功能
├── management/            # 管理员功能
├── templates/             # HTML模板
├── static/                # 静态文件
├── lottery_project/       # 项目配置
├── requirements.txt       # Python依赖
├── Dockerfile            # Docker镜像配置
├── docker-compose.yml    # Docker编排配置
└── manage.py             # Django管理脚本
```

## 安装和运行

### 方法1: Docker部署（推荐）

1. 确保已安装Docker和Docker Compose

2. 克隆项目
```bash
git clone <repository-url>
cd lottery_project
```

3. 启动服务
```bash
docker-compose up -d
```

4. 访问网站
```
http://localhost:8000
```

### 方法2: 本地开发

1. 安装Python依赖
```bash
pip install -r requirements.txt
```

2. 运行数据库迁移
```bash
python manage.py migrate
```

3. 初始化测试数据
```bash
python manage.py init_data
```

4. 启动开发服务器
```bash
python manage.py runserver
```

## 默认账户

系统初始化后会创建以下测试账户：

- **管理员账户**: 
  - 用户名: admin
  - 密码: admin123
  - 权限: 管理员权限，可访问管理后台

- **测试用户**: 
  - 用户名: testuser
  - 密码: test123
  - 余额: 500元

## 数据模型

### 核心模型

1. **LotteryType** - 彩票类型
   - 彩票名称、描述、价格
   - 选号规则（号码范围、选择数量）

2. **LotteryDraw** - 开奖期次
   - 期次号、开奖时间
   - 中奖号码、开奖状态

3. **LotteryTicket** - 彩票
   - 用户、期次、选择号码
   - 中奖状态、奖金金额

4. **UserProfile** - 用户资料
   - 账户余额、消费统计
   - 联系信息

5. **Transaction** - 交易记录
   - 交易类型、金额、描述
   - 时间戳

## API接口

### 用户相关
- `/accounts/register/` - 用户注册
- `/accounts/login/` - 用户登录
- `/accounts/profile/` - 个人中心
- `/accounts/recharge/` - 账户充值

### 彩票相关
- `/` - 首页
- `/lottery/` - 彩票大厅
- `/purchase/<id>/` - 购买彩票
- `/my-tickets/` - 我的彩票
- `/check-winnings/` - 检查中奖
- `/draw-results/` - 开奖结果

### 管理功能
- `/management/` - 管理后台
- `/management/draw-management/` - 开奖管理
- `/management/conduct-draw/<id>/` - 执行开奖
- `/management/sales-report/` - 销售报告

## 测试

运行测试用例：
```bash
python manage.py test
```

测试覆盖：
- 模型功能测试
- 视图功能测试
- 用户认证测试
- 彩票购买流程测试
- 中奖检测测试

## 部署说明

### 生产环境部署

1. 修改 `docker-compose.yml` 中的环境变量
2. 设置安全的数据库密码
3. 配置域名和SSL证书
4. 启用生产环境设置

### 环境变量

创建 `.env` 文件：
```
DEBUG=False
SECRET_KEY=your-production-secret-key
DATABASE_URL=postgresql://user:pass@db:5432/lottery_db
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

## 安全考虑

- 使用CSRF保护
- 密码哈希存储
- 用户权限控制
- SQL注入防护
- XSS攻击防护

## 许可证

本项目仅用于学习和演示目的。

## 贡献

欢迎提交Issue和Pull Request来改进项目。

## 联系方式

如有问题请联系项目维护者。
