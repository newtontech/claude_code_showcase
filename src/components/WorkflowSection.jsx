import React from 'react';
import { motion } from 'framer-motion';

const WorkflowSection = () => {
    return (
        <section className="py-20 bg-gradient-to-b from-bg to-bg-darker relative overflow-hidden">
            {/* Background elements */}
            <div className="absolute inset-0 grid-bg opacity-30"></div>

            <div className="container mx-auto px-4 relative z-10">
                <motion.div
                    initial={{ opacity: 0 }}
                    whileInView={{ opacity: 1 }}
                    className="text-center mb-20"
                >
                    <h2 className="text-4xl md:text-5xl font-display font-bold mb-4 gradient-text">
                        The Agentic Workflow
                    </h2>
                    <p className="text-xl text-secondary">
                        From "Ralph Wiggum" loops to TDD mastery
                    </p>
                </motion.div>

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
                    <motion.div
                        initial={{ opacity: 0, x: -50 }}
                        whileInView={{ opacity: 1, x: 0 }}
                        viewport={{ once: true }}
                    >
                        <h3 className="text-3xl font-bold mb-6 text-primary">The "Ralph Wiggum" Loop</h3>
                        <div className="bg-surface p-6 rounded-xl border border-white/5 space-y-4 font-code text-sm md:text-base">
                            <div className="flex items-start">
                                <span className="text-secondary mr-4">1.</span>
                                <div>
                                    <p className="text-accent">LLM:</p>
                                    <p>"I'm stopping now."</p>
                                </div>
                            </div>
                            <div className="flex items-start">
                                <span className="text-secondary mr-4">2.</span>
                                <div>
                                    <span className="text-secondary"># SYSTEM (Hooks):</span>
                                    <p className="text-red-400">"No you don't. Run the tests first."</p>
                                </div>
                            </div>
                            <div className="flex items-start">
                                <span className="text-secondary mr-4">3.</span>
                                <div>
                                    <p className="text-accent">LLM:</p>
                                    <p>"Tests failed. Fixing bugs..."</p>
                                </div>
                            </div>
                            <div className="flex items-start">
                                <span className="text-secondary mr-4">4.</span>
                                <div>
                                    <span className="text-green-400"># SYSTEM:</span>
                                    <p>"Tests passed. Now you can sleep."</p>
                                </div>
                            </div>
                        </div>
                    </motion.div>

                    <motion.div
                        initial={{ opacity: 0, x: 50 }}
                        whileInView={{ opacity: 1, x: 0 }}
                        viewport={{ once: true }}
                        className="space-y-8"
                    >
                        <div className="glass p-8 rounded-2xl relative overflow-hidden group">
                            <h4 className="text-2xl font-bold mb-4">Plan Mode</h4>
                            <p className="text-secondary mb-4">
                                Architect your solution before writing a single line of code.
                                Let Claude ask <i>you</i> questions to clarify requirements.
                            </p>
                            <div className="h-1 w-0 group-hover:w-full bg-primary transition-all duration-500"></div>
                        </div>

                        <div className="glass p-8 rounded-2xl relative overflow-hidden group">
                            <h4 className="text-2xl font-bold mb-4">Skip Permissions</h4>
                            <p className="text-secondary mb-4">
                                <code className="bg-white/10 px-2 py-1 rounded text-primary-light">--dangerously-skip-permissions</code>
                            </p>
                            <p className="text-gray-400 text-sm">
                                Unleash full autonomy. Let Claude run commands, edit files, and fix errors without interrupting you for approval.
                            </p>
                            <div className="h-1 w-0 group-hover:w-full bg-accent transition-all duration-500"></div>
                        </div>
                    </motion.div>
                </div>
            </div>
        </section>
    );
};

export default WorkflowSection;
