#!/bin/bash

# React 项目测试脚本
# 用于验证 Claude Code Showcase 项目是否正常运行

echo "=========================================="
echo "  Claude Code Showcase - 项目测试"
echo "=========================================="
echo ""

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 测试计数
passed=0
failed=0

# 测试函数
test_check() {
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓${NC} $1"
        ((passed++))
    else
        echo -e "${RED}✗${NC} $1"
        ((failed++))
    fi
}

echo "1. 检查项目结构..."
echo "-----------------------------------"

# 检查必需文件
[ -f "package.json" ]; test_check "package.json 存在"
[ -f "vite.config.js" ]; test_check "vite.config.js 存在"
[ -f "tailwind.config.js" ]; test_check "tailwind.config.js 存在"
[ -f "index.html" ]; test_check "index.html 存在"

echo ""
echo "2. 检查源文件..."
echo "-----------------------------------"

[ -f "src/main.jsx" ]; test_check "src/main.jsx 存在"
[ -f "src/App.jsx" ]; test_check "src/App.jsx 存在"
[ -f "src/index.css" ]; test_check "src/index.css 存在"

echo ""
echo "3. 检查组件..."
echo "-----------------------------------"

[ -f "src/components/Navbar.jsx" ]; test_check "Navbar.jsx 存在"
[ -f "src/components/Hero.jsx" ]; test_check "Hero.jsx 存在"
[ -f "src/components/Marquee.jsx" ]; test_check "Marquee.jsx 存在"
[ -f "src/components/CodeGeneration.jsx" ]; test_check "CodeGeneration.jsx 存在"
[ -f "src/components/DesignInnovation.jsx" ]; test_check "DesignInnovation.jsx 存在"
[ -f "src/components/FullStackDev.jsx" ]; test_check "FullStackDev.jsx 存在"
[ -f "src/components/Collaboration.jsx" ]; test_check "Collaboration.jsx 存在"
[ -f "src/components/Stats.jsx" ]; test_check "Stats.jsx 存在"
[ -f "src/components/CTA.jsx" ]; test_check "CTA.jsx 存在"
[ -f "src/components/Footer.jsx" ]; test_check "Footer.jsx 存在"

echo ""
echo "4. 检查自定义 Hooks..."
echo "-----------------------------------"

[ -f "src/hooks/useScrollReveal.js" ]; test_check "useScrollReveal.js 存在"
[ -f "src/hooks/useCounter.js" ]; test_check "useCounter.js 存在"
[ -f "src/hooks/index.js" ]; test_check "hooks/index.js 存在"

echo ""
echo "5. 检查依赖..."
echo "-----------------------------------"

[ -d "node_modules" ]; test_check "node_modules 已安装"
[ -f "package-lock.json" ]; test_check "package-lock.json 存在"

echo ""
echo "6. 语法检查..."
echo "-----------------------------------"

# 检查是否有语法错误（通过尝试解析）
node -e "require('./package.json')" 2>/dev/null; test_check "package.json 语法正确"

echo ""
echo "=========================================="
echo "  测试结果汇总"
echo "=========================================="
echo -e "${GREEN}通过: $passed${NC}"
echo -e "${RED}失败: $failed${NC}"
echo ""

if [ $failed -eq 0 ]; then
    echo -e "${GREEN}✓ 所有测试通过！${NC}"
    echo ""
    echo "项目已就绪，可以使用以下命令："
    echo "  npm run dev    - 启动开发服务器"
    echo "  npm run build  - 构建生产版本"
    echo "  npm run preview - 预览生产构建"
    exit 0
else
    echo -e "${RED}✗ 有 $failed 个测试失败${NC}"
    exit 1
fi
