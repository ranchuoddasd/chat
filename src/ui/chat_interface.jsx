// Install dependencies
npm install next react react-dom tailwindcss openai axios

// Basic chatbot component structure
const ChatInterface = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    // Process IP search query
    const response = await searchIPAddress(input);
    setMessages([...messages, { user: input, bot: response }]);
  };
  
  return (
    <div className="chat-container">
      <div className="messages">
        {messages.map((msg, idx) => (
          <div key={idx} className="message-pair">
            <div className="user-message">{msg.user}</div>
            <div className="bot-message">{msg.bot}</div>
          </div>
        ))}
      </div>
      <form onSubmit={handleSubmit}>
        <input 
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Enter IP address to search..."
        />
        <button type="submit">Search</button>
      </form>
    </div>
  );
};


---------------

// React component for IP search results dashboard
const IPSearchDashboard = ({ searchResults }) => {
  return (
    <div className="dashboard-container">
      <div className="search-summary">
        <h2>IP Address: {searchResults.ip}</h2>
        <div className="source-summary">
          {Object.keys(searchResults.sources).map(source => (
            <div key={source} className="source-card">
              <h3>{source.toUpperCase()}</h3>
              <p>Found {searchResults.sources[source].count} entries</p>
            </div>
          ))}
        </div>
      </div>
      
      <div className="visualization-grid">
        <NetworkTopologyView data={searchResults.topology} />
        <GeographicMap data={searchResults.location} />
        <TimelineChart data={searchResults.timeline} />
        <SecurityAnalysis data={searchResults.security} />
      </div>
    </div>
  );
};

-----------
import { Network } from 'vis-network';

const NetworkTopologyView = ({ data }) => {
  useEffect(() => {
    const nodes = new DataSet(data.nodes);
    const edges = new DataSet(data.edges);
    
    const container = document.getElementById('network-topology');
    const networkData = { nodes, edges };
    
    const options = {
      nodes: {
        shape: 'circle',
        size: 30,
        font: { size: 14 },
        borderWidth: 2
      },
      edges: {
        width: 2,
        color: { color: '#848484' }
      },
      physics: {
        stabilization: { iterations: 100 }
      }
    };
    
    new Network(container, networkData, options);
  }, [data]);
  
  return <div id="network-topology" style={{ height: '400px' }} />;
};

-------------
const GeographicMap = ({ data }) => {
  return (
    <div className="map-container">
      <h3>IP Address Locations</h3>
      <div id="ip-map" style={{ height: '300px' }}>
        {/* Use libraries like Leaflet or Google Maps */}
        <IPLocationMap 
          coordinates={data.coordinates}
          markers={data.locations}
        />
      </div>
    </div>
  );
};
