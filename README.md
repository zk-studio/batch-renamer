<div align="center">

# ⚡ 批量文件重命名工具

**BatchRenamer** — 安全、快速地批量修改文件名

[![Release](https://img.shields.io/github/v/release/zk-studio/batch-renamer?style=flat-square&color=blue)](https://github.com/zk-studio/batch-renamer/releases/latest)
[![Downloads](https://img.shields.io/github/downloads/zk-studio/batch-renamer/total?style=flat-square&color=green)](https://github.com/zk-studio/batch-renamer/releases)
[![License](https://img.shields.io/github/license/zk-studio/batch-renamer?style=flat-square)](LICENSE)
[![Stars](https://img.shields.io/github/stars/zk-studio/batch-renamer?style=flat-square)](https://github.com/zk-studio/batch-renamer/stargazers)
[![Issues](https://img.shields.io/github/issues/zk-studio/batch-renamer?style=flat-square)](https://github.com/zk-studio/batch-renamer/issues)

**简体中文** | [English](#english)

<br>

<img src="docs/screenshot.png" alt="Screenshot" width="800">

*现代深色主题 · GitHub Dark 风格*

</div>

---

## ✨ 功能特性

| 功能 | 说明 |
|------|------|
| 📁 **添加前缀 / 后缀** | 批量在文件名前后添加文本 |
| 🔍 **查找替换** | 批量替换文件名中的指定文本 |
| 🔢 **序号命名** | 按模板 + 自增编号批量命名 |
| 📝 **修改扩展名** | 批量更改文件扩展名 |
| 📂 **筛选器** | 按扩展名筛选，支持递归子文件夹 |
| ↩️ **一键撤销** | 支持撤销上一次重命名操作 |
| 👀 **实时预览** | 操作前预览所有变更，绿色高亮显示 |
| 🔄 **自动更新** | 启动时自动检查 GitHub 新版本 |

## 📥 下载安装

### 方式一：安装包（推荐）

前往 [**Releases 页面**](https://github.com/zk-studio/batch-renamer/releases/latest) 下载最新版本：

| 文件 | 说明 |
|------|------|
| `BatchRenamer_Setup_x.x.x.exe` | **安装包** — 含中文安装向导，自动创建快捷方式 |
| `BatchRenamer_Portable_x.x.x.zip` | **便携版** — 解压即用，无需安装 |

### 方式二：从源码运行

```bash
# 克隆仓库
git clone https://github.com/zk-studio/batch-renamer.git
cd batch-renamer

# 安装依赖
pip install -r requirements.txt

# 启动
python main.py
```

## 📁 项目结构

```
batch-renamer/
├── main.py                 # 入口文件
├── app/
│   ├── __init__.py         # 版本号、应用名
│   ├── main_window.py      # 主窗口（菜单栏、状态栏、信号编排）
│   ├── rename_engine.py    # 重命名引擎（纯逻辑，不依赖 Qt）
│   ├── styles.py           # QSS 样式表 + 调色板
│   ├── updater.py          # 自动更新（对接 GitHub Releases）
│   └── widgets.py          # 自定义控件
├── .github/
│   ├── workflows/
│   │   ├── ci.yml          # CI 构建检查
│   │   └── release.yml     # 自动发布 Release
│   └── ISSUE_TEMPLATE/     # Issue 模板
├── setup.iss               # Inno Setup 安装脚本
├── requirements.txt
├── CHANGELOG.md
├── CONTRIBUTING.md
└── LICENSE
```

## 🚀 发布新版本

只需三步：

```bash
# 1. 修改 app/__init__.py 中的版本号
# 2. 更新 CHANGELOG.md
# 3. 推送 tag
git tag v1.1.0
git push origin v1.1.0
```

GitHub Actions 会自动：
- ✅ 打包 EXE（PyInstaller）
- ✅ 生成安装包（Inno Setup，含中文界面）
- ✅ 创建便携版 ZIP
- ✅ 发布 GitHub Release（附带下载链接）

已安装的用户会在下次启动时收到更新通知 → 一键静默升级。

## 🛠️ 技术栈

- **Python** 3.12
- **PySide6** 6.11（Qt6 for Python）
- **PyInstaller** — 打包 EXE
- **Inno Setup** — Windows 安装包
- **GitHub Actions** — CI/CD 自动化

## 🤝 参与贡献

欢迎提交 [Issue](https://github.com/zk-studio/batch-renamer/issues) 和 [Pull Request](https://github.com/zk-studio/batch-renamer/pulls)！

详见 [贡献指南](CONTRIBUTING.md)。

## 📄 开源协议

[MIT License](LICENSE) © 2026

---

<div align="center">

如果这个项目对你有帮助，请给一个 ⭐ Star！

</div>
