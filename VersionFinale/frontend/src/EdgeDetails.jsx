const EdgeDetails = ({ edge, onClose }) => {
  return (
    <div 
      style={{
        position: 'fixed',
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        backgroundColor: 'white',
        padding: '20px',
        borderRadius: '8px',
        boxShadow: '0 0 10px rgba(0,0,0,0.2)',
        zIndex: 1000,
        minWidth: '300px'
      }}
    >
      <h3 style={{ marginTop: 0 }}>Détails de la relation</h3>
      <p><strong>Type:</strong> {edge.data('label')}</p>
      <p><strong>Description:</strong> {edge.data('description') || "Aucune description"}</p>
      <p><strong>Source:</strong> {edge.data('source')}</p>
      <p><strong>Destination:</strong> {edge.data('target')}</p>
      <button 
        onClick={onClose}
        style={{
          padding: '8px 16px',
          marginTop: '16px',
          cursor: 'pointer'
        }}
      >
        Fermer
      </button>
    </div>
  );
};

export default EdgeDetails;
