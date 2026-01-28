import React, { useState, useEffect } from 'react';
import { terminalSteps } from '../data';

const TerminalDemo = () => {
  const [lines, setLines] = useState([]);
  const [currentStepIndex, setCurrentStepIndex] = useState(0);
  const [charIndex, setCharIndex] = useState(0);
  const [isTyping, setIsTyping] = useState(true);

  useEffect(() => {
    if (currentStepIndex >= terminalSteps.length) {
      // Reset after a delay
      const timeout = setTimeout(() => {
        setLines([]);
        setCurrentStepIndex(0);
        setCharIndex(0);
        setIsTyping(true);
      }, 3000);
      return () => clearTimeout(timeout);
    }

    const currentStep = terminalSteps[currentStepIndex];

    if (isTyping && currentStep.type === 'command') {
      if (charIndex < currentStep.text.length) {
        const timeout = setTimeout(() => {
          setCharIndex((prev) => prev + 1);
        }, 50 + Math.random() * 50); // Random typing speed
        return () => clearTimeout(timeout);
      } else {
        // Finished typing command
        setIsTyping(false);
        const timeout = setTimeout(() => {
          setLines((prev) => [...prev, { ...currentStep }]);
          setCurrentStepIndex((prev) => prev + 1);
          setCharIndex(0);
        }, 500);
        return () => clearTimeout(timeout);
      }
    } else {
      // Output (instant or slight delay)
      const timeout = setTimeout(() => {
        setLines((prev) => [...prev, currentStep]);
        setCurrentStepIndex((prev) => prev + 1);
        setIsTyping(true); // Ready for next command if any
      }, 800);
      return () => clearTimeout(timeout);
    }
  }, [currentStepIndex, charIndex, isTyping]);

  const currentCommandText = 
    currentStepIndex < terminalSteps.length && 
    terminalSteps[currentStepIndex].type === 'command'
      ? terminalSteps[currentStepIndex].text.substring(0, charIndex)
      : '';

  return (
    <div className="terminal-window">
      <div className="terminal-header">
        <div className="dot red"></div>
        <div className="dot yellow"></div>
        <div className="dot green"></div>
      </div>
      <div className="terminal-body">
        {lines.map((line, index) => (
          <div key={index} className={line.type === 'command' ? 'command-line' : 'output-line'}>
            {line.type === 'command' && <span className="prompt">➜</span>}
            {line.text}
          </div>
        ))}
        {currentStepIndex < terminalSteps.length && terminalSteps[currentStepIndex].type === 'command' && (
           <div className="command-line">
             <span className="prompt">➜</span>
             {currentCommandText}<span className="cursor"></span>
           </div>
        )}
         {currentStepIndex === terminalSteps.length && (
           <div className="command-line">
             <span className="prompt">➜</span><span className="cursor"></span>
           </div>
        )}
      </div>
    </div>
  );
};

export default TerminalDemo;
