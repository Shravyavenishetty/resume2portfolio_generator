import { useState } from 'react';
import Editor from '@monaco-editor/react';

export default function PortfolioEditor({ parsedData, onGenerate }) {
  const [code, setCode] = useState(JSON.stringify(parsedData, null, 2));

  return (
    <div className="mt-6">
      <h2 className="text-xl font-semibold mb-4">Edit Resume Data</h2>
      <Editor
        height="400px"
        defaultLanguage="json"
        value={code}
        onChange={(value) => setCode(value)}
        options={{ minimap: { enabled: false }, scrollBeyondLastLine: false }}
      />
      <button
        onClick={onGenerate}
        className="mt-4 bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600 mr-2"
      >
        Download Portfolio
      </button>
    </div>
  );
}