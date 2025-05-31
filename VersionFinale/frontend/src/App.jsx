import { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import './App.css';

function App() {
  const [recherche, setRecherche] = useState('');
  const [keywords, setKeywords] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [step, setStep] = useState(1); // 1 = génération mots-clés, 2 = recherche RAG
  const [ragResult, setRagResult] = useState('');

  // Étape 1 : Générer les mots-clés
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

  // Étape 2 : Lancer la recherche RAG en streaming markdown
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

      // Streaming de la réponse markdown
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        const chunk = decoder.decode(value, { stream: true });
        setRagResult((prev) => prev + chunk); // Affiche au fur et à mesure
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Réinitialiser pour une nouvelle recherche
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

      {/* Affichage des mots-clés générés */}
      {keywords && (
        <div className="result" style={{ marginBottom: '1em' }}>
          <h2>Mots-clés générés :</h2>
          <ul>
            {keywords.map((q, i) => (
              <li key={i}>{q}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Barre de recherche et boutons */}
      <form onSubmit={step === 1 ? handleGenerateKeywords : handleSimpleSearch}>
        <input
          type="text"
          value={recherche}
          onChange={(e) => setRecherche(e.target.value)}
          placeholder="Tape ta recherche ici..."
          className="search-bar"
          disabled={step === 2}
        />
        <button type="submit" disabled={loading || (step === 1 && !recherche)}>
          {loading
            ? 'Chargement...'
            : step === 1
            ? 'Générer les mots-clés'
            : 'Lancer la recherche'}
        </button>
        {step === 2 && (
          <button
            type="button"
            onClick={handleNewSearch}
            style={{ marginLeft: '1em' }}
          >
            Nouvelle recherche
          </button>
        )}
      </form>

      {error && <p style={{ color: 'red' }}>{error}</p>}

      {/* Résultat RAG en markdown (streaming) */}
      {ragResult && (
        <div style={{ marginTop: '2em', background: '#f6f6f6', padding: '1em', borderRadius: '8px' }}>
          <h3>Réponse :</h3>
          <ReactMarkdown>{ragResult}</ReactMarkdown>
        </div>
      )}
    </div>
  );
}

export default App;
