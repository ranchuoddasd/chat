import streamlit as st
import requests

def search_ip_address(ip):
    # Orchestrate multiple API calls
    results = {}
    
    # Search Splunk
    results['splunk'] = search_splunk_api(ip)
    
    # Search firewall logs
    results['firewall'] = search_firewall_logs(ip)
    
    # Search network inventory
    results['inventory'] = search_network_inventory(ip)
    
    return results

st.title("IP Address Search Assistant")
user_input = st.text_input("Enter IP address:")

if user_input:
    with st.spinner("Searching across network tools..."):
        results = search_ip_address(user_input)
        st.json(results)
import asyncio
import aiohttp
from typing import Dict, List

class NetworkAPIOrchestrator:
    def __init__(self):
        self.apis = {
            'splunk': SplunkAPIClient(),
            'firewall': FirewallAPIClient(),
            'inventory': InventoryAPIClient(),
            'hpna': HPNAAPIClient()
        }
    
    async def search_ip_address(self, ip_address: str) -> Dict:
        """Orchestrate searches across multiple network APIs"""
        tasks = []
        
        # Create concurrent API calls
        for api_name, client in self.apis.items():
            task = asyncio.create_task(
                self.safe_api_call(api_name, client, ip_address)
            )
            tasks.append(task)
        
        # Wait for all results
        results = await asyncio.gather(*tasks)
        
        # Aggregate and format results
        return self.format_results(results)
    
    async def safe_api_call(self, api_name: str, client, ip_address: str):
        """Make API calls with error handling"""
        try:
            return await client.search_ip(ip_address)
        except Exception as e:
            return {'error': str(e), 'source': api_name}

class SplunkAPIClient:
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.token = token
    
    async def search_ip(self, ip_address: str):
        """Search for IP address in Splunk logs"""
        # Use TERM() for efficient IP searches
        search_query = f'index=* TERM({ip_address}) | head 1000'
        
        # Alternative: Use CIDR matching for IP ranges
        # search_query = f'index=* | where cidrmatch("192.168.0.0/24", src_ip)'
        
        return await self.execute_search(search_query)
    
    async def execute_search(self, query):
        """Execute Splunk search via REST API"""
        headers = {'Authorization': f'Splunk {self.token}'}
        
        # Create search job
        job_data = {'search': query, 'output_mode': 'json'}
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f'{self.base_url}/services/search/jobs',
                headers=headers,
                data=job_data
            ) as response:
                job_info = await response.json()
                return await self.get_search_results(job_info['sid'])
class FirewallAPIClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.cognix.au/v1/firewall"
    
    async def search_ip(self, ip_address: str):
        """Search firewall logs for IP address"""
        params = {
            'source_ip': ip_address,
            'date_range': '2024-01-01to2024-12-31',
            'limit': 1000
        }
        
        headers = {'Authorization': f'Bearer {self.api_key}'}
        
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f'{self.base_url}/logs',
                headers=headers,
                params=params
            ) as response:
                return await response.json()

class InventoryAPIClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://auvikapi.us1.my.auvik.com/v1"
    
    async def search_ip(self, ip_address: str):
        """Search network inventory for IP address"""
        headers = {'Authorization': f'Bearer {self.api_key}'}
        
        # Search for devices with specific IP
        params = {'filter[ipAddress]': ip_address}
        
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f'{self.base_url}/inventory/device/info',
                headers=headers,
                params=params
            ) as response:
                return await response.json()

from hpnapy import NAInterface

class HPNAAPIClient:
    def __init__(self, server_url, username, password):
        self.hpna = NAInterface(server_url)
        self.hpna.login(username, password)
    
    async def search_ip(self, ip_address: str):
        """Search HPNA for devices with specific IP"""
        try:
            # Search for devices by IP address
            devices = self.hpna.list_device(ip=ip_address)
            return {'devices': devices, 'source': 'hpna'}
        except Exception as e:
            return {'error': str(e), 'source': 'hpna'}

class ResultsAggregator:
    def __init__(self):
        self.formatters = {
            'splunk': self.format_splunk_results,
            'firewall': self.format_firewall_results,
            'inventory': self.format_inventory_results,
            'hpna': self.format_hpna_results
        }
    
    def aggregate_results(self, raw_results: Dict) -> Dict:
        """Aggregate and format results from multiple sources"""
        aggregated = {
            'ip_address': raw_results.get('ip_address'),
            'sources': {},
            'timeline': [],
            'locations': [],
            'security_events': [],
            'network_topology': {
                'nodes': [],
                'edges': []
            }
        }
        
        for source, data in raw_results.items():
            if source in self.formatters:
                formatted = self.formatters[source](data)
                aggregated['sources'][source] = formatted
                
                # Merge timeline data
                if 'timeline' in formatted:
                    aggregated['timeline'].extend(formatted['timeline'])
                
                # Merge location data
                if 'locations' in formatted:
                    aggregated['locations'].extend(formatted['locations'])
        
        return aggregated


# Main application file
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="IP Address Search System")

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize orchestrator
orchestrator = NetworkAPIOrchestrator()
aggregator = ResultsAggregator()

@app.post("/search/ip")
async def search_ip_address(request: IPSearchRequest):
    """Main endpoint for IP address search"""
    try:
        # Orchestrate searches across multiple APIs
        raw_results = await orchestrator.search_ip_address(request.ip_address)
        
        # Aggregate and format results
        formatted_results = aggregator.aggregate_results(raw_results)
        
        return {
            "success": True,
            "data": formatted_results,
            "message": f"Found IP {request.ip_address} across {len(formatted_results['sources'])} sources"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
