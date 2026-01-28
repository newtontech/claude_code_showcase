# Claude Code 前端设计文档

## 概述

本项目包含一个展示 Claude Code 强大能力的前端应用，采用**编辑杂志风格**设计，使用 **React + Vite + Tailwind CSS** 构建。

## 项目结构

```
new_web/
├── src/
│   ├── components/          # React 组件
│   │   ├── Navbar.jsx       # 导航栏
│   │   ├── Hero.jsx         # 首屏区域
│   │   ├── Marquee.jsx      # 跑马灯横幅
│   │   ├── CodeGeneration.jsx    # 代码生成展示
│   │   ├── DesignInnovation.jsx  # 设计创新展示
│   │   ├── FullStackDev.jsx      # 全栈开发展示
│   │   ├── Collaboration.jsx     # 多域协作展示
│   │   ├── Stats.jsx        # 统计数据
│   │   ├── CTA.jsx          # 行动号召
│   │   └── Footer.jsx       # 页脚
│   ├── hooks/               # 自定义 Hooks
│   │   ├── useScrollReveal.js   # 滚动显示动画
│   │   ├── useCounter.js        # 计数动画
│   │   └── index.js             # Hooks 导出
│   ├── App.jsx              # 主应用组件
│   ├── main.jsx             # 应用入口
│   └── index.css            # 全局样式
├── index.html               # HTML 模板
├── package.json             # 项目依赖
├── vite.config.js           # Vite 配置
├── tailwind.config.js       # Tailwind 配置
└── test.sh                  # 项目测试脚本
```

## 技术栈

- **React 18.3** - UI 框架
- **Vite 5.1** - 构建工具
- **Tailwind CSS 3.4** - 样式框架
- **Framer Motion 11.0** - 动画库
- **PostCSS + Autoprefixer** - CSS 处理

## 设计特点

### 1. 编辑杂志风格
- **大胆排版**：超大号标题（最大 8rem），紧凑字间距
- **不对称布局**：CSS Grid 系统，错位元素创造视觉张力
- **动态效果**：滚动触发动画、悬停效果、视差滚动

### 2. 独特配色方案
- 主色：深黑 (#080808)
- 强调色 1：橙红 (#ff4800)
- 强调色 2：青色 (#00f0ff)
- 避免常见的紫色渐变

### 3. 字体系统
- **Display 字体**：Orbitron（标题，几何感）
- **Body 字体**：Outfit（正文，现代无衬线）
- **Code 字体**：JetBrains Mono（代码，等宽）

## 内容板块

1. **Hero 区域** - 超大号不对称标题 + 实时代码预览
2. **代码生成能力** - 展示毫秒级响应和精准意图理解
3. **设计创新能力** - 视觉语言、微交互动画、响应式设计
4. **全栈开发** - 前后端技术栈全覆盖
5. **多领域协作** - 产品、设计、工程、数据分析全流程
6. **统计数据** - 效率提升数据展示
7. **CTA** - 行动号召

## 开发命令

```bash
# 安装依赖
npm install

# 启动开发服务器 (http://localhost:3000)
npm run dev

# 构建生产版本
npm run build

# 预览生产构建
npm run preview

# 运行项目测试
./test.sh
```

## 自定义 Hooks

### useScrollReveal
滚动触发显示动画的 Hook，使用 Intersection Observer API。

```jsx
const [ref, isVisible] = useScrollReveal();
```

### useCounter
数字计数动画 Hook，当元素进入视口时触发计数。

```jsx
const [ref, count] = useCounter(100, 2000); // 目标值，持续时间
```

## 动画效果

- **滚动显示**: 所有主要内容区域使用滚动触发动画
- **浮动效果**: Hero 区域代码块有 6 秒循环的浮动动画
- **计数动画**: 统计数字从 0 开始计数到目标值
- **悬停效果**: 卡片悬停时有 3D 变换和阴影效果
- **进度条**: 代码生成区域的进度条动画
- **跑马灯**: Marquee 区域的无限滚动横幅

## 浏览器兼容性

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## 测试结果

```
✓ 所有测试通过 (23/23)
✓ 项目构建成功
✓ 开发服务器正常运行
```

---

**设计理念**：通过大胆的视觉设计展示 Claude Code 在代码生成、设计创新、全栈开发和多领域协作方面的强大能力。
