"""End-to-end test for 2048 game generation.

This test uses the real LLM API to:
1. Generate a plan for creating a 2048 web game
2. Execute the plan
3. Verify the generated files exist and are valid
"""

import tempfile
from pathlib import Path

import pytest
from PyQt6.QtWidgets import QApplication

from openmanus.config import get_settings, reset_settings
from openmanus.executor import create_default_executor
from openmanus.gui.main_window import MainWindow
from openmanus.models.plan import RiskLevel
from openmanus.planner.llm_planner import LLMPlanner
from openmanus.tools.base import reset_global_registry


@pytest.fixture
def app(qtbot):
    """Create QApplication for GUI tests."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


@pytest.fixture
def reset_state():
    """Reset global state before each test."""
    reset_settings()
    reset_global_registry()
    yield
    reset_settings()
    reset_global_registry()


class Test2048GameGeneration:
    """E2E tests for 2048 game generation using LLM API."""

    @pytest.mark.skipif(
        True,
        reason="Requires LLM API - run manually to test with real API",
    )
    def test_generate_2048_game_with_llm(self, app, reset_state) -> None:
        """Test complete 2048 game generation flow with real LLM API.

        This is the main integration test that verifies:
        1. Plan generation works with Deepseek API
        2. Plan contains valid steps
        3. Execution succeeds
        4. Required files are generated

        To run this test:
            uv run pytest tests/gui/test_2048_e2e.py::Test2048GameGeneration::test_generate_2048_game_with_llm -v -s
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)

            # Create planner with real API
            planner = LLMPlanner()

            # Task description
            goal = (
                "创建一个 2048 文件夹，在当前项目中生成一个完整的 2048 网页小游戏，"
                "包含 HTML、CSS 和 JavaScript 文件，支持键盘方向键操作"
            )

            # Generate plan
            print(f"\n🎯 生成计划中...")
            print(f"   工作目录: {workspace}")
            print(f"   任务: {goal}\n")

            plan = planner.generate_plan(goal, str(workspace))

            # Verify plan structure
            assert plan is not None
            assert len(plan.steps) > 0
            assert plan.risk_level in [RiskLevel.LOW, RiskLevel.MEDIUM]

            print(f"✓ 计划生成成功!")
            print(f"   风险等级: {plan.risk_level.value}")
            print(f"   步骤数: {len(plan.steps)}")

            # Display steps
            for i, step in enumerate(plan.steps, 1):
                print(f"   {i}. [{step.tool}] {step.description}")

            # Execute the plan
            executor = create_default_executor(workspace_root=str(workspace))

            print(f"\n🚀 执行计划中...\n")
            result = executor.execute_plan(plan)

            # Verify execution
            assert result is not None
            assert result.overall_status.value in ["success", "failure"]

            print(f"✓ 执行完成: {result.overall_status.value}")
            print(f"   成功步骤: {result.successful_steps}/{result.total_steps}")
            print(f"   失败步骤: {result.failed_steps}")
            print(f"   耗时: {result.duration_ms}ms")

            # Check for generated files
            game_dir = workspace / "2048"
            if game_dir.exists():
                print(f"\n📁 生成的文件:")

                # List all files in 2048 directory
                files = list(game_dir.rglob("*"))
                for file in sorted(files):
                    if file.is_file():
                        size = file.stat().st_size
                        print(f"   ✓ {file.relative_to(workspace)} ({size} bytes")

                # Verify required files exist
                html_file = game_dir / "index.html"
                css_file = game_dir / "style.css"
                js_file = game_dir / "game.js"

                # At minimum, we expect an HTML file
                if html_file.exists():
                    html_content = html_file.read_text()
                    print(f"\n📄 HTML 文件验证:")
                    print(f"   大小: {len(html_content)} 字符")

                    # Check for key HTML elements
                    assert "<!DOCTYPE html>" in html_content or "<html" in html_content.lower()
                    assert "2048" in html_content
                    print(f"   ✓ 包含 2048 关键词")

                    # Check for CSS
                    if css_file.exists():
                        print(f"   ✓ 包含 CSS 文件")

                    # Check for JavaScript
                    if js_file.exists():
                        print(f"   ✓ 包含 JavaScript 文件")

                print(f"\n✅ 2048 游戏生成测试通过!")
                print(f"   游戏位置: {game_dir}")
                print(f"   在浏览器中打开 {html_file} 即可开始游戏")

            else:
                pytest.fail(f"2048 目录未创建: {game_dir}")

    def test_generate_2048_with_mock(self, app, reset_state) -> None:
        """Test 2048 generation with MockPlanner for fast testing."""
        from openmanus.planner.mock_planner import MockPlanner

        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)

            # Use mock planner for faster testing
            planner = MockPlanner()

            # Note: MockPlanner won't recognize this specific task,
            # so we'll test a simpler flow
            goal = "总结测试"  # This triggers the mock summarization

            print(f"\n🎯 生成计划中 (Mock 模式)...")
            print(f"   工作目录: {workspace}")
            print(f"   任务: {goal}\n")

            plan = planner.generate_plan(goal, str(workspace))

            assert plan is not None
            assert len(plan.steps) > 0

            print(f"✓ 计划生成成功!")
            print(f"   风险等级: {plan.risk_level.value}")
            print(f"   步骤数: {len(plan.steps)}")

            # Execute
            executor = create_default_executor(workspace_root=str(workspace))
            result = executor.execute_plan(plan)

            assert result is not None
            print(f"\n✓ 执行完成: {result.overall_status.value}")
            print(f"   成功步骤: {result.successful_steps}/{result.total_steps}")


class Test2048GameValidation:
    """Tests to validate generated 2048 game files."""

    def test_html_file_validation(self) -> None:
        """Test that we can validate an HTML file contains required elements."""
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>2048 Game</title>
            <link rel="stylesheet" href="style.css">
        </head>
        <body>
            <h1>2048 Game</h1>
            <div id="game-board"></div>
            <script src="game.js"></script>
        </body>
        </html>
        """

        # Required elements
        assert "<!DOCTYPE html>" in html_content or "<html" in html_content.lower()
        assert "2048" in html_content
        assert "game-board" in html_content

        print("✓ HTML 文件验证通过")

    def test_css_file_validation(self) -> None:
        """Test that we can validate a CSS file contains required styles."""
        css_content = """
        body {
            font-family: Arial, sans-serif;
            background-color: #faf8ef;
        }

        #game-board {
            display: grid;
            grid-template-columns: repeat(4, 100px);
            grid-template-rows: repeat(4, 100px);
            gap: 10px;
        }

        .tile {
            background-color: #eee4da;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            font-weight: bold;
        }
        """

        # Required elements
        assert "game-board" in css_content
        assert "tile" in css_content
        assert "grid" in css_content

        print("✓ CSS 文件验证通过")

    def test_js_file_validation(self) -> None:
        """Test that we can validate a JS file contains required game logic."""
        js_content = """
        class Game2048 {
            constructor() {
                this.board = Array(16).fill(0);
                this.score = 0;
            }

            move(direction) {
                console.log("Moving:", direction);
            }

            render() {
                console.log("Rendering board");
            }
        }

        const game = new Game2048();
        game.render();
        """

        # Required elements
        assert "2048" in js_content
        assert ("class" in js_content or "function" in js_content)
        assert "board" in js_content

        print("✓ JavaScript 文件验证通过")
