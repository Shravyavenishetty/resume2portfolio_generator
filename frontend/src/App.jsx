import { useState } from 'react';
import { motion } from 'framer-motion';
import Hero from './components/Hero';
import HowItWorks from './components/HowItWorks';
import TemplateShowcase from './components/TemplateShowcase';
import PortfolioEditor from './components/PortfolioEditor';
import './index.css';

function App() {
  const [file, setFile] = useState(null);
  const [parsedData, setParsedData] = useState(null);
  const [selectedTemplate, setSelectedTemplate] = useState('classic');
  const [frontendType, setFrontendType] = useState('html');
  const [githubToken, setGithubToken] = useState('');
  const [vercelToken, setVercelToken] = useState('');
  const [error, setError] = useState(null);
  const [deployResult, setDeployResult] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a PDF file');
      return;
    }
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:8000/upload', {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      if (response.ok) {
        setParsedData(data.parsed_data);
        setError(null);
      } else {
        setError(data.detail || 'Error uploading file');
      }
    } catch (err) {
      setError('Failed to connect to backend');
    }
  };

  const handleGenerate = async () => {
    if (!parsedData) {
      setError('No resume data to generate portfolio');
      return;
    }
    try {
      const response = await fetch('http://localhost:8000/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ parsed_data: parsedData, template: selectedTemplate, frontend_type: frontendType }),
      });
      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `portfolio_${selectedTemplate}_${frontendType}_${Date.now()}.zip`;
        a.click();
        window.URL.revokeObjectURL(url);
        setError(null);
      } else {
        const data = await response.json();
        setError(data.detail || 'Error generating portfolio');
      }
    } catch (err) {
      setError('Failed to generate portfolio');
    }
  };

  const handleDeploy = async () => {
    if (!parsedData) {
      setError('No resume data to deploy');
      return;
    }
    if (!githubToken || !vercelToken) {
      setError('Please provide GitHub and Vercel tokens');
      return;
    }
    try {
      const response = await fetch('http://localhost:8000/deploy', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          parsed_data: parsedData,
          template: selectedTemplate,
          frontend_type: frontendType,
          github_token: githubToken,
          vercel_token: vercelToken,
        }),
      });
      if (response.ok) {
        const data = await response.json();
        setDeployResult(data);
        setError(null);
      } else {
        const data = await response.json();
        setError(data.detail || 'Error deploying portfolio');
      }
    } catch (err) {
      setError('Failed to deploy portfolio');
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <Hero />
      <HowItWorks />
      <TemplateShowcase 
        onSelectTemplate={setSelectedTemplate} 
        onSelectFrontendType={setFrontendType}
        selectedTemplate={selectedTemplate}
        selectedFrontendType={frontendType}
      />
      <motion.div
        initial={{ opacity: 0, y: 50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="max-w-4xl mx-auto p-4"
      >
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-2xl font-bold mb-4">Upload Your Resume</h2>
          <input
            type="file"
            accept=".pdf"
            onChange={handleFileChange}
            className="mb-4 w-full"
          />
          <button
            onClick={handleUpload}
            className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 mr-2"
          >
            Upload Resume
          </button>
          {error && <p className="text-red-500 mt-4">{error}</p>}
          {parsedData && (
            <>
              <PortfolioEditor parsedData={parsedData} onGenerate={handleGenerate} />
              <div className="mt-4">
                <h3 className="text-lg font-semibold mb-2">Deploy to Vercel</h3>
                <input
                  type="text"
                  placeholder="GitHub Personal Access Token"
                  value={githubToken}
                  onChange={(e) => setGithubToken(e.target.value)}
                  className="w-full p-2 mb-2 border rounded"
                />
                <input
                  type="text"
                  placeholder="Vercel API Token"
                  value={vercelToken}
                  onChange={(e) => setVercelToken(e.target.value)}
                  className="w-full p-2 mb-2 border rounded"
                />
                <button
                  onClick={handleDeploy}
                  className="bg-purple-500 text-white px-4 py-2 rounded hover:bg-purple-600"
                >
                  Deploy to Vercel
                </button>
                {deployResult && (
                  <div className="mt-4">
                    <p>GitHub Repository: <a href={deployResult.repo_url} target="_blank" className="text-blue-500">{deployResult.repo_url}</a></p>
                    <p>Vercel Domain: {deployResult.vercel_domain}</p>
                  </div>
                )}
              </div>
            </>
          )}
        </div>
      </motion.div>
    </div>
  );
}

export default App;