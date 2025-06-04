import React from "react";

const NodeContextMenu = ({ x, y, onDelete, onClose, nodeLabel }) => {
  return (
    <div
      style={{
        position: "fixed",
        top: y,
        left: x,
        background: "#fff",
        border: "1px solid #ccc",
        borderRadius: 8,
        boxShadow: "0 2px 8px #0002",
        zIndex: 10000,
        minWidth: 160,
        padding: 0,
      }}
      onContextMenu={e => e.preventDefault()}
    >
      <div style={{ padding: "10px 16px", borderBottom: "1px solid #eee", fontWeight: "bold" }}>
        {nodeLabel}
      </div>
      <button
        style={{
          width: "100%",
          padding: "10px 16px",
          background: "#b71c1c",
          color: "#fff",
          border: "none",
          borderRadius: "0 0 8px 8px",
          cursor: "pointer",
          fontWeight: "bold",
        }}
        onClick={onDelete}
      >
        Supprimer le nœud
      </button>
      <button
        style={{
          display: "none"
        }}
        onClick={onClose}
        tabIndex={-1}
      >
        Fermer
      </button>
    </div>
  );
};

export default NodeContextMenu;
