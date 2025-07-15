import React, { useState } from 'react';
import { Search, Shield, Clock, Target, Database, Router, Cloud, AlertTriangle, Settings } from 'lucide-react';

const SecurityQueryAssistant = () => {
  const [userInput, setUserInput] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showConfig, setShowConfig] = useState(false);
  
  // Configuration state for server addresses and credentials
  const [config, setConfig] = useState({
    splunk: {
      host: 'https://splunk.example.com',
      port: '8089',
      username: '',
      password: '',
      token: ''
    },
    firewall: {
      host: 'https://firewall-api.example.com',
      port: '443',
      apiKey: '',
      version: 'v1'
    },
    router: {
      host: 'https://router-logs.example.com',
      port: '443',
      apiKey: '',
      endpoint: '/api/v1/logs'
    },
    cloudwatch: {
      region: 'us-west-2',
      logGroup: '/aws/vpc/flowlogs',
      accessKey: '',
      secretKey: ''
    }
  });

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
    
    // Splunk Query with full connection details
    let splunkQuery = 'index=firewall';
    if (intent.sourceIP) splunkQuery += ` src_ip="${intent.sourceIP}"`;
    if (intent.destIP) splunkQuery += ` dest_ip="${intent.destIP}"`;
    if (intent.port) splunkQuery += ` dest_port="${intent.port}"`;
    if (intent.protocol) splunkQuery += ` protocol="${intent.protocol}"`;
    splunkQuery += ` earliest=${timeConfig.splunk}`;
    
    queries.Splunk = {
      connection: {
        host: config.splunk.host,
        port: config.splunk.port,
        username: config.splunk.username,
        token: config.splunk.token || '[Token Required]'
      },
      query: splunkQuery,
      restApi: `${config.splunk.host}:${config.splunk.port}/services/search/jobs`,
      curlExample: `curl -k -u ${config.splunk.username}:${config.splunk.token} \\
  -d "search=${encodeURIComponent(splunkQuery)}" \\
  ${config.splunk.host}:${config.splunk.port}/services/search/jobs`
    };
    
    // Firewall API Query with full endpoint
    const firewallQuery = {
      action: 'search',
      time_range: timeConfig.api
    };
    if (intent.sourceIP) firewallQuery.src_ip = intent.sourceIP;
    if (intent.destIP) firewallQuery.dst_ip = intent.destIP;
    if (intent.port) firewallQuery.dst_port = intent.port;
    if (intent.protocol) firewallQuery.protocol = intent.protocol;
    
    queries['Firewall API'] = {
      connection: {
        host: config.firewall.host,
        port: config.firewall.port,
        apiKey: config.firewall.apiKey || '[API Key Required]',
        version: config.firewall.version
      },
      endpoint: `${config.firewall.host}:${config.firewall.port}/api/${config.firewall.version}/search`,
      payload: firewallQuery,
      curlExample: `curl -X POST \\
  -H "Authorization: Bearer ${config.firewall.apiKey}" \\
  -H "Content-Type: application/json" \\
  -d '${JSON.stringify(firewallQuery, null, 2)}' \\
  ${config.firewall.host}:${config.firewall.port}/api/${config.firewall.version}/search`
    };
    
    // Router Logs Query with full URL
    const routerParams = [];
    if (intent.sourceIP) routerParams.push(`src=${intent.sourceIP}`);
    if (intent.destIP) routerParams.push(`dst=${intent.destIP}`);
    if (intent.port) routerParams.push(`port=${intent.port}`);
    routerParams.push(`time=${timeConfig.router}`);
    const routerQuery = `${config.router.endpoint}?${routerParams.join('&')}`;
    
    queries['Router Logs'] = {
      connection: {
        host: config.router.host,
        port: config.router.port,
        apiKey: config.router.apiKey || '[API Key Required]'
      },
      fullUrl: `${config.router.host}:${config.router.port}${routerQuery}`,
      curlExample: `curl -X GET \\
  -H "Authorization: Bearer ${config.router.apiKey}" \\
  "${config.router.host}:${config.router.port}${routerQuery}"`
    };
    
    // CloudWatch Query with AWS details
    const cloudWatchFilters = [];
    if (intent.sourceIP) cloudWatchFilters.push(`/${intent.sourceIP}/`);
    if (intent.destIP) cloudWatchFilters.push(`/${intent.destIP}/`);
    if (intent.port) cloudWatchFilters.push(`/${intent.port}/`);
    const cloudWatchQuery = 'filter @message like ' + cloudWatchFilters.join(' and ');
    
    queries.CloudWatch = {
      connection: {
        region: config.cloudwatch.region,
        logGroup: config.cloudwatch.logGroup,
        accessKey: config.cloudwatch.accessKey || '[Access Key Required]',
        secretKey: config.cloudwatch.secretKey || '[Secret Key Required]'
      },
      query: cloudWatchQuery,
      awsCliExample: `aws logs filter-log-events \\
  --log-group-name ${config.cloudwatch.logGroup} \\
  --filter-pattern "${cloudWatchQuery}" \\
  --region ${config.cloudwatch.region}`
    };
    
    return queries;
  };

  const updateConfig = (tool, field, value) => {
    setConfig(prev => ({
      ...prev,
      [tool]: {
        ...prev[tool],
        [field]: value
      }
    }));
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

      {/* Configuration Panel */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center">
            <Settings className="h-5 w-5 text-gray-600 mr-2" />
            <h3 className="text-lg font-medium text-gray-700">System Configuration</h3>
          </div>
          <button
            onClick={() => setShowConfig(!showConfig)}
            className="text-blue-600 hover:text-blue-800"
          >
            {showConfig ? 'Hide Config' : 'Show Config'}
          </button>
        </div>
        
        {showConfig && (
          <div className="space-y-6">
            {/* Splunk Configuration */}
            <div className="border-l-4 border-orange-500 pl-4">
              <h4 className="font-medium text-gray-700 mb-3">Splunk Configuration</h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-600 mb-1">Host</label>
                  <input
                    type="text"
                    value={config.splunk.host}
                    onChange={(e) => updateConfig('splunk', 'host', e.target.value)}
                    placeholder="https://splunk.company.com"
                    className="w-full p-2 border border-gray-300 rounded text-sm"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-600 mb-1">Port</label>
                  <input
                    type="text"
                    value={config.splunk.port}
                    onChange={(e) => updateConfig('splunk', 'port', e.target.value)}
                    placeholder="8089"
                    className="w-full p-2 border border-gray-300 rounded text-sm"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-600 mb-1">Username</label>
                  <input
                    type="text"
                    value={config.splunk.username}
                    onChange={(e) => updateConfig('splunk', 'username', e.target.value)}
                    placeholder="admin"
                    className="w-full p-2 border border-gray-300 rounded text-sm"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-600 mb-1">Auth Token</label>
                  <input
                    type="password"
                    value={config.splunk.token}
                    onChange={(e) => updateConfig('splunk', 'token', e.target.value)}
                    placeholder="Authentication token"
                    className="w-full p-2 border border-gray-300 rounded text-sm"
                  />
                </div>
              </div>
            </div>

            {/* Firewall API Configuration */}
            <div className="border-l-4 border-red-500 pl-4">
              <h4 className="font-medium text-gray-700 mb-3">Firewall API Configuration</h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-600 mb-1">Host</label>
                  <input
                    type="text"
                    value={config.firewall.host}
                    onChange={(e) => updateConfig('firewall', 'host', e.target.value)}
                    placeholder="https://firewall-api.company.com"
                    className="w-full p-2 border border-gray-300 rounded text-sm"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-600 mb-1">Port</label>
                  <input
                    type="text"
                    value={config.firewall.port}
                    onChange={(e) => updateConfig('firewall', 'port', e.target.value)}
                    placeholder="443"
                    className="w-full p-2 border border-gray-300 rounded text-sm"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-600 mb-1">API Key</label>
                  <input
                    type="password"
                    value={config.firewall.apiKey}
                    onChange={(e) => updateConfig('firewall', 'apiKey', e.target.value)}
                    placeholder="API Key"
                    className="w-full p-2 border border-gray-300 rounded text-sm"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-600 mb-1">API Version</label>
                  <input
                    type="text"
                    value={config.firewall.version}
                    onChange={(e) => updateConfig('firewall', 'version', e.target.value)}
                    placeholder="v1"
                    className="w-full p-2 border border-gray-300 rounded text-sm"
                  />
                </div>
              </div>
            </div>

            {/* Router Logs Configuration */}
            <div className="border-l-4 border-blue-500 pl-4">
              <h4 className="font-medium text-gray-700 mb-3">Router Logs Configuration</h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-600 mb-1">Host</label>
                  <input
                    type="text"
                    value={config.router.host}
                    onChange={(e) => updateConfig('router', 'host', e.target.value)}
                    placeholder="https://router-logs.company.com"
                    className="w-full p-2 border border-gray-300 rounded text-sm"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-600 mb-1">Port</label>
                  <input
                    type="text"
                    value={config.router.port}
                    onChange={(e) => updateConfig('router', 'port', e.target.value)}
                    placeholder="443"
                    className="w-full p-2 border border-gray-300 rounded text-sm"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-600 mb-1">API Key</label>
                  <input
                    type="password"
                    value={config.router.apiKey}
                    onChange={(e) => updateConfig('router', 'apiKey', e.target.value)}
                    placeholder="API Key"
                    className="w-full p-2 border border-gray-300 rounded text-sm"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-600 mb-1">Endpoint</label>
                  <input
                    type="text"
                    value={config.router.endpoint}
                    onChange={(e) => updateConfig('router', 'endpoint', e.target.value)}
                    placeholder="/api/v1/logs"
                    className="w-full p-2 border border-gray-300 rounded text-sm"
                  />
                </div>
              </div>
            </div>

            {/* CloudWatch Configuration */}
            <div className="border-l-4 border-purple-500 pl-4">
              <h4 className="font-medium text-gray-700 mb-3">AWS CloudWatch Configuration</h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-600 mb-1">Region</label>
                  <input
                    type="text"
                    value={config.cloudwatch.region}
                    onChange={(e) => updateConfig('cloudwatch', 'region', e.target.value)}
                    placeholder="us-west-2"
                    className="w-full p-2 border border-gray-300 rounded text-sm"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-600 mb-1">Log Group</label>
                  <input
                    type="text"
                    value={config.cloudwatch.logGroup}
                    onChange={(e) => updateConfig('cloudwatch', 'logGroup', e.target.value)}
                    placeholder="/aws/vpc/flowlogs"
                    className="w-full p-2 border border-gray-300 rounded text-sm"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-600 mb-1">Access Key</label>
                  <input
                    type="password"
                    value={config.cloudwatch.accessKey}
                    onChange={(e) => updateConfig('cloudwatch', 'accessKey', e.target.value)}
                    placeholder="AWS Access Key"
                    className="w-full p-2 border border-gray-300 rounded text-sm"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-600 mb-1">Secret Key</label>
                  <input
                    type="password"
                    value={config.cloudwatch.secretKey}
                    onChange={(e) => updateConfig('cloudwatch', 'secretKey', e.target.value)}
                    placeholder="AWS Secret Key"
                    className="w-full p-2 border border-gray-300 rounded text-sm"
                  />
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
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
          <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
            {/* Splunk Query */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="flex items-center mb-4">
                <Database className="h-5 w-5 text-orange-600 mr-2" />
                <h3 className="text-lg font-medium text-gray-700">Splunk Query</h3>
              </div>
              
              <div className="space-y-4">
                <div>
                  <div className="text-sm text-gray-600 mb-2">Connection Info:</div>
                  <div className="text-xs font-mono bg-gray-100 p-2 rounded">
                    {results.queries.Splunk.connection.host}:{results.queries.Splunk.connection.port}
                  </div>
                </div>
                
                <div>
                  <div className="text-sm text-gray-600 mb-2">SPL Query:</div>
                  <div className="bg-gray-900 text-green-400 p-4 rounded font-mono text-sm overflow-x-auto">
                    {results.queries.Splunk.query}
                  </div>
                </div>
                
                <div>
                  <div className="text-sm text-gray-600 mb-2">cURL Example:</div>
                  <div className="bg-gray-900 text-blue-400 p-4 rounded font-mono text-xs overflow-x-auto">
                    {results.queries.Splunk.curlExample}
                  </div>
                </div>
              </div>
            </div>

            {/* Firewall API Query */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="flex items-center mb-4">
                <Shield className="h-5 w-5 text-red-600 mr-2" />
                <h3 className="text-lg font-medium text-gray-700">Firewall API</h3>
              </div>
              
              <div className="space-y-4">
                <div>
                  <div className="text-sm text-gray-600 mb-2">Endpoint:</div>
                  <div className="text-xs font-mono bg-gray-100 p-2 rounded">
                    {results.queries['Firewall API'].endpoint}
                  </div>
                </div>
                
                <div>
                  <div className="text-sm text-gray-600 mb-2">JSON Payload:</div>
                  <div className="bg-gray-900 text-green-400 p-4 rounded font-mono text-sm overflow-x-auto">
                    {JSON.stringify(results.queries['Firewall API'].payload, null, 2)}
                  </div>
                </div>
                
                <div>
                  <div className="text-sm text-gray-600 mb-2">cURL Example:</div>
                  <div className="bg-gray-900 text-blue-400 p-4 rounded font-mono text-xs overflow-x-auto">
                    {results.queries['Firewall API'].curlExample}
                  </div>
                </div>
              </div>
            </div>

            {/* Router Logs Query */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="flex items-center mb-4">
                <Router className="h-5 w-5 text-blue-600 mr-2" />
                <h3 className="text-lg font-medium text-gray-700">Router Logs</h3>
              </div>
              
              <div className="space-y-4">
                <div>
                  <div className="text-sm text-gray-600 mb-2">Full URL:</div>
                  <div className="bg-gray-900 text-green-400 p-4 rounded font-mono text-sm overflow-x-auto">
                    {results.queries['Router Logs'].fullUrl}
                  </div>
                </div>
                
                <div>
                  <div className="text-sm text-gray-600 mb-2">cURL Example:</div>
                  <div className="bg-gray-900 text-blue-400 p-4 rounded font-mono text-xs overflow-x-auto">
                    {results.queries['Router Logs'].curlExample}
                  </div>
                </div>
              </div>
            </div>

            {/* CloudWatch Query */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="flex items-center mb-4">
                <Cloud className="h-5 w-5 text-purple-600 mr-2" />
                <h3 className="text-lg font-medium text-gray-700">CloudWatch Logs</h3>
              </div>
              
              <div className="space-y-4">
                <div>
                  <div className="text-sm text-gray-600 mb-2">Log Group:</div>
                  <div className="text-xs font-mono bg-gray-100 p-2 rounded">
                    {results.queries.CloudWatch.connection.logGroup} ({results.queries.CloudWatch.connection.region})
                  </div>
                </div>
                
                <div>
                  <div className="text-sm text-gray-600 mb-2">Filter Pattern:</div>
                  <div className="bg-gray-900 text-green-400 p-4 rounded font-mono text-sm overflow-x-auto">
                    {results.queries.CloudWatch.query}
                  </div>
                </div>
                
                <div>
                  <div className="text-sm text-gray-600 mb-2">AWS CLI Example:</div>
                  <div className="bg-gray-900 text-blue-400 p-4 rounded font-mono text-xs overflow-x-auto">
                    {results.queries.CloudWatch.awsCliExample}
                  </div>
                </div>
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
