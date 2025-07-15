import { motion } from 'framer-motion';

export default function TemplateShowcase({ onSelectTemplate, onSelectFrontendType, selectedTemplate, selectedFrontendType }) {
  const templates = [
    { id: 'classic', name: 'Classic', desc: 'Clean and professional design.' },
    { id: 'glassmorphism', name: 'Glassmorphism', desc: 'Modern, translucent aesthetic.' },
    { id: 'terminal', name: 'Terminal', desc: 'Retro, command-line style.' },
  ];

  const frontendTypes = [
    { id: 'html', name: 'HTML/CSS' },
    { id: 'react', name: 'React' },
  ];

  return (
    <div className="py-12 bg-white">
      <h2 className="text-3xl font-bold text-center mb-8">Choose Your Template & Framework</h2>
      <div className="max-w-5xl mx-auto">
        <div className="mb-8">
          <h3 className="text-xl font-semibold mb-4">Templates</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {templates.map((template) => (
              <motion.div
                key={template.id}
                whileHover={{ scale: 1.05 }}
                className={`p-6 rounded-lg shadow-md text-center cursor-pointer ${
                  selectedTemplate === template.id ? 'bg-blue-100 border-blue-500 border-2' : 'bg-gray-100'
                }`}
                onClick={() => onSelectTemplate(template.id)}
              >
                <h3 className="text-xl font-semibold mb-2">{template.name}</h3>
                <p>{template.desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
        <div>
          <h3 className="text-xl font-semibold mb-4">Frontend Type</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {frontendTypes.map((type) => (
              <motion.div
                key={type.id}
                whileHover={{ scale: 1.05 }}
                className={`p-6 rounded-lg shadow-md text-center cursor-pointer ${
                  selectedFrontendType === type.id ? 'bg-blue-100 border-blue-500 border-2' : 'bg-gray-100'
                }`}
                onClick={() => onSelectFrontendType(type.id)}
              >
                <h3 className="text-xl font-semibold mb-2">{type.name}</h3>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}