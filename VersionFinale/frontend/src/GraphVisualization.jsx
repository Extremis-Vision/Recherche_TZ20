import React, { useEffect, useRef } from 'react';
import cytoscape from 'cytoscape';
import coseBilkent from 'cytoscape-cose-bilkent';
import './GraphVisualization.css';

cytoscape.use(coseBilkent);

const GraphVisualization = ({ width = '100%', height = 600 }) => {
  const cyRef = useRef(null);
  const cyInstance = useRef(null);

  useEffect(() => {
    let cy;

    fetch('http://localhost:8888/nodebdd/GetAllNode/')
      .then((response) => response.json())
      .then((data) => {
        const nodes = (data.nodes || []).map((node) => {
          const d = node.data || {};
          const displayLabel = d.nom || d.name || d.id;
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

        const edges = (data.edges || []).map((edge) => {
          const d = edge.data || {};
          const label = d.label || d.type || '';
          return {
            ...edge,
            data: {
              ...d,
              label,
            },
          };
        });

        cy = cytoscape({
          container: cyRef.current,
          elements: { nodes, edges },
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
                width: 60,
                height: 60,
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

        cyInstance.current = cy;

        // Optionnel: fit on resize
        const handleResize = () => cy.resize() && cy.fit();
        window.addEventListener('resize', handleResize);

        return () => {
          window.removeEventListener('resize', handleResize);
          if (cy) cy.destroy();
        };
      })
      .catch((error) => {
        console.error('There was a problem with the fetch operation:', error);
      });

    return () => {
      if (cyInstance.current) {
        cyInstance.current.destroy();
        cyInstance.current = null;
      }
    };
  }, []);

  return (
    <div className="graph-container">
      <div
        id="cy"
        ref={cyRef}
        style={{
          width: typeof width === 'number' ? `${width}px` : width,
          height: typeof height === 'number' ? `${height}px` : height,
          minHeight: 120,
        }}
      ></div>
    </div>
  );
};

export default GraphVisualization;
