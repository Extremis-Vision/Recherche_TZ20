import { useState } from 'react';
import SearchBar from './SearchBar';
import KeywordList from './KeywordList';
import ResultDisplay from './ResultDisplay';
import './App.css';

function App() {
  const [recherche, setRecherche] = useState('');
  const [keywords, setKeywords] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [step, setStep] = useState(1);
  const [ragResult, setRagResult] = useState('');

  const handleGenerateKeywords = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setKeywords(null);
    setRagResult('');
    try {
      const response = await fetch('http://localhost:8888/recherche/keywords/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ recherche, numberKeyWord: 5 }),
      });
      if (!response.ok) throw new Error('Erreur lors de la génération des mots-clés');
      const data = await response.json();
      setKeywords(data.questions);
      setStep(2);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSimpleSearch = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setRagResult('');
    try {
      const response = await fetch('http://localhost:8888/recherche/SimpleSearch', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          recherche_prompt: recherche,
          MotCLee: keywords,
          number_result: 5,
        }),
      });
      if (!response.ok) throw new Error('Erreur lors de la recherche RAG');

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        const chunk = decoder.decode(value, { stream: true });
        setRagResult((prev) => prev + chunk);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleNewSearch = () => {
    setRecherche('');
    setKeywords(null);
    setRagResult('');
    setStep(1);
    setError(null);
  };

  return (
    <div className="container">
      <h1>Recherche de mots-clés IA</h1>
      <SearchBar
        recherche={recherche}
        setRecherche={setRecherche}
        loading={loading}
        step={step}
        onSubmit={step === 1 ? handleGenerateKeywords : handleSimpleSearch}
        onNewSearch={handleNewSearch}
      />
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <KeywordList keywords={keywords} setKeywords={setKeywords} />
      <ResultDisplay ragResult={ragResult} />
    </div>
  );
}

export default App;
