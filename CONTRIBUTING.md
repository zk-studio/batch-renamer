# 贡献指南

感谢你对 **批量文件重命名工具** 的关注！欢迎提交 Issue 和 Pull Request。

## 🐛 报告 Bug

请使用 [Bug Report](https://github.com/zk-studio/batch-renamer/issues/new?template=bug_report.md) 模板提交。

## 💡 功能建议

请使用 [Feature Request](https://github.com/zk-studio/batch-renamer/issues/new?template=feature_request.md) 模板提交。

## 🔧 开发环境

```bash
# 克隆仓库
git clone https://github.com/zk-studio/batch-renamer.git
cd batch-renamer

# 创建虚拟环境（推荐）
python -m venv .venv
.venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 运行
python main.py
```

## 📐 代码规范

- 使用 **Python 3.12+**
- 遵循 PEP 8 代码风格
- 提交信息使用中文，格式：`类型: 描述`
  - `feat: 新增XX功能`
  - `fix: 修复XX问题`
  - `docs: 更新文档`
  - `style: 调整样式`
  - `refactor: 重构代码`

## 📦 构建与发布

```bash
# 打包 EXE
pyinstaller --noconfirm --onedir --windowed --name "BatchRenamer" --clean main.py

# 生成安装包
iscc setup.iss
```

发布新版本时，只需推送 tag：
```bash
git tag v1.1.0
git push origin v1.1.0
```
GitHub Actions 会自动构建并发布 Release。
