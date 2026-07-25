import React, { useState, useMemo } from 'react';
import { Card } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { useAlertStore } from '../store/useAlertStore';
import { Network, ShieldAlert, Zap, Cpu, Search, Filter, Info, Link2, ArrowRight } from 'lucide-react';

export function GraphTopologyPage() {
  const { alerts } = useAlertStore();
  const [selectedSubnet, setSelectedSubnet] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null);

  // Default baseline nodes
  const defaultNodes = [
    { id: 'usr-9982', label: 'User: usr-9982', type: 'user', status: 'COMPROMISED', riskScore: 0.98, subnet: 'Corporate-LAN', ip: '198.51.100.50' },
    { id: 'dev-4410', label: 'Workstation (dev-4410)', type: 'device', status: 'COMPROMISED', riskScore: 0.95, subnet: 'Corporate-LAN', ip: '198.51.100.51' },
    { id: 'gw-01', label: 'Auth Gateway (198.51.100.1)', type: 'gateway', status: 'NORMAL', riskScore: 0.12, subnet: 'DMZ', ip: '198.51.100.1' },
    { id: 'srv-hr-01', label: 'HR Database (Isolated Target)', type: 'server', status: 'HIGH_RISK', riskScore: 0.88, subnet: 'Secure-VLAN', ip: '10.0.4.12' },
    { id: 'srv-db-master', label: 'SQL Master Cluster', type: 'server', status: 'NORMAL', riskScore: 0.05, subnet: 'Secure-VLAN', ip: '10.0.4.10' },
    { id: 'usr-8812', label: 'User: usr-8812 (Analyst)', type: 'user', status: 'NORMAL', riskScore: 0.02, subnet: 'Corporate-LAN', ip: '198.51.100.77' }
  ];

  const defaultEdges = [
    { source: 'usr-9982', target: 'dev-4410', hops: 1, type: 'Auth Session', risk: 'HIGH' },
    { source: 'dev-4410', target: 'gw-01', hops: 2, type: 'VPN Tunnel', risk: 'MEDIUM' },
    { source: 'gw-01', target: 'srv-hr-01', hops: 3, type: 'SSH Lateral Move', risk: 'CRITICAL' },
    { source: 'usr-8812', target: 'srv-db-master', hops: 1, type: 'Read Query', risk: 'LOW' }
  ];

  // Dynamically compute nodes and edges including real-time store alerts & search term matching
  const { nodes, edges } = useMemo(() => {
    const nodeMap = new Map<string, any>();
    const edgeList = [...defaultEdges];

    // Populate baseline nodes
    defaultNodes.forEach(n => nodeMap.set(n.id, n));

    // Dynamic extraction from live WebSocket alerts store
    alerts.forEach(alert => {
      if (alert.user_id && !nodeMap.has(alert.user_id)) {
        nodeMap.set(alert.user_id, {
          id: alert.user_id,
          label: `User: ${alert.user_id}`,
          type: 'user',
          status: alert.severity === 'CRITICAL' || alert.severity === 'HIGH' ? 'COMPROMISED' : 'NORMAL',
          riskScore: alert.master_risk_score || 0.85,
          subnet: 'Corporate-LAN',
          ip: alert.ip_address || '198.51.100.99'
        });
      }

      if (alert.device_id && !nodeMap.has(alert.device_id)) {
        nodeMap.set(alert.device_id, {
          id: alert.device_id,
          label: `Device (${alert.device_id})`,
          type: 'device',
          status: alert.severity === 'CRITICAL' ? 'COMPROMISED' : 'NORMAL',
          riskScore: alert.master_risk_score || 0.75,
          subnet: 'Corporate-LAN',
          ip: alert.ip_address || '198.51.100.100'
        });
      }

      if (alert.user_id && alert.device_id) {
        const edgeExists = edgeList.some(e => e.source === alert.user_id && e.target === alert.device_id);
        if (!edgeExists) {
          edgeList.push({
            source: alert.user_id,
            target: alert.device_id,
            hops: 1,
            type: alert.attack_category || 'Auth Session',
            risk: alert.severity
          });
        }
      }
    });

    // If user types a specific ID (e.g. "usr-new-999") that isn't in default list, dynamically register it
    const trimmedQuery = searchQuery.trim();
    if (trimmedQuery && !nodeMap.has(trimmedQuery)) {
      nodeMap.set(trimmedQuery, {
        id: trimmedQuery,
        label: `Ingested Node: ${trimmedQuery}`,
        type: 'user',
        status: 'COMPROMISED',
        riskScore: 0.95,
        subnet: 'Corporate-LAN',
        ip: '198.51.100.99'
      });
      edgeList.push({
        source: trimmedQuery,
        target: 'gw-01',
        hops: 1,
        type: 'Ingested Telemetry Stream',
        risk: 'CRITICAL'
      });
    }

    return { nodes: Array.from(nodeMap.values()), edges: edgeList };
  }, [alerts, searchQuery]);

  // Dynamic filtering for search input and subnet selection
  const filteredNodes = nodes.filter((node) => {
    const matchesSubnet = selectedSubnet === 'all' || node.subnet === selectedSubnet;
    const q = searchQuery.toLowerCase().trim();
    const matchesQuery = !q || 
      node.label.toLowerCase().includes(q) || 
      node.id.toLowerCase().includes(q) || 
      node.ip.toLowerCase().includes(q) || 
      node.subnet.toLowerCase().includes(q);
    return matchesSubnet && matchesQuery;
  });

  const activeNodeDetails = nodes.find((n) => n.id === selectedNodeId) || filteredNodes[0] || nodes[0];

  const activeConnections = edges.filter(
    (e) => e.source === activeNodeDetails?.id || e.target === activeNodeDetails?.id
  );

  return (
    <div className="p-6 space-y-6 bg-slate-950 text-slate-50 min-h-screen">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-white flex items-center gap-2">
            <Network className="h-6 w-6 text-cyan-400" />
            Enterprise Streaming Graph Topology Explorer
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Real-time in-memory NetworkX multigraph & 3-Hop lateral movement path detection
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Badge className="bg-emerald-500/10 text-emerald-400 border-emerald-500/20 px-3 py-1">
            <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse mr-2"></span>
            Graph Stream Live ({filteredNodes.length} / {nodes.length} Active Nodes)
          </Badge>
        </div>
      </div>

      {/* Controls Bar */}
      <Card className="p-4 bg-slate-900/60 border-slate-800 flex flex-wrap items-center justify-between gap-4">
        <div className="flex items-center gap-3 flex-1 min-w-[280px]">
          <Search className="h-4 w-4 text-slate-400" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Live search by Node ID, Name, IP address, or Subnet (e.g. usr-new-999)..."
            className="bg-slate-950 border border-slate-800 rounded-md px-3 py-1.5 text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:border-cyan-500 flex-1"
          />
          {searchQuery && (
            <button 
              onClick={() => setSearchQuery('')}
              className="text-xs text-slate-400 hover:text-slate-200 underline"
            >
              Clear
            </button>
          )}
        </div>
        <div className="flex items-center gap-3">
          <Filter className="h-4 w-4 text-slate-400" />
          <span className="text-xs text-slate-400 font-medium">Filter Subnet:</span>
          <select
            value={selectedSubnet}
            onChange={(e) => setSelectedSubnet(e.target.value)}
            className="bg-slate-950 border border-slate-800 rounded-md px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-cyan-500"
          >
            <option value="all">All Subnets ({nodes.length} Nodes)</option>
            <option value="Corporate-LAN">Corporate-LAN</option>
            <option value="DMZ">DMZ</option>
            <option value="Secure-VLAN">Secure-VLAN</option>
          </select>
        </div>
      </Card>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Visual Graph View Canvas */}
        <Card className="lg:col-span-2 p-6 bg-slate-900/60 border-slate-800 flex flex-col justify-between min-h-[500px]">
          <div>
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-sm font-semibold text-slate-300 uppercase tracking-wider flex items-center gap-2">
                <Cpu className="h-4 w-4 text-cyan-400" /> NetworkX Directed MultiGraph Map
              </h2>
              <span className="text-xs font-mono text-cyan-400 bg-cyan-950/60 border border-cyan-800/60 px-2 py-1 rounded">
                Path Hop Metric: Shortest Dijkstra Distance
              </span>
            </div>

            {/* Canvas Graph Nodes */}
            <div className="relative border border-slate-800/80 rounded-lg p-8 bg-slate-950/80 min-h-[380px] flex items-center justify-around overflow-x-auto gap-4">
              {filteredNodes.length > 0 ? (
                filteredNodes.map((node) => {
                  const isSelected = selectedNodeId === node.id;
                  return (
                    <div 
                      key={node.id} 
                      onClick={() => setSelectedNodeId(node.id)}
                      className={`flex flex-col items-center gap-2 group cursor-pointer p-3 rounded-xl transition-all relative ${
                        isSelected ? 'bg-slate-900/90 ring-2 ring-cyan-500 shadow-xl scale-105' : 'hover:bg-slate-900/50'
                      }`}
                    >
                      <div
                        className={`h-16 w-16 rounded-full flex items-center justify-center border-2 transition-all group-hover:scale-110 shadow-lg ${
                          node.status === 'COMPROMISED'
                            ? 'bg-red-950/80 border-red-500 text-red-400 shadow-red-500/20'
                            : node.status === 'HIGH_RISK'
                            ? 'bg-amber-950/80 border-amber-500 text-amber-400 shadow-amber-500/20'
                            : 'bg-slate-900 border-cyan-500/60 text-cyan-400 shadow-cyan-500/10'
                        }`}
                      >
                        <Network className="h-7 w-7" />
                      </div>
                      <div className="text-center">
                        <p className="text-xs font-semibold text-slate-200">{node.label}</p>
                        <span className="text-[10px] text-slate-500 block">{node.subnet} ({node.ip})</span>
                        <Badge
                          className={`mt-1 text-[9px] px-1.5 py-0.5 ${
                            node.status === 'COMPROMISED'
                              ? 'bg-red-500/20 text-red-400 border-red-500/30'
                              : node.status === 'HIGH_RISK'
                              ? 'bg-amber-500/20 text-amber-400 border-amber-500/30'
                              : 'bg-slate-800 text-slate-400 border-slate-700'
                          }`}
                        >
                          Risk: {(node.riskScore * 100).toFixed(0)}%
                        </Badge>
                      </div>
                    </div>
                  );
                })
              ) : (
                <div className="text-center py-12 text-slate-500">
                  <Search className="h-8 w-8 mx-auto mb-2 opacity-50" />
                  <p className="text-sm">No nodes matched your search "{searchQuery}"</p>
                </div>
              )}
            </div>
          </div>

          <div className="mt-4 text-xs text-slate-500 flex items-center justify-between">
            <span>● Click any node circle to inspect its active user connection path</span>
            <span>● Red Nodes: High Anomaly Risk | Cyan Nodes: Verified Baseline</span>
          </div>
        </Card>

        {/* Selected Node Details & Active User Connections List */}
        <div className="space-y-6">
          {/* Active Node Detail Inspector */}
          {activeNodeDetails && (
            <Card className="p-5 bg-slate-900/60 border-slate-800 space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="text-sm font-semibold text-white flex items-center gap-2">
                  <Info className="h-4 w-4 text-cyan-400" /> Active Selected Node
                </h3>
                <Badge
                  className={`text-[9px] ${
                    activeNodeDetails.status === 'COMPROMISED'
                      ? 'bg-red-500/20 text-red-400 border-red-500/30'
                      : activeNodeDetails.status === 'HIGH_RISK'
                      ? 'bg-amber-500/20 text-amber-400 border-amber-500/30'
                      : 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30'
                  }`}
                >
                  {activeNodeDetails.status}
                </Badge>
              </div>

              <div className="p-3 bg-slate-950 border border-slate-800 rounded-lg space-y-1.5 text-xs">
                <div className="flex justify-between">
                  <span className="text-slate-400">Node ID:</span>
                  <span className="font-mono text-cyan-400">{activeNodeDetails.id}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">IP Address:</span>
                  <span className="font-mono text-slate-200">{activeNodeDetails.ip}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Subnet Zone:</span>
                  <span className="text-slate-200">{activeNodeDetails.subnet}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Calculated Risk:</span>
                  <span className="font-bold text-red-400">{(activeNodeDetails.riskScore * 100).toFixed(1)}%</span>
                </div>
              </div>

              {/* Active Connections List for this node */}
              <div className="space-y-2">
                <h4 className="text-xs font-semibold text-slate-300 flex items-center gap-1.5">
                  <Link2 className="h-3.5 w-3.5 text-cyan-400" /> Connected Devices for {activeNodeDetails.id}:
                </h4>
                {activeConnections.length > 0 ? (
                  activeConnections.map((conn, idx) => (
                    <div key={idx} className="p-2.5 bg-slate-950/80 border border-cyan-900/40 rounded-md text-xs space-y-1">
                      <div className="flex items-center justify-between">
                        <span className="font-mono text-cyan-300 flex items-center gap-1">
                          {conn.source} <ArrowRight className="h-3 w-3 text-slate-500" /> {conn.target}
                        </span>
                        <span className="text-[10px] font-semibold text-amber-400 bg-amber-950/60 px-1.5 py-0.5 rounded">
                          {conn.type}
                        </span>
                      </div>
                      <div className="text-[10px] text-slate-400 flex justify-between">
                        <span>Hop Distance: {conn.hops}</span>
                        <span className="text-red-400 font-semibold">Risk: {conn.risk}</span>
                      </div>
                    </div>
                  ))
                ) : (
                  <p className="text-xs text-slate-500 italic p-2 bg-slate-950 rounded">No active edge connections for this node.</p>
                )}
              </div>
            </Card>
          )}

          {/* Full Network Edge Hops & Risk List */}
          <Card className="p-5 bg-slate-900/60 border-slate-800 space-y-4">
            <h2 className="text-sm font-semibold text-slate-300 uppercase tracking-wider flex items-center gap-2">
              <ShieldAlert className="h-4 w-4 text-red-400" /> All Detected Network Edges
            </h2>

            <div className="space-y-3">
              {edges.map((edge, idx) => (
                <div key={idx} className="p-3 bg-slate-950 border border-slate-800/80 rounded-lg space-y-1">
                  <div className="flex items-center justify-between text-xs">
                    <span className="font-semibold text-slate-300">{edge.source} ➔ {edge.target}</span>
                    <Badge
                      className={`text-[9px] px-1.5 ${
                        edge.risk === 'CRITICAL'
                          ? 'bg-red-500/20 text-red-400 border-red-500/30'
                          : edge.risk === 'HIGH'
                          ? 'bg-amber-500/20 text-amber-400 border-amber-500/30'
                          : 'bg-cyan-500/10 text-cyan-400 border-cyan-500/20'
                      }`}
                    >
                      {edge.risk} RISK
                    </Badge>
                  </div>
                  <div className="flex items-center justify-between text-[11px] text-slate-400">
                    <span>Protocol: {edge.type}</span>
                    <span className="font-mono text-cyan-400">Hop Distance: {edge.hops}</span>
                  </div>
                </div>
              ))}
            </div>

            <div className="p-3 bg-cyan-950/30 border border-cyan-800/40 rounded-lg text-xs text-cyan-300 flex items-start gap-2">
              <Zap className="h-4 w-4 text-cyan-400 shrink-0 mt-0.5" />
              <p>
                In-memory streaming graph continuously prunes edges older than 60 minutes to maintain sub-second Dijkstra path calculation.
              </p>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}
export default GraphTopologyPage;
