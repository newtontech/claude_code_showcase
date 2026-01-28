import React from 'react';
import { motion } from 'framer-motion';

const ShowcaseSection = () => {
    return (
        <section className="py-20 relative bg-black/50">
            <div className="container mx-auto px-4">
                <h2 className="text-4xl md:text-5xl font-display font-bold mb-16 text-center">
                    Power in Practice
                </h2>

                <div className="space-y-32">
                    {/* Project 1: Desktop Agent */}
                    <div className="flex flex-col lg:flex-row items-center gap-12">
                        <motion.div
                            initial={{ opacity: 0, x: -50 }}
                            whileInView={{ opacity: 1, x: 0 }}
                            className="lg:w-1/2"
                        >
                            <div className="bg-gradient-to-r from-primary/20 to-purple-500/20 p-1 rounded-2xl">
                                <div className="bg-bg-lighter rounded-xl overflow-hidden aspect-video relative group">
                                    <div className="absolute inset-0 flex items-center justify-center">
                                        <span className="text-6xl group-hover:scale-110 transition-transform">🤖</span>
                                    </div>
                                    <div className="absolute bottom-0 left-0 right-0 p-6 bg-gradient-to-t from-black/80 to-transparent">
                                        <h3 className="text-2xl font-bold">Self-Bootstrapping Agent</h3>
                                    </div>
                                </div>
                            </div>
                        </motion.div>
                        <motion.div
                            initial={{ opacity: 0, x: 50 }}
                            whileInView={{ opacity: 1, x: 0 }}
                            className="lg:w-1/2 space-y-6"
                        >
                            <h3 className="text-3xl font-display font-bold text-primary">Desktop General Agent</h3>
                            <p className="text-lg text-secondary">
                                "Use Claude Code to develop a functional Desktop General Agent."
                            </p>
                            <div className="space-y-4">
                                <div className="flex items-center space-x-4">
                                    <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center font-bold">1</div>
                                    <p>Claude Code scaffolds the project</p>
                                </div>
                                <div className="flex items-center space-x-4">
                                    <div className="w-8 h-8 rounded-full bg-secondary flex items-center justify-center font-bold text-bg">2</div>
                                    <p>Integrates OpenManus architecture</p>
                                </div>
                                <div className="flex items-center space-x-4">
                                    <div className="w-8 h-8 rounded-full bg-accent flex items-center justify-center font-bold text-bg">3</div>
                                    <p>Result: An agent that plays 2048 autonomously</p>
                                </div>
                            </div>
                        </motion.div>
                    </div>

                    {/* Project 2: Scientific Research */}
                    <div className="flex flex-col lg:flex-row-reverse items-center gap-12">
                        <motion.div
                            initial={{ opacity: 0, x: 50 }}
                            whileInView={{ opacity: 1, x: 0 }}
                            className="lg:w-1/2"
                        >
                            <div className="bg-gradient-to-r from-secondary/20 to-blue-500/20 p-1 rounded-2xl">
                                <div className="bg-bg-lighter rounded-xl overflow-hidden aspect-video relative group">
                                    <div className="absolute inset-0 flex items-center justify-center">
                                        <span className="text-6xl group-hover:scale-110 transition-transform">🔬</span>
                                    </div>
                                    <div className="absolute bottom-0 left-0 right-0 p-6 bg-gradient-to-t from-black/80 to-transparent">
                                        <h3 className="text-2xl font-bold">Automated Research</h3>
                                    </div>
                                </div>
                            </div>
                        </motion.div>
                        <motion.div
                            initial={{ opacity: 0, x: -50 }}
                            whileInView={{ opacity: 1, x: 0 }}
                            className="lg:w-1/2 space-y-6"
                        >
                            <h3 className="text-3xl font-display font-bold text-secondary-light">Scientific Literature Survey</h3>
                            <p className="text-lg text-secondary">
                                "Automated generation of LaTeX surveys with citation verification."
                            </p>
                            <ul className="grid grid-cols-2 gap-4">
                                <li className="bg-surface p-3 rounded-lg text-sm border border-white/5">Scholar Gateway MCP</li>
                                <li className="bg-surface p-3 rounded-lg text-sm border border-white/5">LaTeX Bib Formatting</li>
                                <li className="bg-surface p-3 rounded-lg text-sm border border-white/5">Citation Verification</li>
                                <li className="bg-surface p-3 rounded-lg text-sm border border-white/5">Auto-compilation</li>
                            </ul>
                        </motion.div>
                    </div>
                </div>
            </div>
        </section>
    );
};

export default ShowcaseSection;
