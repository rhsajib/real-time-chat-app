import React from 'react';
import { motion } from 'framer-motion';

const LandingPage = () => {
  const containerVariants = {
    initial: { opacity: 0, y: -20 },
    animate: { opacity: 1, y: 0 },
  };

  const textVariants = {
    initial: { opacity: 0, y: 20 },
    animate: { opacity: 1, y: 0, transition: { delay: 0.5, duration: 1 } },
  };

  return (
    <motion.div
      className="min-h-screen flex items-center justify-center"
      initial="initial"
      animate="animate"
      variants={containerVariants}
    >
      <motion.h1
        className="text-3xl text-cyan-800 font-semibold"
        variants={textVariants}
      >
        Welcome to ChatP
      </motion.h1>
    </motion.div>
  );
};

export default LandingPage;
