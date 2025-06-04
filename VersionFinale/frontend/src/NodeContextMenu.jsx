import React from "react";

const NodeContextMenu = ({ x, y, nodeLabel, onDelete, onCreateRelation, onClose }) => {
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
        minWidth: "200px",
        color: "#333",
      }}
    >
      <div style={{ marginBottom: "8px", fontWeight: "bold", color: "#000" }}>
        {nodeLabel}
      </div>
      <button
        onClick={(e) => {
          e.stopPropagation();
          onCreateRelation();
        }}
        style={{
          display: "block",
          width: "100%",
          padding: "6px",
          marginBottom: "4px",
          backgroundColor: "#f5f5f5",
          border: "1px solid #ddd",
          borderRadius: "4px",
          cursor: "pointer",
          color: "#333",
          textAlign: "left"
        }}
      >
        Créer relation
      </button>
      <button
        onClick={(e) => {
          e.stopPropagation();
          onDelete();
        }}
        style={{
          display: "block",
          width: "100%",
          padding: "6px",
          backgroundColor: "#fff0f0",
          border: "1px solid #ffcccc",
          borderRadius: "4px",
          cursor: "pointer",
          color: "#cc0000",
          textAlign: "left"
        }}
      >
        Supprimer
      </button>
    </div>
  );
};

export default NodeContextMenu;
