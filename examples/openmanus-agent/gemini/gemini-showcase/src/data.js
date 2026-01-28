export const features = [
  {
    title: "Context Aware",
    description: "Understand your entire codebase structure and conventions before acting.",
    icon: "🧠"
  },
  {
    title: "Multi-Agent System",
    description: "Delegate complex tasks to specialized agents like Codebase Investigator.",
    icon: "🤖"
  },
  {
    title: "Tool Integrated",
    description: "Seamlessly read files, run shell commands, and search content.",
    icon: "🛠️"
  },
  {
    title: "Safe & Secure",
    description: "Sandboxed environment options and critical command explanations.",
    icon: "🛡️"
  },
  {
    title: "Project Idiomatic",
    description: "Mimics your project's coding style, naming conventions, and structure.",
    icon: "🎨"
  },
  {
    title: "Memory",
    description: "Remembers your preferences and specific project details across sessions.",
    icon: "💾"
  }
];

export const terminalSteps = [
  { type: 'command', text: 'gemini fix-bug --file src/App.jsx' },
  { type: 'output', text: '🔍 Analyzing codebase context...' },
  { type: 'output', text: '💡 Found issue: Missing import in App.jsx' },
  { type: 'output', text: '✅ Applying fix...' },
  { type: 'output', text: '✨ Bug fixed! Verifying with tests...' },
  { type: 'output', text: '🟢 Tests passed.' }
];
