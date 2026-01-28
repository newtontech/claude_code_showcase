import React from 'react';
import { motion } from 'framer-motion';

const EcosystemSection = () => {
    const integrations = [
        { title: "MCP Integration", desc: "Model Context Protocol for standardized tool use", color: "from-blue-400 to-blue-600" },
        { title: "Plugin Store", desc: "Vast ecosystem of community capabilities", color: "from-purple-400 to-purple-600" },
        { title: "Context Loading", desc: "Smart context management for large codebases", color: "from-green-400 to-green-600" },
        { title: "Terminal Control", desc: "Direct shell access for command execution", color: "from-orange-400 to-orange-600" }
    ];

    return (
        <section className="py-20 relative px-4">
            <div className="container mx-auto">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    className="text-center mb-16"
                >
                    <h2 className="text-4xl font-display font-bold mb-6">A Complete Ecosystem</h2>
                    <p className="text-xl text-secondary max-w-2xl mx-auto">
                        Claude Code isn't just a chatbot. It's a platform integrated with your entire development environment.
                    </p>
                </motion.div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                    {integrations.map((item, idx) => (
                        <motion.div
                            key={idx}
                            initial={{ opacity: 0, scale: 0.9 }}
                            whileInView={{ opacity: 1, scale: 1 }}
                            transition={{ delay: idx * 0.1 }}
                            className="p-6 rounded-2xl glass hover:bg-white/5 transition-colors group cursor-pointer"
                        >
                            <div className={`w-12 h-12 rounded-lg bg-gradient-to-br ${item.color} mb-4 group-hover:scale-110 transition-transform`}></div>
                            <h3 className="text-xl font-bold mb-2">{item.title}</h3>
                            <p className="text-sm text-secondary">{item.desc}</p>
                        </motion.div>
                    ))}
                </div>
            </div>
        </section>
    );
};

export default EcosystemSection;
