# Claude Code Showcase

A modern, high-performance showcase of using Claude Code to build and deploy advanced agentic applications.

## 🚀 Developing with Claude Code

Claude Code is an agentic coding tool that lives in your terminal. It helps you turn ideas into code faster than ever before.

### Getting Started

1. **Install Claude Code**: 
   ```bash
   npm install -g @anthropic-ai/claude-code
   ```
2. **Authenticate**:
   ```bash
   claude auth login
   ```
3. **Launch in this project**:
   ```bash
   claude
   ```

### Common Commands

- `claude "Add a new React component for the contact section"`
- `claude "Debug why the sidebar is not responsive on mobile"`
- `claude "Apply the latest design tokens from tailwind.config.js to all components"`

---

## 🎨 Task Showcase: Developing a Desktop Agent

This project serves as a practical demonstration of using Claude Code to develop a functional **Desktop General Agent**.

### The Objective
> **"用 CLAUDE CODE 开发一个能跑的桌面通用 Agent"**
> (Develop a functional Desktop General Agent using Claude Code)

### 🔄 Development Flow: Claude Code Self-Bootstrapping
The process follows a modular, agentic workflow illustrated below:

1. **Claude Code**: The primary agentic tool used for initial scaffolding and logic development.
2. **参考 OpenManus 开发有桌面 Agent**: Leveraging the OpenManus architecture to implement desktop-level capabilities (screen control, tool usage, etc.).
3. **2048 小游戏**: The ultimate proof of concept—an agent developed and refined by Claude Code that can autonomously play or develop games like 2048.

---

## 📁 Integrated Examples

We have integrated real-world examples to showcase the architecture:

### OpenManus Agent
Located in `/examples/openmanus-agent`, this is a reference implementation of a desktop agent.

> [!IMPORTANT]
> This example was integrated from a standalone research project. Security-sensitive files (like `.env`) have been excluded for safety. To run the example, ensure you provide your own environment variables.

---

## 🌐 Deployment

This project is configured for automated deployment to **GitHub Pages** via GitHub Actions.

- **URL**: [https://newtontech.github.io/claude_code_showcase/](https://newtontech.github.io/claude_code_showcase/)
- **Configuration**: See `.github/workflows/deploy.yml` for the CI/CD pipeline.
