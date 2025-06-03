import React from 'react';

const SearchBar = ({ recherche, setRecherche, loading, step, onSubmit, onNewSearch }) => (
  <form onSubmit={onSubmit}>
    <input
      type="text"
      value={recherche}
      onChange={(e) => setRecherche(e.target.value)}
      placeholder="Tape ta recherche ici..."
      className="search-bar"
      disabled={step === 2}
    />
    <button type="submit" disabled={loading || (step === 1 && !recherche)}>
      {loading ? 'Chargement...' : step === 1 ? 'Générer les mots-clés' : 'Lancer la recherche'}
    </button>
    {step === 2 && (
      <button type="button" onClick={onNewSearch} style={{ marginLeft: '1em' }}>
        Nouvelle recherche
      </button>
    )}
  </form>
);

export default SearchBar;
