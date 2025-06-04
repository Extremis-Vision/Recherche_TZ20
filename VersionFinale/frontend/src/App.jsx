import { useState } from 'react';
import SearchBar from './SearchBar';
import KeywordList from './KeywordList';
import ResultDisplay from './ResultDisplay';
import GraphVisualization from './GraphVisualization';
import './App.css';

function App() {
  const [recherche, setRecherche] = useState('');
  const [keywords, setKeywords] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [step, setStep] = useState(1);
  const [ragResult, setRagResult] = useState('');
  const [graphFullScreen, setGraphFullScreen] = useState(false);

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
      if (!response.ok) throw new Error('Erreur lors de la g�n�ration des mots-cl�s');
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
    <div className="container" style={{ maxWidth: 1200 }}>
      <h1>Recherche de mots-cl�s IA</h1>
      <div style={{ display: 'flex', alignItems: 'flex-start', gap: 24 }}>
        {/* Colonne Recherche */}
        <div style={{ flex: 1, minWidth: 0 }}>
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
        {/* Colonne Graphe (miniature) */}
        <div style={{ width: 340, minWidth: 300, maxWidth: 400, position: 'relative' }}>
          <div style={{
            border: '1px solid #ccc',
            borderRadius: 8,
            background: '#fafafa',
            boxShadow: '0 2px 8px #0001',
            padding: 8,
            position: 'relative'
          }}>
            <div style={{ fontWeight: 'bold', marginBottom: 6 }}>Aper�u du Graphe</div>
            <div style={{ width: '100%', height: 220 }}>
              <GraphVisualization height={220} />
            </div>
            <button
              style={{
                position: 'absolute',
                top: 10,
                right: 10,
                background: '#267dc5',
                color: '#fff',
                border: 'none',
                borderRadius: 4,
                padding: '4px 10px',
                cursor: 'pointer'
              }}
              onClick={() => setGraphFullScreen(true)}
              title="Agrandir le graphe"
            >
              Agrandir
            </button>
          </div>
        </div>
      </div>

      {/* Modal plein �cran pour le graphe */}
      {graphFullScreen && (
  <div
    style={{
      position: 'fixed',
      zIndex: 1000,
      top: 0, left: 0, right: 0, bottom: 0,
      background: 'rgba(0,0,0,0.7)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center'
    }}
    onClick={() => setGraphFullScreen(false)}
  >
    <div
      style={{
        background: '#fff',
        borderRadius: 12,
        padding: 20,
        width: '90vw',
        height: '90vh',
        position: 'relative',
        boxShadow: '0 4px 24px #0004',
        display: 'flex',
        flexDirection: 'column'
      }}
      onClick={e => e.stopPropagation()}
    >
      <button
        onClick={() => setGraphFullScreen(false)}
        style={{
          position: 'absolute',
          top: 20,
          right: 20,
          background: '#b71c1c',
          color: '#fff',
          border: 'none',
          borderRadius: 4,
          padding: '6px 16px',
          fontWeight: 'bold',
          cursor: 'pointer',
          fontSize: '1.2em',
          zIndex: 10, // <-- Ajoute ceci
        }}
      >
        Fermer
      </button>

      <div style={{ flex: 1, width: '100%', height: '100%' }}>
        <GraphVisualization width="100%" height="100%" />
      </div>
    </div>
  </div>
)}

    </div>
  );
}

export default App;