import { motion } from 'framer-motion';

export default function Hero() {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 1 }}
      className="bg-blue-600 text-white text-center py-16"
    >
      <h1 className="text-4xl md:text-6xl font-bold mb-4">
        Turn Your Resume Into a Stunning Portfolio
      </h1>
      <p className="text-lg md:text-xl max-w-2xl mx-auto">
        Upload your resume, choose a template and framework, and deploy a professional portfolio in minutes.
      </p>
    </motion.div>
  );
}