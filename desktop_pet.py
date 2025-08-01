import sys
import random
import time
from PyQt5.QtWidgets import (QApplication, QWidget, QMenu, QAction, QSystemTrayIcon, QStyle)
from PyQt5.QtGui import QPixmap, QPainter, QCursor, QIcon, QFont, QColor
from PyQt5.QtCore import Qt, QTimer, QPoint, QPropertyAnimation, QRect

class DesktopPet(QWidget):
    def __init__(self):
        super().__init__()
        # 宠物状态枚举
        self.PET_STATES = {
            'NORMAL': 'normal',
            'CATCH': 'catch',
            'SLEEP': 'sleep'
        }
        
        # 窗口设置
        self.initUI()
        
        # 宠物状态 - 初始不移动
        self.current_state = self.PET_STATES['NORMAL']
        self.is_moving = False
        self.direction = [1, 1]
        self.speed = 2
        self.animation_frame = 0
        self.energy = 100
        self.happiness = 100
        
        # 加载宠物图像
        self.load_images()
        
        # 定时器
        self.move_timer = QTimer(self)
        self.move_timer.timeout.connect(self.move_randomly)
        
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.update_animation)
        self.animation_timer.start(300)
        
        # 状态定时器
        self.state_timer = QTimer(self)
        self.state_timer.timeout.connect(self.update_state)
        self.state_timer.start(5000)
        
        # 系统托盘
        self.create_tray_icon()
        
        # 初始化
        self.set_state('NORMAL')

    def initUI(self):
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.SubWindow |
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        screen_geometry = QApplication.desktop().availableGeometry()
        self.screen_width = screen_geometry.width()
        self.screen_height = screen_geometry.height()
        
        # 根据图片大小调整窗口
        self.setGeometry(100, 100, 80, 100)  # 增加高度给文字显示
        self.show()

    def load_images(self):
        """加载真实的宠物图片并修复路径问题"""
        self.images = {}
        image_files = {
            'NORMAL': 'normal.png',
            'CATCH': 'catch.png',
            'SLEEP': 'sleep.png'
        }
        
        import os
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        for state, filename in image_files.items():
            try:
                file_path = os.path.join(current_dir, filename)
                pixmap = QPixmap(file_path)
                if not pixmap.isNull():
                    # 调整图片大小，保持宽高比
                    pixmap = pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    self.images[state] = pixmap
                    print(f"成功加载: {filename}")
                else:
                    print(f"无法加载图片: {file_path}")
                    self.create_placeholder(state)
            except Exception as e:
                print(f"加载图片出错: {e}")
                self.create_placeholder(state)
        
        self.current_image = self.images.get('NORMAL')

    def create_placeholder(self, state):
        """创建占位图片"""
        pixmap = QPixmap(80, 80)
        pixmap.fill(Qt.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        colors = {
            'NORMAL': Qt.blue,
            'CATCH': Qt.red,
            'SLEEP': Qt.gray
        }
        
        painter.setBrush(colors.get(state, Qt.blue))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(10, 10, 60, 60)
        
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        painter.setFont(font)
        painter.setPen(Qt.white)
        painter.drawText(pixmap.rect(), Qt.AlignCenter, state[0])
        
        painter.end()
        self.images[state] = pixmap

    def set_state(self, state):
        """设置宠物状态并确保图片切换"""
        if state in self.images and self.images[state] is not None:
            old_state = self.current_state
            self.current_state = state
            self.current_image = self.images[state]
            print(f"状态切换: {old_state} -> {state}")
            self.update()
        else:
            print(f"状态 {state} 的图片未加载")

    def update_state(self):
        """根据时间和条件更新状态"""
        if self.current_state == 'CATCH':
            # 捕捉状态持续5秒后恢复正常
            self.set_state('NORMAL')
        elif self.current_state == 'SLEEP':
            # 睡眠时恢复能量
            self.energy = min(100, self.energy + 1)
        else:
            # 正常状态消耗能量
            self.energy = max(0, self.energy - 0.5)
            
            # 能量低时睡觉
            if self.energy < 20 and self.current_state != 'SLEEP':
                self.set_state('SLEEP')

    def start_moving(self):
        """开始移动"""
        if not self.move_timer.isActive():
            self.move_timer.start(50)
            self.is_moving = True
            print("宠物开始移动")
            self.update()

    def stop_moving(self):
        """停止移动"""
        if self.move_timer.isActive():
            self.move_timer.stop()
            self.is_moving = False
            print("宠物停止移动")
            self.update()

    def move_randomly(self):
        """智能随机移动"""
        if not self.is_moving or self.current_state == 'SLEEP':
            return
            
        # 根据状态调整移动行为
        if self.current_state == 'CATCH':
            current_speed = int(self.speed * 1.5)
        else:
            current_speed = int(self.speed)
            
        # 智能移动逻辑
        if random.random() < 0.02:
            self.direction = [random.choice([-1, 1]), random.choice([-1, 1])]
        
        # 计算新位置
        current_pos = self.pos()
        new_x = int(current_pos.x() + self.direction[0] * current_speed)
        new_y = int(current_pos.y() + self.direction[1] * current_speed)
        
        # 边界检测和反弹
        if new_x < 0 or new_x + self.width() > self.screen_width:
            self.direction[0] *= -1
            new_x = max(0, min(new_x, self.screen_width - self.width()))
            
        if new_y < 0 or new_y + self.height() > self.screen_height:
            self.direction[1] *= -1
            new_y = max(0, min(new_y, self.screen_height - self.height()))
        
        self.move(new_x, new_y)

    def update_animation(self):
        """更新动画效果"""
        if self.current_state == 'SLEEP':
            # 睡眠时轻微浮动
            offset = int(1 * (1 if self.animation_frame % 2 else -1))
            current_pos = self.pos()
            self.move(current_pos.x(), current_pos.y() + offset)
            
        self.animation_frame += 1
        self.update()

    def create_tray_icon(self):
        """创建系统托盘图标 - 使用当前状态的图片"""
        self.tray_icon = QSystemTrayIcon(self)
        
        # 使用当前状态的图片作为托盘图标
        if self.current_state in self.images and self.images[self.current_state] is not None:
            icon = QIcon(self.images[self.current_state])
        elif 'NORMAL' in self.images and self.images['NORMAL'] is not None:
            icon = QIcon(self.images['NORMAL'])
        else:
            icon = self.style().standardIcon(QStyle.SP_ComputerIcon)
            
        self.tray_icon.setIcon(icon)
        
        # 添加双击托盘图标切换显示/隐藏
        self.tray_icon.activated.connect(self.tray_icon_activated)
        
        tray_menu = QMenu()
        
        show_action = QAction("显示", self)
        hide_action = QAction("隐藏", self)
        quit_action = QAction("退出", self)
        
        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(QApplication.quit)
        
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addSeparator()
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def tray_icon_activated(self, reason):
        """托盘图标激活处理"""
        if reason == QSystemTrayIcon.DoubleClick:
            if self.isVisible():
                self.hide()
            else:
                self.show()
                self.raise_()
                self.activateWindow()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # 左键点击切换状态
            if self.current_state == 'SLEEP':
                self.set_state('NORMAL')
                self.energy = 50
            else:
                self.set_state('CATCH')
                self.happiness = min(100, self.happiness + 10)
                
            self.drag_start_position = event.globalPos() - self.frameGeometry().topLeft()
            
        elif event.button() == Qt.RightButton:
            self.show_menu()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.move(event.globalPos() - self.drag_start_position)

    def show_menu(self):
        menu = QMenu(self)
        
        # 能量显示（不可点击）
        energy_action = QAction(f"能量: {int(self.energy)}%", self)
        energy_action.setEnabled(False)
        
        # 鼠标跟踪相关
        self.last_mouse_pos = QCursor.pos()
        self.mouse_idle_timer = QTimer(self)
        self.mouse_idle_timer.timeout.connect(self.check_mouse_idle)
        self.mouse_idle_timer.start(1000)  # 每秒检查一次
        self.mouse_idle_time = 0
        self.is_dragging_mouse = False

        # 移动控制
        if self.is_moving:
            move_action = QAction("停止移动", self)
            move_action.triggered.connect(self.stop_moving)
        else:
            move_action = QAction("开始移动", self)
            move_action.triggered.connect(self.start_moving)
        
        # 状态切换
        normal_action = QAction("正常模式", self)
        sleep_action = QAction("睡觉模式", self)
        catch_action = QAction("捕捉模式", self)
        
        normal_action.triggered.connect(lambda: self.set_state('NORMAL'))
        sleep_action.triggered.connect(lambda: self.set_state('SLEEP'))
        catch_action.triggered.connect(lambda: self.set_state('CATCH'))
        
        exit_action = QAction("退出", self)
        exit_action.triggered.connect(QApplication.instance().quit)
        
        menu.addAction(energy_action)
        menu.addSeparator()
        menu.addAction(move_action)
        menu.addSeparator()
        menu.addAction(normal_action)
        menu.addAction(sleep_action)
        menu.addAction(catch_action)
        menu.addSeparator()
        menu.addAction(exit_action)
        
        menu.exec_(QCursor.pos())

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 绘制宠物图片
        if self.current_image:
            painter.drawPixmap(0, 0, self.current_image)
        

    def check_mouse_idle(self):
        """检查鼠标是否空闲超过3秒"""
        if self.is_dragging_mouse:
            return
            
        current_pos = QCursor.pos()
        if current_pos == self.last_mouse_pos:
            self.mouse_idle_time += 1
            if self.mouse_idle_time >= 3:  # 3秒
                self.drag_mouse_randomly()
                self.mouse_idle_time = 0
        else:
            self.mouse_idle_time = 0
            self.last_mouse_pos = current_pos

    def drag_mouse_randomly(self):
        """随机拖拽鼠标移动"""
        if self.current_state == 'SLEEP':
            return
            
        self.is_dragging_mouse = True
        
        # 随机方向和距离
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        direction = random.choice(directions)
        distance = random.randint(50, 150)
        
        # 计算新位置
        current_mouse = QCursor.pos()
        new_x = current_mouse.x() + direction[0] * distance
        new_y = current_mouse.y() + direction[1] * distance
        
        # 确保在屏幕范围内
        new_x = max(0, min(new_x, self.screen_width - 1))
        new_y = max(0, min(new_y, self.screen_height - 1))
        
        # 移动鼠标
        QCursor.setPos(new_x, new_y)
        
        # 更新宠物状态
        self.set_state('CATCH')
        
        # 重置标记
        QTimer.singleShot(1000, lambda: setattr(self, 'is_dragging_mouse', False))
        
        print(f"宠物拖拽鼠标移动了 {distance} 像素")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    
    pet = DesktopPet()
    sys.exit(app.exec_())