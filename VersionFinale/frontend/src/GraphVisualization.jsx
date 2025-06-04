import React, { useEffect, useRef, useState } from "react";
import cytoscape from "cytoscape";
import coseBilkent from "cytoscape-cose-bilkent";
import NodeContextMenu from "./NodeContextMenu";
import EdgeContextMenu from "./EdgeContextMenu";
import EdgeDetails from './EdgeDetails';
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

  const [edgeContextMenu, setEdgeContextMenu] = useState({
    visible: false,
    x: 0,
    y: 0,
    edge: null,
  });

  const [showCreateForm, setShowCreateForm] = useState(false);
  const [showRelationForm, setShowRelationForm] = useState(false);
  const [newNode, setNewNode] = useState({ nom: '', description: '', couleur: '#267dc5' });
  const [newRelation, setNewRelation] = useState({ source: '', target: '', type: '', description: '' });
  const [relationSource, setRelationSource] = useState(null);
  const [isCreatingRelation, setIsCreatingRelation] = useState(false);
  const [newRelationType, setNewRelationType] = useState("");
  const [newRelationDescription, setNewRelationDescription] = useState("");
  const [selectedEdge, setSelectedEdge] = useState(null);

  useEffect(() => {
    console.log("Initializing graph...");

    fetch("http://localhost:8888/nodebdd/GetAllNode/")
      .then((response) => response.json())
      .then((data) => {
        console.log("Raw data received:", data);

        if (!data.nodes || !data.edges) {
          console.error("Invalid data format received:", data);
          return;
        }

        // Filtrer et traiter les nœuds
        const nodes = data.nodes
          .filter(node => node.data && node.data.id)
          .map(node => ({
            group: 'nodes',
            data: {
              ...node.data,
              id: String(node.data.id),
              label: node.data.displayLabel || node.data.nom || node.data.name || String(node.data.id)
            }
          }));

        const validNodeIds = new Set(nodes.map(n => n.data.id));
        console.log("Valid node IDs:", validNodeIds);

        // Filtrer et traiter les arêtes
        const edges = data.edges
          .filter(edge => {
            if (!edge.data || !edge.data.source || !edge.data.target) {
              console.warn("Invalid edge data:", edge);
              return false;
            }
            const sourceExists = validNodeIds.has(String(edge.data.source));
            const targetExists = validNodeIds.has(String(edge.data.target));
            if (!sourceExists || !targetExists) {
              console.warn(`Skipping edge - missing nodes:`, edge.data);
              return false;
            }
            return true;
          })
          .map(edge => ({
            group: 'edges',
            data: {
              ...edge.data,
              id: String(edge.data.id),
              source: String(edge.data.source),
              target: String(edge.data.target),
              label: edge.data.label || ''
            }
          }));

        setAllNodes(nodes);
        setAllEdges(edges);

        if (!cyRef.current) {
          console.error("Container not found");
          return;
        }

        const cy = cytoscape({
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

        cy.on("cxttap", "edge", (evt) => {
          const edge = evt.target;
          const pos = evt.originalEvent;
          setEdgeContextMenu({
            visible: true,
            x: pos.clientX,
            y: pos.clientY,
            edge: edge,
          });
          evt.preventDefault();
        });

        cy.on("tap", "edge", (evt) => {
          const edge = evt.target;
          setSelectedEdge(edge);
        });

        cy.on("tap", (evt) => {
          if (evt.target === cy) {
            // Si on clique sur le fond
            setContextMenu((m) => ({ ...m, visible: false }));
            setEdgeContextMenu((m) => ({ ...m, visible: false }));
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

  const handleCreateNode = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch("http://localhost:8888/nodebdd/CreeNoeud/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(newNode),
      });

      if (!response.ok) throw new Error("Erreur lors de la création du nœud");
      
      // Recharger le graphe
      window.location.reload();
      setShowCreateForm(false);
    } catch (error) {
      console.error("Erreur:", error);
      alert("Erreur lors de la création du nœud");
    }
  };

  const handleCreateRelation = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch("http://localhost:8888/nodebdd/CreeRelation/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          id_source: newRelation.source,
          id_target: newRelation.target,
          type: newRelation.type.trim(),  // S'assurer qu'il n'y a pas d'espaces superflus
          description: newRelation.description
        }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Erreur lors de la création de la relation");
      }
      
      // Recharger le graphe
      window.location.reload();
      setShowRelationForm(false);
    } catch (error) {
      console.error("Erreur:", error);
      alert("Erreur lors de la création de la relation: " + error.message);
    }
  };

  const handleStartCreateRelation = () => {
    setIsCreatingRelation(true);
    setRelationSource(contextMenu.nodeId);
    setContextMenu((m) => ({ ...m, visible: false }));
  };

  const handleNodeClick = async (node) => {
    if (isCreatingRelation && relationSource) {
      const type = prompt("Type de relation :");
      if (!type) {
        setIsCreatingRelation(false);
        setRelationSource(null);
        return;
      }
      
      const description = prompt("Description de la relation (optionnel) :");
      
      try {
        const response = await fetch("http://localhost:8888/nodebdd/CreeRelation/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            id_source: relationSource,
            id_target: node.id(),
            type: type,
            description: description || ""
          }),
        });

        if (!response.ok) {
          const error = await response.json();
          throw new Error(error.detail || "Erreur lors de la création de la relation");
        }
        
        // Recharger le graphe
        window.location.reload();
      } catch (error) {
        console.error("Erreur:", error);
        alert(error.message || "Erreur lors de la création de la relation");
      }
      
      setIsCreatingRelation(false);
      setRelationSource(null);
    }
  };

  useEffect(() => {
    const cy = cyInstance.current;
    if (!cy) return;

    cy.on("tap", "node", (evt) => {
      const node = evt.target;
      if (isCreatingRelation) {
        handleNodeClick(node);
      }
    });
  }, [isCreatingRelation]);

  useEffect(() => {
    const closeMenu = () => {
      if (contextMenu.visible) {
        setContextMenu((m) => ({ ...m, visible: false }));
      }
      if (edgeContextMenu.visible) {
        setEdgeContextMenu((m) => ({ ...m, visible: false }));
      }
    };

    if (contextMenu.visible || edgeContextMenu.visible) {
      document.addEventListener("click", closeMenu);
    }

    return () => {
      document.removeEventListener("click", closeMenu);
    };
  }, [contextMenu.visible, edgeContextMenu.visible]);

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
      <div style={{ marginBottom: 8, display: "flex", alignItems: "center", gap: 8, flexWrap: "wrap" }}>
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
        <button onClick={() => setShowCreateForm(true)} style={{ padding: "6px 12px" }}>
          Nouveau Nœud
        </button>
        <button onClick={() => setShowRelationForm(true)} style={{ padding: "6px 12px" }}>
          Nouvelle Relation
        </button>
      </div>

      {/* Modifier le style des modales */}
      {showCreateForm && (
        <div className="modal" style={{
          position: 'fixed',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          background: 'white',
          padding: '20px',
          borderRadius: '8px',
          boxShadow: '0 0 10px rgba(0,0,0,0.5)',
          zIndex: 1000,
          color: '#333', // Couleur du texte
        }}>
          <h3 style={{ color: '#333' }}>Créer un nouveau nœud</h3>
          <form onSubmit={handleCreateNode}>
            <input
              type="text"
              placeholder="Nom"
              value={newNode.nom}
              onChange={(e) => setNewNode({...newNode, nom: e.target.value})}
              style={{ display: 'block', margin: '10px 0' }}
            />
            <input
              type="text"
              placeholder="Description"
              value={newNode.description}
              onChange={(e) => setNewNode({...newNode, description: e.target.value})}
              style={{ display: 'block', margin: '10px 0' }}
            />
            <input
              type="color"
              value={newNode.couleur}
              onChange={(e) => setNewNode({...newNode, couleur: e.target.value})}
              style={{ display: 'block', margin: '10px 0' }}
            />
            <button type="submit">Créer</button>
            <button type="button" onClick={() => setShowCreateForm(false)}>Annuler</button>
          </form>
        </div>
      )}

      {showRelationForm && (
        <div className="modal" style={{
          position: 'fixed', top: '50%', left: '50%', transform: 'translate(-50%, -50%)',
          background: 'white', padding: '20px', borderRadius: '8px', boxShadow: '0 0 10px rgba(0,0,0,0.5)',
          zIndex: 1000
        }}>
          <h3>Créer une nouvelle relation</h3>
          <form onSubmit={handleCreateRelation}>
            <select
              value={newRelation.source}
              onChange={(e) => setNewRelation({...newRelation, source: e.target.value})}
              style={{ display: 'block', margin: '10px 0' }}
            >
              <option value="">Sélectionner source</option>
              {allNodes.map(node => (
                <option key={node.data.id} value={node.data.id}>
                  {node.data.displayLabel || node.data.nom || node.data.id}
                </option>
              ))}
            </select>
            <select
              value={newRelation.target}
              onChange={(e) => setNewRelation({...newRelation, target: e.target.value})}
              style={{ display: 'block', margin: '10px 0' }}
            >
              <option value="">Sélectionner cible</option>
              {allNodes.map(node => (
                <option key={node.data.id} value={node.data.id}>
                  {node.data.displayLabel || node.data.nom || node.data.id}
                </option>
              ))}
            </select>
            <input
              type="text"
              placeholder="Type de relation"
              value={newRelation.type}
              onChange={(e) => setNewRelation({...newRelation, type: e.target.value})}
              style={{ display: 'block', margin: '10px 0' }}
            />
            <input
              type="text"
              placeholder="Description"
              value={newRelation.description}
              onChange={(e) => setNewRelation({...newRelation, description: e.target.value})}
              style={{ display: 'block', margin: '10px 0' }}
            />
            <button type="submit">Créer</button>
            <button type="button" onClick={() => setShowRelationForm(false)}>Annuler</button>
          </form>
        </div>
      )}

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
          onCreateRelation={handleStartCreateRelation}
          onClose={() => setContextMenu((m) => ({ ...m, visible: false }))}
        />
      )}
      {edgeContextMenu.visible && (
        <EdgeContextMenu
          x={edgeContextMenu.x}
          y={edgeContextMenu.y}
          edge={edgeContextMenu.edge}
          onClose={() => setEdgeContextMenu({ visible: false, x: 0, y: 0, edge: null })}
        />
      )}
      {selectedEdge && (
        <div style={{
          position: 'fixed',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          backgroundColor: 'white',
          padding: '20px',
          borderRadius: '8px',
          boxShadow: '0 0 10px rgba(0,0,0,0.2)',
          zIndex: 1000,
          color: '#333', // Couleur du texte
        }}>
          <h3 style={{ marginTop: 0, color: '#333' }}>Détails de la relation</h3>
          <p style={{ color: '#666' }}><strong>Type:</strong> {selectedEdge.data('label')}</p>
          <p style={{ color: '#666' }}><strong>Description:</strong> {selectedEdge.data('description') || "Aucune description"}</p>
          <p style={{ color: '#666' }}><strong>Source:</strong> {selectedEdge.data('source')}</p>
          <p style={{ color: '#666' }}><strong>Destination:</strong> {selectedEdge.data('target')}</p>
          <button 
            onClick={() => setSelectedEdge(null)}
            style={{
              padding: '8px 16px',
              marginTop: '16px',
              cursor: 'pointer',
              backgroundColor: '#f0f0f0',
              border: '1px solid #ccc',
              borderRadius: '4px',
              color: '#333'
            }}
          >
            Fermer
          </button>
        </div>
      )}
      {isCreatingRelation && (
        <div style={{
          position: 'fixed',
          top: '10px',
          left: '50%',
          transform: 'translateX(-50%)',
          backgroundColor: 'rgba(0,0,0,0.8)',
          color: 'white',
          padding: '10px',
          borderRadius: '5px',
          zIndex: 1000
        }}>
          Sélectionnez un nœud cible pour créer la relation
        </div>
      )}
    </div>
  );
};

export default GraphVisualization;
