import React, { useEffect, useState } from 'react';
import Cytoscape from 'cytoscape';
import CytoscapeComponent from 'react-cytoscapejs';
import './GraphVisualization.css'; // Assurez-vous de créer ce fichier CSS

const GraphVisualization = () => {
  const [graphData, setGraphData] = useState({ nodes: [], edges: [] });

  useEffect(() => {
    // Remplacez cette URL par l'endpoint de votre API
    fetch('/graph')
      .then((response) => response.json())
      .then((data) => {
        // Définir displayLabel comme la première propriété utile
        data.nodes.forEach((nodeObj) => {
          const nodeData = nodeObj.data;
          let display = null;
          for (let key in nodeData) {
            if (!['id', 'label', 'background-color'].includes(key)) {
              display = nodeData['nom'];
              break;
            }
          }
          nodeData.displayLabel = display || nodeData.label || nodeData.id;
        });

        setGraphData(data);
      });
  }, []);

  const layout = { name: 'cose' };

  return (
    <div className="graph-container">
      <CytoscapeComponent
        elements={CytoscapeComponent.normalizeElements({
          nodes: graphData.nodes,
          edges: graphData.edges,
        })}
        style={{ width: '100vw', height: '90vh' }}
        stylesheet={[
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
        ]}
        layout={layout}
      />
    </div>
  );
};

export default GraphVisualization;
