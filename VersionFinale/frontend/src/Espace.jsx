import React, { useState, useEffect } from 'react';

function Accueil() {
  const [espaces, setEspaces] = useState([]);
  const [nouvelEspace, setNouvelEspace] = useState({ subject: '', objectif: '', couleur: '#267dc5' });
  const [selectedEspace, setSelectedEspace] = useState(null);
  const [selectedEspaceDetails, setSelectedEspaceDetails] = useState(null);
  const [recherches, setRecherches] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Charger la liste des espaces au chargement de la page
  useEffect(() => {
    fetchEspaces();
  }, []);

  // Charger les recherches et détails quand on sélectionne un espace
  useEffect(() => {
    if (selectedEspace) {
      fetchEspaceDetails(selectedEspace.id);
      fetchRecherches(selectedEspace.id);
    } else {
      setSelectedEspaceDetails(null);
      setRecherches([]);
    }
    // eslint-disable-next-line
  }, [selectedEspace]);

  // Récupérer tous les espaces
  const fetchEspaces = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch('http://localhost:8888/bdd/GetEspaceRecherches/');
      if (!response.ok) throw new Error('Erreur lors de la récupération des espaces');
      const data = await response.json();
      setEspaces(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Créer un nouvel espace
  const handleCreateEspace = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const response = await fetch('http://localhost:8888/bdd/CreeEspaceRecherche/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(nouvelEspace),
      });
      if (!response.ok) throw new Error('Erreur lors de la création de l\'espace');
      setNouvelEspace({ subject: '', objectif: '', couleur: '#267dc5' });
      await fetchEspaces();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Récupérer les détails d'un espace
  const fetchEspaceDetails = async (idEspace) => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`http://localhost:8888/bdd/GetEspaceRecherche/?id=${idEspace}`);
      if (!response.ok) throw new Error("Erreur lors de la récupération du détail de l'espace");
      const data = await response.json();
      setSelectedEspaceDetails(data);
    } catch (err) {
      setError(err.message);
      setSelectedEspaceDetails(null);
    } finally {
      setLoading(false);
    }
  };

  // Récupérer les recherches d'un espace
  const fetchRecherches = async (idEspace) => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`http://localhost:8888/bdd/GetRecherches/?id_Espaces_Recherches=${idEspace}`);
      if (!response.ok) throw new Error('Erreur lors de la récupération des recherches');
      const data = await response.json();
      setRecherches(data);
    } catch (err) {
      setError(err.message);
      setRecherches([]);
    } finally {
      setLoading(false);
    }
  };

  // Supprimer un espace
  const handleDeleteEspace = async (idEspace) => {
    if (!window.confirm("Supprimer cet espace de recherche ?")) return;
    setLoading(true);
    setError(null);
    try {
      const response = await fetch('http://localhost:8888/bdd/SupprimerEspaceRecherche/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id_espace: idEspace }),
      });
      if (!response.ok) throw new Error("Erreur lors de la suppression de l'espace");
      await fetchEspaces();
      setSelectedEspace(null);
      setSelectedEspaceDetails(null);
      setRecherches([]);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 700, margin: 'auto', padding: 30 }}>
      <h1>Accueil - Espaces de Recherche</h1>

      {/* Formulaire de création d'espace */}
      <form onSubmit={handleCreateEspace} style={{ marginBottom: '2em', background: '#f6f6f6', padding: 20, borderRadius: 8 }}>
        <h2>Créer un nouvel espace</h2>
        <input
          type="text"
          value={nouvelEspace.subject}
          onChange={e => setNouvelEspace({ ...nouvelEspace, subject: e.target.value })}
          placeholder="Sujet"
          required
          style={{ marginRight: 10 }}
        />
        <input
          type="text"
          value={nouvelEspace.objectif}
          onChange={e => setNouvelEspace({ ...nouvelEspace, objectif: e.target.value })}
          placeholder="Objectif"
          required
          style={{ marginRight: 10 }}
        />
        <input
          type="color"
          value={nouvelEspace.couleur}
          onChange={e => setNouvelEspace({ ...nouvelEspace, couleur: e.target.value })}
          style={{ width: 40, height: 40, verticalAlign: 'middle', marginRight: 10 }}
        />
        <button type="submit" disabled={loading}>Créer</button>
      </form>

      {/* Liste des espaces */}
      <h2>Espaces existants</h2>
      <ul style={{ listStyle: 'none', padding: 0 }}>
        {espaces.map(espace => (
          <li key={espace.id} style={{ marginBottom: 10, display: 'flex', alignItems: 'center' }}>
            <button
              style={{
                background: selectedEspace && selectedEspace.id === espace.id ? '#267dc5' : '#e0e0e0',
                color: selectedEspace && selectedEspace.id === espace.id ? '#fff' : '#333',
                border: 'none',
                borderRadius: 6,
                padding: '0.5em 1em',
                cursor: 'pointer',
                fontWeight: 'bold',
              }}
              onClick={() => setSelectedEspace(espace)}
            >
              {espace.subject} ({espace.objectif})
            </button>
            <button
              onClick={() => handleDeleteEspace(espace.id)}
              style={{
                marginLeft: 10,
                background: '#b71c1c',
                color: '#fff',
                border: 'none',
                borderRadius: 6,
                padding: '0.3em 0.7em',
                cursor: 'pointer',
              }}
              title="Supprimer l'espace"
            >
              Supprimer
            </button>
          </li>
        ))}
      </ul>

      {/* Affichage des détails et recherches de l'espace sélectionné */}
      {selectedEspaceDetails && (
        <div style={{ marginTop: 30, background: '#f6f6f6', padding: 20, borderRadius: 8 }}>
          <h3>Détail de l’espace</h3>
          <pre style={{ background: '#eee', padding: 10, borderRadius: 5 }}>
            {JSON.stringify(selectedEspaceDetails, null, 2)}
          </pre>
          <h4>Recherches pour : {selectedEspace && selectedEspace.subject}</h4>
          {recherches.length === 0 ? (
            <p>Aucune recherche pour cet espace.</p>
          ) : (
            <ul>
              {recherches.map(rech => (
                <li key={rech.id}>
                  <b>{rech.prompt}</b> — <span>{rech.response}</span>
                </li>
              ))}
            </ul>
          )}
        </div>
      )}

      {error && <p style={{ color: 'red', marginTop: 20 }}>{error}</p>}
    </div>
  );
}

export default Accueil;
