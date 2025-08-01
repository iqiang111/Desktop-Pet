# 桌面宠物 (Desktop Pet)

一个可爱的桌面宠物应用，基于PyQt5开发的桌面互动小工具，可以在你的桌面上显示一个会动的小宠物。

## 🌟 功能特性

- **三种状态模式**：正常、睡觉、捕捉模式
- **自动移动**：宠物会在屏幕边缘自动移动和反弹
- **状态切换**：通过右键菜单快速切换宠物状态
- **能量系统**：宠物拥有能量值，随时间变化
- **系统托盘**：最小化到系统托盘，不占用任务栏空间
- **鼠标交互**：支持鼠标拖拽移动宠物位置

## 🚀 安装

### 环境要求
- Python 3.6+
- PyQt5
- Windows/Linux/macOS

### 快速安装

1. **克隆或下载项目**
   ```bash
   git clone [项目地址]
   cd DesktopPet
   ```

2. **安装依赖**
   ```bash
   pip install PyQt5
   ```

3. **运行应用**
   ```bash
   python desktop_pet.py
   ```

### Conda环境安装

如果你使用conda环境：
```bash
conda create -n desktop_pet python=3.8
conda activate desktop_pet
conda install pyqt
python desktop_pet.py
```

## 📦 打包成exe

### 使用PyInstaller

1. **安装PyInstaller**
   ```bash
   pip install pyinstaller
   ```

2. **打包命令**
   ```bash
   pyinstaller --onefile --windowed --name=DesktopPet --icon=normal.png --add-data "catch.png;." --add-data "normal.png;." --add-data "sleep.png;." desktop_pet.py
   ```

3. **打包完成后**
   在 `dist` 文件夹中找到 `DesktopPet.exe`

### Conda环境打包
```bash
conda install pyinstaller
pyinstaller --onefile --windowed --name=DesktopPet --icon=normal.png --add-data "catch.png;." --add-data "normal.png;." --add-data "sleep.png;." desktop_pet.py
```

## 🎮 使用方法

### 基本操作
- **右键菜单**：在宠物上右键点击打开菜单
- **拖拽移动**：用鼠标左键拖拽宠物到任意位置
- **状态切换**：右键菜单中选择不同状态
- **最小化**：点击关闭按钮会最小化到系统托盘

### 状态说明
- **正常模式**：宠物正常显示，会随机移动
- **睡觉模式**：宠物显示睡觉状态，停止移动
- **捕捉模式**：宠物显示捕捉状态，适合互动

### 系统托盘
- 左键点击托盘图标显示/隐藏宠物
- 右键点击托盘图标打开菜单

## 🎨 自定义

### 更换图片
替换以下文件可以自定义宠物外观：
- `normal.png` - 正常状态图片
- `sleep.png` - 睡觉状态图片
- `catch.png` - 捕捉状态图片

### 调整参数
在 `desktop_pet.py` 中可以修改以下参数：
- 移动速度
- 能量变化速度
- 图片大小

## 📁 项目结构
DesktopPet/
├── desktop_pet.py # 主程序文件
├── normal.png # 正常状态图片
├── sleep.png # 睡觉状态图片
├── catch.png # 捕捉状态图片
└── README.md # 项目说明

## 🐛 常见问题

### Q: 运行时报错找不到模块
A: 确保已安装PyQt5：
```bash
pip install PyQt5
```

### Q: 打包后exe无法运行
A: 确保所有png图片与exe在同一目录下

### Q: 宠物不显示
A: 检查图片文件是否存在且格式正确

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个项目！

## 📄 许可证

MIT License - 详见LICENSE文件