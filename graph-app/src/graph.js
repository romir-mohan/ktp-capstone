import React, { useEffect, useState, useRef } from 'react';
import { Network } from 'vis-network/standalone/umd/vis-network.min.js';

const Graph = () => {
  const graphContainer = useRef(null);
  const [graphData, setGraphData] = useState({ nodes: [], edges: [] });

  useEffect(() => {
    const fetchData = async () => {
      // Fetch the graph data from the Flask server
      const response = await fetch('http://localhost:5000/graph');
      const data = await response.json();
      setGraphData(data);
    };

    fetchData();
  }, []);

  useEffect(() => {
    if (graphData.nodes.length === 0 || graphData.edges.length === 0) return;

    const { nodes, edges } = graphData;

    const options = {
      nodes: { shape: 'dot', size: 10 },
      edges: { width: 2, color: { color: 'gray' } },
      physics: { enabled: true }
    };

    // Create the network graph using the vis-network library
    new Network(graphContainer.current, { nodes, edges }, options);
  }, [graphData]);

  return <div ref={graphContainer} style={{ height: '500px' }} />;
};

export default Graph;
