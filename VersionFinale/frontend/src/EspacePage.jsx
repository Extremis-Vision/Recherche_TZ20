import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';

function EspacePage() {
  const { id } = useParams();
  const [details, setDetails] = useState(null);
  const [recherches, setRecherches] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchDetails = async () => {
      setLoading(true);
      try {
        const res = await fetch(`http://localhost:8888/bdd/GetEspaceRecherche/?id=${id}`);
        const data = await res.json();
        setDetails(data);
      } catch {
        setDetails(null);
      }
      setLoading(false);
    };
    fetchDetails();
  }, [id]);

  useEffect(() => {
    const fetchRecherches = async () => {
      try {
        const res = await fetch(`http://localhost:8888/bdd/GetRecherches/?id_Espaces_Recherches=${id}`);
        const data = await res.json();
        setRecherches(data);
      } catch {
        setRecherches([]);
      }
    };
    fetchRecherches();
  }, [id]);

  if (loading) return <div>Chargement...</div>;
  if (!details) return <div>Espace introuvable</div>;

  return (
    <div style={{ maxWidth: 800, margin: 'auto', padding: 30 }}>
      <button onClick={() => navigate(-1)} style={{ marginBottom: 20 }}>← Retour</button>
      <h2>Détail de l’espace</h2>
      <pre style={{ background: '#eee', padding: 10, borderRadius: 5 }}>
        {JSON.stringify(details, null, 2)}
      </pre>
      <h3>Recherches associées</h3>
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
  );
}

export default EspacePage;
