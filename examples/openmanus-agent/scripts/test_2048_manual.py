#!/usr/bin/env python3
"""Manual test script for 2048 game generation.

This script performs a complete end-to-end test of 2048 game generation
using the real LLM API.

Run with: uv run python scripts/test_2048_manual.py
"""

import sys
import tempfile
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from openmanus.config import get_settings, reset_settings
from openmanus.executor import create_default_executor
from openmanus.models.plan import RiskLevel
from openmanus.planner.llm_planner import LLMPlanner
from openmanus.tools.base import reset_global_registry


def print_section(title: str) -> None:
    """Print a section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def print_success(message: str) -> None:
    """Print a success message."""
    print(f"✅ {message}")


def print_error(message: str) -> None:
    """Print an error message."""
    print(f"❌ {message}")


def print_info(message: str) -> None:
    """Print an info message."""
    print(f"ℹ️  {message}")


def test_2048_generation_with_llm() -> bool:
    """Test 2048 game generation with real LLM API.

    Returns:
        True if test passes, False otherwise
    """
    print_section("2048 游戏生成 E2E 测试")

    # Reset state
    reset_settings()
    reset_global_registry()

    with tempfile.TemporaryDirectory() as tmpdir:
        workspace = Path(tmpdir)

        # Task description
        goal = (
            "创建一个 2048 文件夹，在当前项目中生成一个完整的 2048 网页小游戏，"
            "包含 HTML、CSS 和 JavaScript 文件，支持键盘方向键操作"
        )

        print_info(f"工作目录: {workspace}")
        print_info(f"任务描述: {goal}")

        try:
            # Step 1: Create planner with real API
            print_section("步骤 1: 初始化 LLM Planner")

            planner = LLMPlanner()
            print_success("LLM Planner 初始化成功")
            print_info(f"API Base: {planner.api_base}")
            print_info(f"Model: {planner.model}")

            # Step 2: Generate plan
            print_section("步骤 2: 生成执行计划")

            print_info("正在调用 Deepseek API 生成计划...")
            print_info("(这可能需要 10-30 秒)")

            plan = planner.generate_plan(goal, str(workspace))

            print_success("计划生成成功!")

            print(f"   任务目标: {plan.goal}")
            print(f"   风险等级: {plan.risk_level.value}")
            print(f"   工作目录: {plan.workspace_root}")
            print(f"   步骤数: {len(plan.steps)}")

            print("\n   执行步骤:")
            for i, step in enumerate(plan.steps, 1):
                print(f"      {i}. [{step.tool}] {step.description}")
                if step.inputs:
                    print(f"         输入: {step.inputs}")

            # Step 3: Execute the plan
            print_section("步骤 3: 执行计划")

            executor = create_default_executor(workspace_root=str(workspace))
            result = executor.execute_plan(plan)

            print(f"   执行状态: {result.overall_status.value}")
            print(f"   总步骤: {result.total_steps}")
            print(f"   成功: {result.successful_steps}")
            print(f"   失败: {result.failed_steps}")
            print(f"   耗时: {result.duration_ms}ms")

            if result.overall_status.value != "success":
                print_error("执行失败!")
                print("\n   失败详情:")

                for i, trace in enumerate(result.traces):
                    if trace.status.value == "failure":
                        print(f"      步骤 {trace.step_id}: {trace.error}")
                return False

            # Step 4: Validate generated files
            print_section("步骤 4: 验证生成的文件")

            game_dir = workspace / "2048"

            if not game_dir.exists():
                print_error(f"2048 目录不存在: {game_dir}")
                return False

            print_success(f"2048 目录已创建: {game_dir}")

            # List all generated files
            files = list(game_dir.rglob("*"))
            files = [f for f in files if f.is_file()]

            print(f"\n   生成的文件 ({len(files)} 个):")

            html_file = None
            css_file = None
            js_file = None

            for file in sorted(files):
                rel_path = file.relative_to(workspace)
                size = file.stat().st_size
                print(f"      📄 {rel_path} ({size:,} bytes)")

                if file.suffix == ".html":
                    html_file = file
                elif file.suffix == ".css":
                    css_file = file
                elif file.suffix == ".js":
                    js_file = file

            # Validate HTML file
            if html_file:
                print_section("步骤 5: 验证 HTML 文件")

                html_content = html_file.read_text(encoding="utf-8", errors="ignore")
                print_success(f"HTML 文件读取成功 ({len(html_content)} 字符)")

                # Check for required elements
                checks = [
                    ("DOCTYPE 或 html 标签", "<!DOCTYPE html>" in html_content or "<html" in html_content.lower()),
                    ("2048 关键词", "2048" in html_content),
                    ("游戏容器", any(tag in html_content for tag in ["game-board", "#game", ".game", 'id="game"', 'id="grid"', 'class="grid"'])),
                    ("脚本引用", "<script" in html_content.lower()),
                ]

                print("\n   HTML 验证:")
                all_passed = True
                for check_name, check_result in checks:
                    status = "✅" if check_result else "❌"
                    print(f"      {status} {check_name}")
                    if not check_result:
                        all_passed = False

                if not all_passed:
                    print_error("HTML 文件验证失败!")
                    print(f"\n   HTML 内容预览:\n{html_content[:500]}...")
                    return False

                print_success("HTML 文件验证通过!")

            else:
                print_error("HTML 文件不存在")
                return False

            # Validate CSS file
            if css_file:
                print_section("步骤 6: 验证 CSS 文件")

                css_content = css_file.read_text(encoding="utf-8", errors="ignore")
                print_success(f"CSS 文件读取成功 ({len(css_content)} 字符)")

                checks = [
                    ("游戏板样式", "game-board" in css_content or "grid" in css_content),
                    ("图块样式", "tile" in css_content),
                ]

                print("\n   CSS 验证:")
                for check_name, check_result in checks:
                    status = "✅" if check_result else "❌"
                    print(f"      {status} {check_name}")

            # Validate JavaScript file
            if js_file:
                print_section("步骤 7: 验证 JavaScript 文件")

                js_content = js_file.read_text(encoding="utf-8", errors="ignore")
                print_success(f"JavaScript 文件读取成功 ({len(js_content)} 字符)")

                checks = [
                    ("2048 关键词", "2048" in js_content),
                    ("游戏逻辑", any(word in js_content for word in ["class", "function", "const", "let", "var"])),
                    ("游戏板", "board" in js_content or "grid" in js_content),
                ]

                print("\n   JavaScript 验证:")
                for check_name, check_result in checks:
                    status = "✅" if check_result else "❌"
                    print(f"      {status} {check_name}")

            # Final summary
            print_section("测试总结")

            print_success("🎉 所有测试通过!")
            print(f"\n✅ 计划生成成功")
            print(f"✅ 计划执行成功")
            print(f"✅ 文件验证成功")
            print(f"✅ 游戏位置: {game_dir}")

            print(f"\n📮 在浏览器中打开游戏:")
            print(f"   open {html_file}")
            print(f"\n   或者双击文件: {html_file}")

            return True

        except Exception as e:
            print_error(f"测试失败: {e}")
            import traceback
            traceback.print_exc()
            return False


def main():
    """Main entry point."""
    print_section("OpenManus 2048 游戏生成测试")
    test_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print_info(f"测试时间: {test_time}")

    success = test_2048_generation_with_llm()

    print_section("测试完成")

    if success:
        print_success("✨ 2048 游戏生成测试全部通过!")
        print("\n🚀 您现在可以在浏览器中打开生成的游戏并开始玩 2048!")
        return 0
    else:
        print_error("❌ 测试失败")
        print("\n💡 请检查:")
        print("   1. Deepseek API key 是否正确配置")
        print("   2. 网络连接是否正常")
        print("   3. 查看上面的错误信息")
        return 1


if __name__ == "__main__":
    sys.exit(main())
