import React, { useEffect, useRef } from 'react';
import cytoscape from 'cytoscape';
import coseBilkent from 'cytoscape-cose-bilkent';
import './GraphVisualization.css';

cytoscape.use(coseBilkent);

const GraphVisualization = () => {
  const cyRef = useRef(null);

  useEffect(() => {
    fetch('http://localhost:8888/nodebdd/GetAllNode/')
      .then((response) => response.json())
      .then((data) => {
        // Pré-traitement pour garantir que chaque nœud ait un label et une couleur
        const nodes = (data.nodes || []).map((node) => {
          const d = node.data || {};
          // Prend 'nom' ou 'name' comme label
          const displayLabel = d.nom || d.name || d.id;
          // Prend la couleur si présente, sinon couleur par défaut
          const backgroundcolor = d.backgroundcolor || '#267dc5';
          return {
            ...node,
            data: {
              ...d,
              displayLabel,
              backgroundcolor,
            },
          };
        });

        // Pré-traitement des arêtes (edges)
        const edges = (data.edges || []).map((edge) => {
          const d = edge.data || {};
          // Prend le label de la relation si présent
          const label = d.label || d.type || '';
          return {
            ...edge,
            data: {
              ...d,
              label,
            },
          };
        });

        // Initialiser Cytoscape
        const cy = cytoscape({
          container: cyRef.current,
          elements: {
            nodes,
            edges,
          },
          style: [
            {
              selector: 'node',
              style: {
                label: 'data(displayLabel)',
                'background-color': 'data(backgroundcolor)',
                color: '#fff',
                'font-size': '14px',
                'text-valign': 'center',
                'text-halign': 'center',
                'border-width': 2,
                'border-color': '#333',
                'text-outline-width': 2,
                'text-outline-color': '#333',
                'width': 60,
                'height': 60,
              },
            },
            {
              selector: 'node.highlighted',
              style: {
                'border-color': '#ffd700',
                'border-width': 4,
              },
            },
            {
              selector: 'edge',
              style: {
                width: 2,
                'line-color': '#aaa',
                'target-arrow-shape': 'triangle',
                'target-arrow-color': '#aaa',
                'curve-style': 'bezier',
                label: 'data(label)',
                'font-size': '12px',
                color: '#fff',
                'text-background-color': '#444',
                'text-background-opacity': 0.7,
                'text-background-padding': 2,
              },
            },
          ],
          layout: {
            name: 'cose-bilkent',
            animate: true,
            randomize: false,
            fit: true,
          },
        });

        // Optionnel : zoom/fit automatique au resize
        window.addEventListener('resize', () => {
          cy.fit();
        });

        // Nettoyage à la destruction du composant
        return () => {
          cy.destroy();
        };
      })
      .catch((error) => {
        console.error('There was a problem with the fetch operation:', error);
      });
  }, []);

  return (
    <div className="graph-container">
      <div
        id="cy"
        ref={cyRef}
        style={{ width: '100%', height: '600px', border: '1px solid #ccc', borderRadius: 8 }}
      ></div>
    </div>
  );
};

export default GraphVisualization;
