import { useEffect, useRef, useState } from 'react';

export const useCounter = (target, duration = 2000) => {
  const [count, setCount] = useState(0);
  const ref = useRef(null);
  const hasAnimated = useRef(false);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting && !hasAnimated.current) {
          hasAnimated.current = true;
          const step = target / (duration / 16);
          let current = 0;

          const updateCounter = () => {
            current += step;
            if (current < target) {
              setCount(Math.floor(current));
              requestAnimationFrame(updateCounter);
            } else {
              setCount(target);
            }
          };

          updateCounter();
          observer.unobserve(entry.target);
        }
      },
      { threshold: 0.5 }
    );

    if (ref.current) {
      observer.observe(ref.current);
    }

    return () => {
      if (ref.current) {
        observer.unobserve(ref.current);
      }
    };
  }, [target, duration]);

  return [ref, count];
};
