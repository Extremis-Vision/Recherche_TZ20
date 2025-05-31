import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';

function BarreDeRecherche() {
  const [recherche, setRecherche] = useState('');
  const [keywords, setKeywords] = useState(null);
  const [ragResult, setRagResult] = useState('');
  const [loading, setLoading] = useState(false);
  const [step, setStep] = useState(1); // 1 = génération mots-clés, 2 = recherche RAG
  const [error, setError] = useState(null);

  // 1ère étape : Générer les mots-clés
  const handleGenerateKeywords = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setKeywords(null);
    setRagResult('');
    try {
      const response = await fetch(
        'http://localhost:8888/recherche/keywords/',
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ recherche, numberKeyWord: 5 }),
        }
      );
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

  // 2ème étape : Lancer la recherche RAG avec streaming markdown
  const handleSimpleSearch = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setRagResult('');
    try {
      const response = await fetch(
        'http://localhost:8888/recherche/SimpleSearch',
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            recherche_prompt: recherche,
            MotCLee: keywords,
            number_result: 10,
          }),
        }
      );
      if (!response.ok) throw new Error('Erreur lors de la recherche RAG');

      // Streaming de la réponse markdown
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let fullText = '';
      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        const chunk = decoder.decode(value, { stream: true });
        fullText += chunk;
        setRagResult((prev) => prev + chunk); // Affiche au fur et à mesure
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      {/* Affichage des mots-clés générés */}
      {keywords && (
        <div style={{ marginBottom: '1em' }}>
          <h3>Mots-clés générés :</h3>
          <ul>
            {keywords.map((keyword, index) => (
              <li key={index}>{keyword}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Barre de recherche */}
      <form onSubmit={step === 1 ? handleGenerateKeywords : handleSimpleSearch}>
        <input
          type="text"
          value={recherche}
          onChange={(e) => setRecherche(e.target.value)}
          placeholder="Entrez votre recherche..."
          disabled={step === 2} // On ne change plus la recherche après la génération des mots-clés
        />
        <button type="submit" disabled={loading}>
          {loading
            ? 'Chargement...'
            : step === 1
            ? 'Générer les mots-clés'
            : 'Lancer la recherche'}
        </button>
        {step === 2 && (
          <button
            type="button"
            onClick={() => {
              setStep(1);
              setKeywords(null);
              setRagResult('');
            }}
            style={{ marginLeft: '1em' }}
          >
            Nouvelle recherche
          </button>
        )}
      </form>

      {/* Affichage des erreurs */}
      {error && <p style={{ color: 'red' }}>{error}</p>}

      {/* Résultat de la recherche RAG en markdown (streaming) */}
      {ragResult && (
        <div style={{ marginTop: '2em', background: '#f6f6f6', padding: '1em', borderRadius: '8px' }}>
          <h3>Réponse :</h3>
          <ReactMarkdown>{ragResult}</ReactMarkdown>
        </div>
      )}
    </div>
  );
}

export default BarreDeRecherche;
