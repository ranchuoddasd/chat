import React, { useState } from 'react';
import { Search, Shield, Clock, Target, Database, Router, Cloud, AlertTriangle } from 'lucide-react';

const SecurityQueryAssistant = () => {
  const [userInput, setUserInput] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  // IP address regex pattern
  const ipPattern = /(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)/g;
  
  // Time range patterns
  const timePatterns = {
    '1 hour': { splunk: '-1h', api: 'last_1_hour', router: '60' },
    '2 hours': { splunk: '-2h', api: 'last_2_hours', router: '120' },
    '4 hours': { splunk: '-4h', api: 'last_4_hours', router: '240' },
    '8 hours': { splunk: '-8h', api: 'last_8_hours', router: '480' },
    '12 hours': { splunk: '-12h', api: 'last_12_hours', router: '720' },
    '24 hours': { splunk: '-24h', api: 'last_24_hours', router: '1440' },
    '1 day': { splunk: '-1d', api: 'last_1_day', router: '1440' },
    '7 days': { splunk: '-7d', api: 'last_7_days', router: '10080' },
    '30 days': { splunk: '-30d', api: 'last_30_days', router: '43200' }
  };

  const parseUserInput = (input) => {
    const normalizedInput = input.toLowerCase();
    
    // Extract IP addresses
    const ips = input.match(ipPattern) || [];
    
    // Determine source and destination based on keywords
    let sourceIP = null;
    let destIP = null;
    
    if (ips.length >= 2) {
      // Look for "from" and "to" keywords
      const fromIndex = normalizedInput.indexOf('from');
      const toIndex = normalizedInput.indexOf('to');
      
      if (fromIndex !== -1 && toIndex !== -1 && fromIndex < toIndex) {
        sourceIP = ips[0];
        destIP = ips[1];
      } else {
        sourceIP = ips[0];
        destIP = ips[1];
      }
    } else if (ips.length === 1) {
      // Single IP - determine if it's source or destination
      if (normalizedInput.includes('from') || normalizedInput.includes('source')) {
        sourceIP = ips[0];
      } else if (normalizedInput.includes('to') || normalizedInput.includes('destination')) {
        destIP = ips[0];
      } else {
        sourceIP = ips[0]; // Default to source
      }
    }
    
    // Extract time range
    let timeRange = 'last 1 hour'; // default
    for (const pattern in timePatterns) {
      if (normalizedInput.includes(pattern)) {
        timeRange = pattern;
        break;
      }
    }
    
    // Extract ports if mentioned
    const portMatch = normalizedInput.match(/port\s+(\d+)/);
    const port = portMatch ? portMatch[1] : null;
    
    // Extract protocols
    const protocols = ['tcp', 'udp', 'icmp', 'http', 'https', 'ftp', 'ssh', 'telnet'];
    const detectedProtocol = protocols.find(proto => normalizedInput.includes(proto));
    
    return {
      sourceIP,
      destIP,
      timeRange,
      port,
      protocol: detectedProtocol
    };
  };

  const generateQueries = (intent) => {
    const timeConfig = timePatterns[intent.timeRange] || timePatterns['1 hour'];
    
    const queries = {};
    
    // Splunk Query
    let splunkQuery = 'index=firewall';
    if (intent.sourceIP) splunkQuery += ` src_ip="${intent.sourceIP}"`;
    if (intent.destIP) splunkQuery += ` dest_ip="${intent.destIP}"`;
    if (intent.port) splunkQuery += ` dest_port="${intent.port}"`;
    if (intent.protocol) splunkQuery += ` protocol="${intent.protocol}"`;
    splunkQuery += ` earliest=${timeConfig.splunk}`;
    queries.Splunk = splunkQuery;
    
    // Firewall API Query
    const firewallQuery = {
      action: 'search',
      time_range: timeConfig.api
    };
    if (intent.sourceIP) firewallQuery.src_ip = intent.sourceIP;
    if (intent.destIP) firewallQuery.dst_ip = intent.destIP;
    if (intent.port) firewallQuery.dst_port = intent.port;
    if (intent.protocol) firewallQuery.protocol = intent.protocol;
    queries['Firewall API'] = firewallQuery;
    
    // Router Logs Query
    let routerQuery = '/logs?';
    const routerParams = [];
    if (intent.sourceIP) routerParams.push(`src=${intent.sourceIP}`);
    if (intent.destIP) routerParams.push(`dst=${intent.destIP}`);
    if (intent.port) routerParams.push(`port=${intent.port}`);
    routerParams.push(`time=${timeConfig.router}`);
    routerQuery += routerParams.join('&');
    queries['Router Logs'] = routerQuery;
    
    // CloudWatch Query
    let cloudWatchQuery = 'filter @message like';
    const cloudWatchFilters = [];
    if (intent.sourceIP) cloudWatchFilters.push(`/${intent.sourceIP}/`);
    if (intent.destIP) cloudWatchFilters.push(`/${intent.destIP}/`);
    if (intent.port) cloudWatchFilters.push(`/${intent.port}/`);
    cloudWatchQuery += ' ' + cloudWatchFilters.join(' and ');
    queries.CloudWatch = cloudWatchQuery;
    
    return queries;
  };

  const handleQuery = () => {
    if (!userInput.trim()) return;
    
    setLoading(true);
    
    // Simulate processing time
    setTimeout(() => {
      const intent = parseUserInput(userInput);
      const queries = generateQueries(intent);
      
      setResults({
        intent,
        queries
      });
      setLoading(false);
    }, 500);
  };

  const sampleQueries = [
    "Check traffic from 10.0.0.5 to 172.16.8.9 in the last 1 hour",
    "Show connections to 192.168.1.100 on port 80 in the last 4 hours",
    "Find all HTTP traffic from 10.1.1.50 in the last 24 hours",
    "Investigate SSH connections to 172.16.0.10 in the last 2 hours",
    "Check ICMP traffic from 192.168.0.0/24 in the last 30 minutes"
  ];

  return (
    <div className="max-w-6xl mx-auto p-6 bg-gray-50 min-h-screen">
      {/* Header */}
      <div className="text-center mb-8">
        <div className="flex items-center justify-center mb-4">
          <Shield className="h-8 w-8 text-blue-600 mr-2" />
          <h1 className="text-3xl font-bold text-gray-800">Security Query Assistant</h1>
        </div>
        <p className="text-gray-600">Intelligent multi-tool security query generator</p>
      </div>

      {/* Query Input */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <div className="flex items-center mb-4">
          <Search className="h-5 w-5 text-gray-500 mr-2" />
          <label className="text-lg font-medium text-gray-700">
            Describe your security investigation:
          </label>
        </div>
        
        <textarea
          value={userInput}
          onChange={(e) => setUserInput(e.target.value)}
          placeholder="e.g., Check traffic from 10.0.0.5 to 172.16.8.9 in the last 1 hour"
          className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-none"
          rows="3"
        />
        
        <div className="flex justify-between items-center mt-4">
          <button
            onClick={handleQuery}
            disabled={loading || !userInput.trim()}
            className="bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center"
          >
            {loading ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                Generating...
              </>
            ) : (
              <>
                <Search className="h-4 w-4 mr-2" />
                Generate Queries
              </>
            )}
          </button>
          
          <button
            onClick={() => setUserInput('')}
            className="text-gray-500 hover:text-gray-700"
          >
            Clear
          </button>
        </div>
      </div>

      {/* Sample Queries */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <h3 className="text-lg font-medium text-gray-700 mb-3">Sample Queries:</h3>
        <div className="space-y-2">
          {sampleQueries.map((query, index) => (
            <button
              key={index}
              onClick={() => setUserInput(query)}
              className="text-left w-full p-2 text-sm text-blue-600 hover:bg-blue-50 rounded border border-blue-200 hover:border-blue-300"
            >
              {query}
            </button>
          ))}
        </div>
      </div>

      {/* Results */}
      {results && (
        <div className="space-y-6">
          {/* Intent Summary */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center mb-4">
              <Target className="h-5 w-5 text-green-600 mr-2" />
              <h3 className="text-lg font-medium text-gray-700">Extracted Intent</h3>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <div className="p-3 bg-gray-50 rounded">
                <div className="text-sm text-gray-500">Source IP</div>
                <div className="font-mono text-sm">
                  {results.intent.sourceIP || 'Not specified'}
                </div>
              </div>
              <div className="p-3 bg-gray-50 rounded">
                <div className="text-sm text-gray-500">Destination IP</div>
                <div className="font-mono text-sm">
                  {results.intent.destIP || 'Not specified'}
                </div>
              </div>
              <div className="p-3 bg-gray-50 rounded">
                <div className="text-sm text-gray-500">Time Range</div>
                <div className="font-mono text-sm">{results.intent.timeRange}</div>
              </div>
              <div className="p-3 bg-gray-50 rounded">
                <div className="text-sm text-gray-500">Port/Protocol</div>
                <div className="font-mono text-sm">
                  {results.intent.port || results.intent.protocol || 'Not specified'}
                </div>
              </div>
            </div>
          </div>

          {/* Generated Queries */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Splunk Query */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="flex items-center mb-4">
                <Database className="h-5 w-5 text-orange-600 mr-2" />
                <h3 className="text-lg font-medium text-gray-700">Splunk Query</h3>
              </div>
              <div className="bg-gray-900 text-green-400 p-4 rounded font-mono text-sm overflow-x-auto">
                {results.queries.Splunk}
              </div>
            </div>

            {/* Firewall API Query */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="flex items-center mb-4">
                <Shield className="h-5 w-5 text-red-600 mr-2" />
                <h3 className="text-lg font-medium text-gray-700">Firewall API</h3>
              </div>
              <div className="bg-gray-900 text-green-400 p-4 rounded font-mono text-sm overflow-x-auto">
                {JSON.stringify(results.queries['Firewall API'], null, 2)}
              </div>
            </div>

            {/* Router Logs Query */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="flex items-center mb-4">
                <Router className="h-5 w-5 text-blue-600 mr-2" />
                <h3 className="text-lg font-medium text-gray-700">Router Logs</h3>
              </div>
              <div className="bg-gray-900 text-green-400 p-4 rounded font-mono text-sm overflow-x-auto">
                {results.queries['Router Logs']}
              </div>
            </div>

            {/* CloudWatch Query */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="flex items-center mb-4">
                <Cloud className="h-5 w-5 text-purple-600 mr-2" />
                <h3 className="text-lg font-medium text-gray-700">CloudWatch Logs</h3>
              </div>
              <div className="bg-gray-900 text-green-400 p-4 rounded font-mono text-sm overflow-x-auto">
                {results.queries.CloudWatch}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Footer */}
      <div className="mt-8 text-center text-gray-500 text-sm">
        <div className="flex items-center justify-center mb-2">
          <AlertTriangle className="h-4 w-4 mr-1" />
          <span>Always verify queries in your environment before execution</span>
        </div>
      </div>
    </div>
  );
};

export default SecurityQueryAssistant;
