import React from 'react';
import { motion } from 'framer-motion';

const ComparisonSection = () => {
    const tools = [
        {
            name: 'Gemini',
            type: 'Multimodal Giant',
            strengths: ['Huge Context Window', 'Video Understanding', 'Research capabilities'],
            icon: '🌟'
        },
        {
            name: 'Claude Code',
            type: 'Agentic Specialist',
            strengths: ['Terminal Integration', 'Plan & Execute Mode', 'Self-Correction', 'Permissionless Mode'],
            isHighlight: true,
            icon: '🔥'
        },
        {
            name: 'Codex CLI',
            type: 'Code Completion',
            strengths: ['Rapid Autocomplete', 'IDE Integration', 'GitHub Ecosystem'],
            icon: '💻'
        }
    ];

    return (
        <section className="py-20 relative overflow-hidden">
            <div className="container mx-auto px-4 relative z-10">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    className="text-center mb-16"
                >
                    <h2 className="text-4xl md:text-5xl font-display font-bold mb-4">
                        AI Coding Landscape
                    </h2>
                    <p className="text-xl text-secondary-light">
                        Where does Claude Code fit in?
                    </p>
                </motion.div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
                    {tools.map((tool, index) => (
                        <motion.div
                            key={tool.name}
                            initial={{ opacity: 0, y: 20 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            viewport={{ once: true }}
                            transition={{ delay: index * 0.1 }}
                            className={`relative p-8 rounded-2xl border ${tool.isHighlight
                                    ? 'bg-gradient-to-b from-primary/10 to-transparent border-primary/50 shadow-[0_0_40px_-10px_rgba(217,119,87,0.3)]'
                                    : 'glass border-white/10'
                                }`}
                        >
                            <div className="text-6xl mb-6">{tool.icon}</div>
                            <h3 className="text-2xl font-bold mb-2 font-display">{tool.name}</h3>
                            <div className="text-secondary mb-6 text-sm uppercase tracking-wider">{tool.type}</div>

                            <ul className="space-y-4">
                                {tool.strengths.map((strength, i) => (
                                    <li key={i} className="flex items-center text-sm md:text-base">
                                        <span className={`mr-2 ${tool.isHighlight ? 'text-primary' : 'text-accent'}`}>✓</span>
                                        <span className="text-gray-300">{strength}</span>
                                    </li>
                                ))}
                            </ul>

                            {tool.isHighlight && (
                                <div className="absolute top-0 right-0 bg-primary text-white text-xs font-bold px-3 py-1 rounded-bl-lg">
                                    RECOMMENDED
                                </div>
                            )}
                        </motion.div>
                    ))}
                </div>
            </div>
        </section>
    );
};

export default ComparisonSection;
