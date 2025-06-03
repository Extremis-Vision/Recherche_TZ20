import React from 'react';
import ReactMarkdown from 'react-markdown';

const ResultDisplay = ({ ragResult }) => (
  <div>
    {ragResult && (
      <div style={{ marginTop: '2em', background: '#f6f6f6', padding: '1em', borderRadius: '8px' }}>
        <h3>Réponse :</h3>
        <ReactMarkdown>{ragResult}</ReactMarkdown>
      </div>
    )}
  </div>
);

export default ResultDisplay;
