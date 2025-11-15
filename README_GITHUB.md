# 🎲 Django彩票网站

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-3.2.25-green.svg)](https://www.djangoproject.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

一个基于Django和Docker构建的功能完整的在线彩票网站，支持用户注册、彩票购买、自动开奖、中奖检测等功能。

## ✨ 功能特性

### 🔐 用户功能
- ✅ 用户注册和登录系统
- ✅ 个人资料管理
- ✅ 账户充值功能
- ✅ 彩票购买（手动选号/机选）
- ✅ 购买历史查看
- ✅ 中奖查询和自动兑奖
- ✅ 交易记录追踪

### 👨‍💼 管理员功能
- ✅ 管理员仪表板
- ✅ 彩票销售统计报告
- ✅ 彩票类型管理
- ✅ 开奖期次管理
- ✅ 自动/手动开奖操作
- ✅ 用户管理和监控
- ✅ 中奖确认和管理

### 🎯 系统特性
- ✅ 响应式Web界面（Bootstrap 5）
- ✅ 安全的用户认证和权限控制
- ✅ 自动中奖检测算法
- ✅ 完整的交易记录系统
- ✅ Docker容器化部署
- ✅ 完整的单元测试覆盖

## 🚀 快速开始

### 方法1：Docker部署（推荐）

```bash
# 克隆项目
git clone https://github.com/AlexKaili/lottery-website.git
cd lottery-website

# 启动服务
docker-compose up -d

# 访问网站
open http://localhost:8000
```

### 方法2：本地开发

```bash
# 安装依赖
pip install -r requirements.txt

# 数据库迁移
python manage.py migrate

# 初始化测试数据
python manage.py init_data

# 启动开发服务器
python manage.py runserver
```

## 🎮 演示账户

| 用户类型 | 用户名 | 密码 | 权限说明 |
|---------|--------|------|----------|
| 管理员 | `admin` | `admin123` | 完整管理权限 |
| 测试用户 | `testuser` | `test123` | 普通用户，余额500元 |
| 中奖测试 | `alex` | `alex12345` | 包含中奖彩票的测试账户 |

## 🏗️ 技术架构

```
lottery_project/
├── 🔐 accounts/           # 用户认证模块
├── 🎲 lottery/            # 彩票核心功能
├── 👨‍💼 management/        # 管理员功能
├── 🎨 templates/          # HTML模板
├── 📦 requirements.txt    # Python依赖
├── 🐳 Dockerfile         # Docker配置
├── 🔧 docker-compose.yml # 容器编排
└── 📚 docs/              # 项目文档
```

### 核心技术栈
- **后端**: Django 3.2.25
- **数据库**: PostgreSQL / SQLite
- **前端**: Bootstrap 5 + HTML/CSS/JavaScript
- **容器化**: Docker + Docker Compose
- **测试**: Django TestCase

## 📊 数据模型

### 核心模型关系
```mermaid
erDiagram
    User ||--|| UserProfile : has
    User ||--o{ LotteryTicket : purchases
    LotteryType ||--o{ LotteryDraw : has
    LotteryDraw ||--o{ LotteryTicket : contains
    User ||--o{ Transaction : makes
```

## 🧪 测试

```bash
# 运行所有测试
python manage.py test

# 运行功能测试
python test_website.py

# 运行管理员功能测试
python test_admin_functions.py
```

**测试覆盖**: 17个测试用例，100%通过率

## 🎯 中奖测试

项目包含完整的中奖测试功能：

```bash
# 创建中奖测试数据
python create_winning_test.py

# 检查用户中奖情况
python check_alex_winnings.py
```

## 📱 功能截图

### 用户界面
- 🏠 **首页**: 彩票展示和最新开奖
- 🎫 **彩票大厅**: 所有可购买的彩票类型
- 🛒 **购买页面**: 手动选号和机选功能
- 📋 **我的彩票**: 购买历史和中奖状态
- 🎉 **中奖查询**: 自动检测和兑奖

### 管理后台
- 📊 **仪表板**: 销售统计和系统概览
- 📈 **销售报告**: 详细的销售数据分析
- 🎲 **开奖管理**: 期次创建和开奖操作
- 👥 **用户管理**: 用户信息和行为监控

## 🔧 配置说明

### 环境变量
创建 `.env` 文件：
```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:pass@localhost:5432/lottery_db
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Docker配置
```yaml
# docker-compose.yml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "8000:8000"
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: lottery_db
```

## 🛡️ 安全特性

- ✅ CSRF跨站请求伪造保护
- ✅ 用户权限分级控制
- ✅ 密码哈希安全存储
- ✅ SQL注入防护
- ✅ XSS攻击防护
- ✅ 安全的会话管理

## 📈 性能优化

- ⚡ 数据库查询优化
- 🗄️ 静态文件缓存
- 📄 分页处理大数据
- 🔄 异步任务处理

## 🚀 部署指南

### 生产环境部署

1. **环境准备**
   ```bash
   # 安装Docker和Docker Compose
   # 配置域名和SSL证书
   ```

2. **配置修改**
   ```bash
   # 修改生产环境配置
   cp env.example .env
   # 编辑.env文件设置生产参数
   ```

3. **启动服务**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

## 🤝 贡献指南

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📝 开发文档

- 📖 [详细开发报告](开发报告.md)
- 📋 [项目完成总结](项目完成总结.md)
- 🔗 [GitHub仓库信息](GitHub_Repository.md)

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 👨‍💻 作者

**AlexKaili** - [GitHub](https://github.com/AlexKaili)

## 🙏 致谢

- Django框架团队
- Bootstrap UI框架
- Docker容器化技术
- 所有开源贡献者

## 📞 联系方式

- 📧 Email: alex@example.com
- 🐛 Issues: [GitHub Issues](https://github.com/AlexKaili/lottery-website/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/AlexKaili/lottery-website/discussions)

---

⭐ 如果这个项目对您有帮助，请给个Star支持一下！

🎲 **Happy Coding & Good Luck!** 🍀
