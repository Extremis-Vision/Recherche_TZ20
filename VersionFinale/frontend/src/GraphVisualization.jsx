import React, { useEffect, useRef, useState } from "react";
import cytoscape from "cytoscape";
import coseBilkent from "cytoscape-cose-bilkent";
import NodeContextMenu from "./NodeContextMenu";
import "./GraphVisualization.css";

cytoscape.use(coseBilkent);

const GraphVisualization = ({ width = "100%", height = 600 }) => {
  const cyRef = useRef(null);
  const cyInstance = useRef(null);

  const [allNodes, setAllNodes] = useState([]);
  const [allEdges, setAllEdges] = useState([]);
  const [search, setSearch] = useState("");
  const [includeNeighbors, setIncludeNeighbors] = useState(false);

  const [contextMenu, setContextMenu] = useState({
    visible: false,
    x: 0,
    y: 0,
    nodeId: null,
    nodeLabel: "",
  });

  useEffect(() => {
    console.log("Initializing graph...");
    let cy;

    fetch("http://localhost:8888/nodebdd/GetAllNode/")
      .then((response) => response.json())
      .then((data) => {
        console.log("Raw data:", data);

        // Vérification et nettoyage des données
        const nodes = (data.nodes || [])
          .filter((node) => node.data && node.data.id)
          .map((node) => ({
            data: {
              ...node.data,
              displayLabel:
                node.data.displayLabel ||
                node.data.nom ||
                node.data.name ||
                node.data.id,
              backgroundcolor: node.data.backgroundcolor || "#267dc5",
            },
          }));

        const nodeIds = new Set(nodes.map((n) => n.data.id));

        const edges = (data.edges || [])
          .filter((edge) => {
            const hasValidIds = edge.data && edge.data.source && edge.data.target;
            const sourceExists = nodeIds.has(edge.data.source);
            const targetExists = nodeIds.has(edge.data.target);
            return hasValidIds && sourceExists && targetExists;
          })
          .map((edge) => ({
            data: {
              ...edge.data,
              id: edge.data.id || `edge-${edge.data.source}-${edge.data.target}`,
            },
          }));

        console.log("Processed nodes:", nodes);
        console.log("Processed edges:", edges);

        setAllNodes(nodes);
        setAllEdges(edges);

        if (!cyRef.current) {
          console.error("Container not found");
          return;
        }

        cy = cytoscape({
          container: cyRef.current,
          elements: [...nodes, ...edges],
          style: [
            {
              selector: "node",
              style: {
                "background-color": "data(backgroundcolor)",
                label: "data(displayLabel)",
                color: "#fff",
                "font-size": "14px",
                "text-valign": "center",
                "text-halign": "center",
                "border-width": 2,
                "border-color": "#333",
                "text-outline-width": 2,
                "text-outline-color": "#333",
                width: 60,
                height: 60,
              },
            },
            {
              selector: "node.highlighted",
              style: {
                "border-color": "#ffd700",
                "border-width": 4,
              },
            },
            {
              selector: "edge",
              style: {
                width: 2,
                "line-color": "#aaa",
                "target-arrow-shape": "triangle",
                "target-arrow-color": "#aaa",
                "curve-style": "bezier",
                label: "data(label)",
                "font-size": "12px",
                color: "#fff",
                "text-background-color": "#444",
                "text-background-opacity": 0.7,
                "text-background-padding": 2,
              },
            },
          ],
          layout: {
            name: "cose-bilkent",
            animate: false, // Désactiver l'animation initiale
            randomize: true,
            fit: true,
            padding: 50,
          },
        });

        cyInstance.current = cy;

        // Force layout render
        setTimeout(() => {
          if (cy) {
            cy.resize();
            cy.fit();
            cy.center();
          }
        }, 100);

        cy.on("cxttap", "node", (evt) => {
          const node = evt.target;
          const pos = evt.originalEvent;
          setContextMenu({
            visible: true,
            x: pos.clientX,
            y: pos.clientY,
            nodeId: node.data("id"),
            nodeLabel: node.data("displayLabel") || node.data("id"),
          });
        });

        cy.on("tap", (evt) => {
          if (contextMenu.visible) {
            setContextMenu((m) => ({ ...m, visible: false }));
          }
        });

        const handleResize = () => {
          if (cy) {
            cy.resize();
            cy.fit();
          }
        };

        window.addEventListener("resize", handleResize);

        return () => {
          window.removeEventListener("resize", handleResize);
          if (cy) {
            cy.destroy();
          }
        };
      })
      .catch((error) => {
        console.error("Error loading graph:", error);
      });

    return () => {
      if (cyInstance.current) {
        cyInstance.current.destroy();
        cyInstance.current = null;
      }
    };
  }, []);

  useEffect(() => {
    const cy = cyInstance.current;
    if (!cy) return;

    if (!search.trim()) {
      cy.elements().remove();
      cy.add([...allNodes, ...allEdges]);
      cy.layout({ name: "cose-bilkent", fit: true, animate: true }).run();
      return;
    }

    const searchLower = search.trim().toLowerCase();
    const matchedNodes = allNodes.filter((node) =>
      (node.data.displayLabel || "").toLowerCase().includes(searchLower)
    );

    let nodesToShow = [...matchedNodes];
    let edgesToShow = [];

    if (includeNeighbors) {
      const matchedIds = new Set(matchedNodes.map((n) => n.data.id));
      const neighborIds = new Set();

      allEdges.forEach((edge) => {
        const { source, target } = edge.data;
        if (matchedIds.has(source)) neighborIds.add(target);
        if (matchedIds.has(target)) neighborIds.add(source);
      });

      nodesToShow = [
        ...nodesToShow,
        ...allNodes.filter((node) => neighborIds.has(node.data.id)),
      ];

      const idsToShow = new Set(nodesToShow.map((n) => n.data.id));
      edgesToShow = allEdges.filter(
        (edge) =>
          idsToShow.has(edge.data.source) && idsToShow.has(edge.data.target)
      );
    } else {
      const matchedIds = new Set(matchedNodes.map((n) => n.data.id));
      edgesToShow = allEdges.filter(
        (edge) =>
          matchedIds.has(edge.data.source) && matchedIds.has(edge.data.target)
      );
    }

    cy.elements().remove();
    cy.add([...nodesToShow, ...edgesToShow]);
    cy.layout({ name: "cose-bilkent", fit: true, animate: true }).run();
  }, [search, includeNeighbors, allNodes, allEdges]);

  const handleDeleteNode = async () => {
    if (!contextMenu.nodeId) return;

    const nodeToDelete = allNodes.find((node) => node.data.id === contextMenu.nodeId);

    if (!nodeToDelete) {
      console.error("Node not found in the current graph data.");
      return;
    }

    const nodeDetails = `Node Details:\n\nID: ${nodeToDelete.data.id}\nLabel: ${nodeToDelete.data.displayLabel}\nDescription: ${nodeToDelete.data.description || 'No description'}\nColor: ${nodeToDelete.data.backgroundcolor || 'No color'}`;

    if (!window.confirm(`Supprimer le nœud:\n\n${nodeDetails}\n\nVoulez-vous vraiment supprimer ce nœud et toutes ses connexions?`)) {
      return;
    }

    try {
      console.log("Deleting node with ID:", contextMenu.nodeId);

      const response = await fetch("http://localhost:8888/nodebdd/SupprimerNode/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id: contextMenu.nodeId }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(`Erreur lors de la suppression du nœud: ${JSON.stringify(errorData)}`);
      }

      const cy = cyInstance.current;
      if (cy) {
        const node = cy.getElementById(contextMenu.nodeId);
        node.remove();
      }
      setContextMenu({ ...contextMenu, visible: false });
    } catch (error) {
      console.error("Erreur lors de la suppression du nœud:", error);
      alert(error.message || "Erreur lors de la suppression du nœud.");
    }
  };

  useEffect(() => {
    const closeMenu = () => {
      if (contextMenu.visible) {
        setContextMenu((m) => ({ ...m, visible: false }));
      }
    };

    if (contextMenu.visible) {
      document.addEventListener("click", closeMenu);
    }

    return () => {
      document.removeEventListener("click", closeMenu);
    };
  }, [contextMenu.visible]);

  return (
    <div
      className="graph-container"
      style={{
        width,
        height,
        position: "relative",
        border: "1px solid #ccc", // Aide visuelle pour voir le conteneur
        background: "#f5f5f5",     // Couleur de fond pour voir la zone
      }}
    >
      <div style={{ marginBottom: 8, display: "flex", alignItems: "center", gap: 8 }}>
        <input
          className="barre-recherche"
          type="text"
          placeholder="Rechercher un nœud..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          style={{
            padding: "6px 10px",
            border: "1px solid #aaa",
            borderRadius: 4,
            fontSize: 14,
          }}
        />
        <label style={{ fontSize: 13, display: "flex", alignItems: "center", gap: 4 }}>
          <input
            type="checkbox"
            checked={includeNeighbors}
            onChange={(e) => setIncludeNeighbors(e.target.checked)}
            style={{ marginRight: 4 }}
          />
          Inclure voisins
        </label>
      </div>
      <div
        ref={cyRef}
        style={{
          width: "100%",
          height: `calc(100% - 50px)`,
          minHeight: "300px", // Hauteur minimum garantie
          background: "#fff",  // Fond blanc pour le graphe
        }}
      />
      {contextMenu.visible && (
        <NodeContextMenu
          x={contextMenu.x}
          y={contextMenu.y}
          nodeLabel={contextMenu.nodeLabel}
          onDelete={handleDeleteNode}
          onClose={() => setContextMenu((m) => ({ ...m, visible: false }))}
        />
      )}
    </div>
  );
};

export default GraphVisualization;
