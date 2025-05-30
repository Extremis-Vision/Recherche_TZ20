import React, { useState } from 'react';

function BarreDeRecherche() {
  const [recherche, setRecherche] = useState('');
  const [keywords, setKeywords] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
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
      setKeywords(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={recherche}
          onChange={(e) => setRecherche(e.target.value)}
          placeholder="Entrez votre recherche..."
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Chargement...' : 'G�n�rer les mots-cl�s'}
        </button>
      </form>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {keywords && (
        <div>
          <h3>Mots-clés générés :</h3>
          <ul>
            {keywords.questions.map((question, index) => (
              <li key={index}>{question}</li>
            ))}
          </ul>
          {/* Langue retir�e */}
          <p>Catégorie : {keywords.categorie}</p>
          <p>Peut être traité par une fonction locale spécifique ? : {keywords.boolean ? 'Oui' : 'Non'}</p>
        </div>
      )}
    </div>
  );
}

export default BarreDeRecherche;
