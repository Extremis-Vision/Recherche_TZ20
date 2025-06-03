import React, { useState, useEffect } from 'react';

function Accueil() {
  const [espaces, setEspaces] = useState([]);
  const [nouvelEspace, setNouvelEspace] = useState({ subject: '', objectif: '', couleur: '#267dc5' });
  const [selectedEspace, setSelectedEspace] = useState(null);
  const [selectedEspaceDetails, setSelectedEspaceDetails] = useState(null);
  const [recherches, setRecherches] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Panneau latéral
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [search, setSearch] = useState('');

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
  }, [selectedEspace]);

  // Récupérer tous les espaces (pour la sidebar SEULEMENT)
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
      if (selectedEspace && selectedEspace.id === idEspace) {
        setSelectedEspace(null);
        setSelectedEspaceDetails(null);
        setRecherches([]);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Clic sur un espace dans la sidebar
  const handleSidebarClick = (espace) => {
    setSelectedEspace(espace);
    setSidebarOpen(false);
  };

  // Espaces filtrés selon la recherche
  const filteredEspaces = espaces.filter(
    espace =>
      espace.subject.toLowerCase().includes(search.toLowerCase()) ||
      espace.objectif.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div style={{ maxWidth: 1000, margin: 'auto', padding: 30, display: 'flex' }}>
      {/* Sidebar historique */}
      <div
        style={{
          width: sidebarOpen ? 280 : 0,
          transition: 'width 0.3s',
          overflow: 'hidden',
          background: '#f9f9f9',
          borderRight: '1px solid #eee',
          minHeight: '100vh',
          position: 'relative',
        }}
      >
        <button
          onClick={() => setSidebarOpen(false)}
          style={{
            position: 'absolute',
            top: 10,
            right: -30,
            background: '#267dc5',
            color: '#fff',
            border: 'none',
            borderRadius: '0 6px 6px 0',
            padding: '6px 10px',
            cursor: 'pointer',
            zIndex: 2,
            boxShadow: '1px 2px 8px #0002'
          }}
          title="Fermer l'historique"
        >
          ←
        </button>
        <div style={{ padding: sidebarOpen ? 16 : 0, opacity: sidebarOpen ? 1 : 0, transition: 'opacity 0.2s' }}>
          <h3 style={{ fontSize: 18, marginBottom: 10 }}>Espaces</h3>
          {/* Barre de recherche */}
          <input
            type="text"
            value={search}
            onChange={e => setSearch(e.target.value)}
            placeholder="Rechercher un espace..."
            style={{
              width: '100%',
              marginBottom: 12,
              padding: '8px 12px',
              borderRadius: 20,
              border: '1.5px solid #b6b6b6',
              fontSize: 15,
              background: '#fff',
              boxShadow: '0 1px 4px #0001',
              outline: 'none',
              transition: 'border 0.2s',
            }}
          />
          {filteredEspaces.length === 0 && (
            <div style={{ color: '#aaa', fontStyle: 'italic' }}>Aucun espace</div>
          )}
          <ul style={{ listStyle: 'none', padding: 0 }}>
            {filteredEspaces.map((espace) => (
              <li key={espace.id} style={{ marginBottom: 8, display: 'flex', alignItems: 'center' }}>
                <button
                  onClick={() => handleSidebarClick(espace)}
                  style={{
                    background: selectedEspace && selectedEspace.id === espace.id ? '#267dc5' : '#e0e0e0',
                    color: selectedEspace && selectedEspace.id === espace.id ? '#fff' : '#333',
                    border: 'none',
                    borderRadius: 6,
                    padding: '0.5em 1em',
                    cursor: 'pointer',
                    width: '100%',
                    textAlign: 'left',
                    fontWeight: 'bold'
                  }}
                >
                  {espace.subject} <span style={{ color: '#b6e' }}>({espace.objectif})</span>
                </button>
                <button
                  onClick={() => handleDeleteEspace(espace.id)}
                  style={{
                    marginLeft: 6,
                    background: '#b71c1c',
                    color: '#fff',
                    border: 'none',
                    borderRadius: 6,
                    padding: '0.3em 0.7em',
                    cursor: 'pointer',
                  }}
                  title="Supprimer l'espace"
                >
                  ✕
                </button>
              </li>
            ))}
          </ul>
        </div>
      </div>
      {/* Bouton pour ouvrir la sidebar */}
      {!sidebarOpen && (
        <button
          onClick={() => setSidebarOpen(true)}
          style={{
            position: 'fixed',
            top: 20,
            left: 10,
            background: '#267dc5',
            color: '#fff',
            border: 'none',
            borderRadius: '6px',
            padding: '6px 12px',
            cursor: 'pointer',
            zIndex: 10,
            boxShadow: '1px 2px 8px #0002'
          }}
          title="Ouvrir les espaces"
        >
          ≡
        </button>
      )}
      {/* Contenu principal */}
      <div style={{ flex: 1, minWidth: 0 }}>
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
    </div>
  );
}

export default Accueil;
