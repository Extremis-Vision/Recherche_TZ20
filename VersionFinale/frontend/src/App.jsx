import { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import './App.css';

function App() {
  const [recherche, setRecherche] = useState('');
  const [keywords, setKeywords] = useState(null);
  const [editingKeywordIndex, setEditingKeywordIndex] = useState(null);
  const [editingKeywordValue, setEditingKeywordValue] = useState('');
  const [addingKeyword, setAddingKeyword] = useState(false);
  const [newKeyword, setNewKeyword] = useState('');
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
    setEditingKeywordIndex(null);
    setEditingKeywordValue('');
    setAddingKeyword(false);
    setNewKeyword('');
  };

  // Supprimer un mot-clé
  const handleDeleteKeyword = (index) => {
    setKeywords((prev) => prev.filter((_, i) => i !== index));
    if (editingKeywordIndex === index) {
      setEditingKeywordIndex(null);
      setEditingKeywordValue('');
    }
  };

  // Cliquer sur un mot-clé pour le modifier
  const handleEditKeyword = (index) => {
    setEditingKeywordIndex(index);
    setEditingKeywordValue(keywords[index]);
  };

  // Valider la modification du mot-clé
  const handleEditKeywordSubmit = (e) => {
    e.preventDefault();
    if (editingKeywordValue.trim() === '') return;
    setKeywords((prev) =>
      prev.map((kw, i) => (i === editingKeywordIndex ? editingKeywordValue.trim() : kw))
    );
    setEditingKeywordIndex(null);
    setEditingKeywordValue('');
  };

  // Annuler la modification du mot-clé
  const handleEditKeywordCancel = () => {
    setEditingKeywordIndex(null);
    setEditingKeywordValue('');
  };

  // Ajouter un mot-clé
  const handleAddKeyword = (e) => {
    e.preventDefault();
    const value = newKeyword.trim();
    if (!value) return;
    if (keywords && keywords.includes(value)) {
      setNewKeyword('');
      setAddingKeyword(false);
      return; // Pas de doublon
    }
    setKeywords((prev) => (prev ? [...prev, value] : [value]));
    setNewKeyword('');
    setAddingKeyword(false);
  };

  return (
    <div className="container">
      <h1>Recherche de mots-clés IA</h1>

      {/* Affichage des mots-clés générés */}
      {keywords && (
        <div className="result" style={{ marginBottom: '1em' }}>
          <h2>Mots-clés générés :</h2>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5em', alignItems: 'center' }}>
            {keywords.map((keyword, index) =>
              editingKeywordIndex === index ? (
                <form
                  key={index}
                  onSubmit={handleEditKeywordSubmit}
                  style={{
                    display: 'inline-flex',
                    alignItems: 'center',
                    background: '#e0e0e0',
                    borderRadius: '16px',
                    padding: '0.2em 0.6em',
                  }}
                >
                  <input
                    type="text"
                    value={editingKeywordValue}
                    autoFocus
                    onChange={(e) => setEditingKeywordValue(e.target.value)}
                    style={{
                      border: 'none',
                      outline: 'none',
                      background: 'transparent',
                      fontSize: '1em',
                      width: '7em',
                    }}
                  />
                  <button
                    type="submit"
                    style={{
                      marginLeft: '0.3em',
                      border: 'none',
                      background: 'transparent',
                      cursor: 'pointer',
                      color: 'green',
                      fontWeight: 'bold',
                    }}
                    title="Valider"
                  >
                    ✓
                  </button>
                  <button
                    type="button"
                    onClick={handleEditKeywordCancel}
                    style={{
                      marginLeft: '0.1em',
                      border: 'none',
                      background: 'transparent',
                      cursor: 'pointer',
                      color: 'red',
                      fontWeight: 'bold',
                    }}
                    title="Annuler"
                  >
                    ✗
                  </button>
                </form>
              ) : (
                <span
                  key={index}
                  style={{
                    display: 'inline-flex',
                    alignItems: 'center',
                    background: '#e0e0e0',
                    borderRadius: '16px',
                    padding: '0.2em 0.6em',
                    cursor: 'pointer',
                    fontSize: '1em',
                  }}
                  onClick={() => handleEditKeyword(index)}
                  title="Cliquez pour modifier"
                >
                  {keyword}
                  <span
                    onClick={(e) => {
                      e.stopPropagation();
                      handleDeleteKeyword(index);
                    }}
                    style={{
                      marginLeft: '0.4em',
                      color: '#b71c1c',
                      fontWeight: 'bold',
                      cursor: 'pointer',
                      fontSize: '1.1em',
                    }}
                    title="Supprimer"
                  >
                    ×
                  </span>
                </span>
              )
            )}
            {/* Ajout du bouton + et du champ d'ajout */}
            {addingKeyword ? (
              <form
                onSubmit={handleAddKeyword}
                style={{
                  display: 'inline-flex',
                  alignItems: 'center',
                  background: '#e0e0e0',
                  borderRadius: '16px',
                  padding: '0.2em 0.6em',
                  marginLeft: '0.5em',
                }}
              >
                <input
                  type="text"
                  value={newKeyword}
                  autoFocus
                  onChange={(e) => setNewKeyword(e.target.value)}
                  style={{
                    border: 'none',
                    outline: 'none',
                    background: 'transparent',
                    fontSize: '1em',
                    width: '7em',
                  }}
                  placeholder="Nouveau mot-clé"
                />
                <button
                  type="submit"
                  style={{
                    marginLeft: '0.3em',
                    border: 'none',
                    background: 'transparent',
                    cursor: 'pointer',
                    color: 'green',
                    fontWeight: 'bold',
                  }}
                  title="Ajouter"
                >
                  ✓
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setAddingKeyword(false);
                    setNewKeyword('');
                  }}
                  style={{
                    marginLeft: '0.1em',
                    border: 'none',
                    background: 'transparent',
                    cursor: 'pointer',
                    color: 'red',
                    fontWeight: 'bold',
                  }}
                  title="Annuler"
                >
                  ✗
                </button>
              </form>
            ) : (
              <button
                type="button"
                onClick={() => setAddingKeyword(true)}
                style={{
                  marginLeft: '0.5em',
                  border: 'none',
                  background: '#e0e0e0',
                  borderRadius: '16px',
                  padding: '0.2em 0.6em',
                  cursor: 'pointer',
                  fontSize: '1em',
                  color: '#1976d2',
                  fontWeight: 'bold',
                }}
                title="Ajouter un mot-clé"
              >
                + Ajouter un mot-clé
              </button>
            )}
          </div>
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