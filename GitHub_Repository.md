# GitHub 仓库信息

## 项目源代码

本彩票网站项目的完整源代码已上传至GitHub仓库。

### 仓库地址
```
https://github.com/AlexKaili/lottery-website
```

### 仓库内容

仓库包含以下主要文件和目录：

```
lottery-website/
├── accounts/                 # 用户账户应用
├── lottery/                  # 彩票核心功能应用
├── management/               # 管理员功能应用
├── templates/                # HTML模板文件
├── lottery_project/          # Django项目配置
├── requirements.txt          # Python依赖包列表
├── Dockerfile               # Docker镜像配置
├── docker-compose.yml       # Docker编排配置
├── README.md                # 项目说明文档
├── 开发报告.md               # 详细开发报告
├── .gitignore              # Git忽略文件配置
└── manage.py               # Django管理脚本
```

### 克隆和运行

1. **克隆仓库**
   ```bash
   git clone https://github.com/AlexKaili/lottery-website.git
   cd lottery-website
   ```

2. **使用Docker运行**
   ```bash
   docker-compose up -d
   ```

3. **本地开发运行**
   ```bash
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py init_data
   python manage.py runserver
   ```

### 提交历史

仓库包含完整的开发历史记录，展示了项目从初始化到完成的整个开发过程：

- 项目初始化和基础配置
- 数据模型设计和实现
- 用户认证系统开发
- 彩票功能核心实现
- 管理员后台开发
- 前端界面设计
- Docker容器化配置
- 测试用例编写
- 文档完善

### 分支说明

- `main`: 主分支，包含稳定的生产版本
- `develop`: 开发分支，用于功能开发
- `feature/*`: 功能分支，用于特定功能开发

### 贡献指南

欢迎提交Issue和Pull Request来改进项目：

1. Fork本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

### 许可证

本项目采用MIT许可证，详见LICENSE文件。

### 联系方式

如有问题或建议，请通过以下方式联系：

- GitHub Issues: https://github.com/AlexKaili/lottery-website/issues
- Email: alex@example.com
