import React, { useEffect } from "react";

const EdgeContextMenu = ({ x, y, edge, onUpdate, onClose }) => {
  useEffect(() => {
    const handleClickOutside = (event) => {
      // Si le clic est en dehors du menu
      if (!event.target.closest('.edge-context-menu')) {
        onClose();
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [onClose]);

  return (
    <div
      className="edge-context-menu"
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
        minWidth: "200px",
        color: "#333",  // Couleur du texte
      }}
    >
      <h4 style={{ margin: "0 0 8px 0", color: "#000" }}>Type: {edge.data("label")}</h4>
      <p style={{ margin: "4px 0", color: "#333" }}>Description: {edge.data("description") || "Aucune description"}</p>
      <div style={{ borderTop: "1px solid #eee", marginTop: "8px", paddingTop: "8px" }}>
        <button
          onClick={onClose}
          style={{
            display: "block",
            width: "100%",
            padding: "6px",
            backgroundColor: "#f5f5f5",
            border: "1px solid #ddd",
            borderRadius: "4px",
            cursor: "pointer",
            color: "#333",
            textAlign: "center",
            marginTop: "4px"
          }}
        >
          Fermer
        </button>
      </div>
    </div>
  );
};

export default EdgeContextMenu;
