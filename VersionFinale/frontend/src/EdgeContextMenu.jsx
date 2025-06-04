const EdgeContextMenu = ({ x, y, edge, onUpdate, onClose }) => {
  return (
    <div
      style={{
        position: "fixed",
        left: x,
        top: y,
        backgroundColor: "white",
        border: "1px solid #ccc",
        borderRadius: "4px",
        padding: "8px",
        boxShadow: "2px 2px 5px rgba(0,0,0,0.2)",
        zIndex: 1000,
      }}
    >
      <h4 style={{ margin: "0 0 8px 0" }}>Relation: {edge.data("label")}</h4>
      <p style={{ margin: "4px 0" }}>Description: {edge.data("description") || "Aucune description"}</p>
      <button
        onClick={() => {
          const newType = prompt("Nouveau type de relation:", edge.data("label"));
          const newDescription = prompt("Nouvelle description:", edge.data("description"));
          if (newType !== null) {
            onUpdate(edge, newType, newDescription);
          }
        }}
        style={{
          display: "block",
          width: "100%",
          padding: "4px 12px",
          marginTop: "8px",
          border: "1px solid #ccc",
          borderRadius: "4px",
          background: "white",
          cursor: "pointer",
        }}
      >
        Modifier
      </button>
    </div>
  );
};

export default EdgeContextMenu;
