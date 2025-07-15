import { motion } from 'framer-motion';

export default function HowItWorks() {
  const steps = [
    { title: 'Upload Resume', desc: 'Upload your PDF resume.' },
    { title: 'Analyze & Parse', desc: 'Our AI extracts and enhances your data.' },
    { title: 'Choose Template', desc: 'Select a stunning portfolio design.' },
    { title: 'Select Framework', desc: 'Choose HTML or React for your site.' },
    { title: 'Download or Deploy', desc: 'Download as ZIP or deploy to Vercel.' },
  ];

  return (
    <div className="py-12 bg-gray-50">
      <h2 className="text-3xl font-bold text-center mb-8">How It Works</h2>
      <div className="max-w-5xl mx-auto grid grid-cols-1 md:grid-cols-5 gap-6">
        {steps.map((step, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.2 }}
            className="bg-white p-6 rounded-lg shadow-md text-center"
          >
            <h3 className="text-xl font-semibold mb-2">{step.title}</h3>
            <p>{step.desc}</p>
          </motion.div>
        ))}
      </div>
    </div>
  );
}