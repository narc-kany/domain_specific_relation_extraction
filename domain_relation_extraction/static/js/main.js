document.addEventListener('DOMContentLoaded', function() {
  const extractionForm = document.getElementById('extractionForm');
  const textInput = document.getElementById('textInput');
  const domainSelect = document.getElementById('domainSelect');
  const extractButton = document.getElementById('extractButton');
  const loadingIndicator = document.getElementById('loadingIndicator');
  const entitiesTable = document.getElementById('entitiesTable');
  const relationsTable = document.getElementById('relationsTable');
  const graphVisualization = document.getElementById('graphVisualization');
  
  // Handle form submission
  extractionForm.addEventListener('submit', async function(event) {
      event.preventDefault();
      
      // Show loading indicator
      loadingIndicator.classList.remove('d-none');
      
      // Clear previous results
      entitiesTable.innerHTML = '';
      relationsTable.innerHTML = '';
      
      // Get form data
      const text = textInput.value;
      const domain = domainSelect.value;
      
      // Create form data for API request
      const formData = new FormData();
      formData.append('text', text);
      formData.append('domain', domain);
      
      try {
          // Send request to backend
          const response = await fetch('/extract', {
              method: 'POST',
              body: formData
          });
          
          // Parse JSON response
          const data = await response.json();
          
          if (data.error) {
              alert(data.error);
              return;
          }
          
          // Display entities
          displayEntities(data.entities);
          
          // Display relations
          displayRelations(data.relations);
          
          // Create graph visualization
          createGraphVisualization(data.entities, data.relations);
          
      } catch (error) {
          console.error('Error:', error);
          alert('An error occurred while processing your request.');
      } finally {
          // Hide loading indicator
          loadingIndicator.classList.add('d-none');
      }
  });
  
  // Function to display entities in the table
  function displayEntities(entities) {
      entities.forEach(entity => {
          const row = document.createElement('tr');
          
          const nameCell = document.createElement('td');
          nameCell.textContent = entity.text;
          
          const typeCell = document.createElement('td');
          typeCell.textContent = entity.type;
          
          row.appendChild(nameCell);
          row.appendChild(typeCell);
          
          entitiesTable.appendChild(row);
      });
  }
  
  // Function to display relations in the table
  function displayRelations(relations) {
      relations.forEach(relation => {
          const row = document.createElement('tr');
          
          const sourceCell = document.createElement('td');
          sourceCell.textContent = relation.source;
          
          const relTypeCell = document.createElement('td');
          relTypeCell.textContent = relation.type;
          
          const targetCell = document.createElement('td');
          targetCell.textContent = relation.target;
          
          row.appendChild(sourceCell);
          row.appendChild(relTypeCell);
          row.appendChild(targetCell);
          
          relationsTable.appendChild(row);
      });
  }
  
  // Function to create graph visualization
  function createGraphVisualization(entities, relations) {
      // Create nodes for entities
      const nodes = entities.map((entity, index) => ({
          id: index,
          label: entity.text,
          title: entity.type,
          group: entity.type // Entities of the same type will have the same color
      }));
      
      // Create edges for relations
      const edges = relations.map((relation, index) => {
          // Find source and target node ids
          const sourceId = nodes.findIndex(node => node.label === relation.source);
          const targetId = nodes.findIndex(node => node.label === relation.target);
          
          return {
              id: `e${index}`,
              from: sourceId,
              to: targetId,
              label: relation.type,
              arrows: 'to'
          };
      });
      
      // Create data object
      const data = {
          nodes: new vis.DataSet(nodes),
          edges: new vis.DataSet(edges)
      };
      
      // Configuration for the network
      const options = {
          nodes: {
              shape: 'box',
              font: {
                  size: 14
              }
          },
          edges: {
              font: {
                  size: 12,
                  align: 'middle'
              },
              color: {
                  color: '#848484',
                  highlight: '#1B78E2'
              }
          },
          physics: {
              enabled: true,
              solver: 'forceAtlas2Based'
          }
      };
      
      // Initialize network
      new vis.Network(graphVisualization, data, options);
  }
});