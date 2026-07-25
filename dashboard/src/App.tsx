import React, { useState } from 'react';
import { Sidebar } from './components/layout/Sidebar';
import { TopNav } from './components/layout/TopNav';
import { OverviewPage } from './pages/OverviewPage';
import { AlertsPage } from './pages/AlertsPage';
import { AlertDetailPage } from './pages/AlertDetailPage';
import { EntityProfilePage } from './pages/EntityProfilePage';
import { GraphTopologyPage } from './pages/GraphTopologyPage';
import { SystemSettingsPage } from './pages/SystemSettingsPage';

export function App() {
  const [activeTab, setActiveTab] = useState<string>('alerts');

  const renderTabContent = () => {
    switch (activeTab) {
      case 'overview':
        return <OverviewPage />;
      case 'alerts':
        return <AlertsPage onSelectAlert={() => setActiveTab('detail')} />;
      case 'detail':
        return <AlertDetailPage />;
      case 'entities':
        return <EntityProfilePage />;
      case 'network':
        return <GraphTopologyPage />;
      case 'settings':
        return <SystemSettingsPage />;
      default:
        return <AlertsPage onSelectAlert={() => setActiveTab('detail')} />;
    }
  };

  return (
    <div className="flex min-h-screen bg-slate-950 text-slate-50">
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />
      <div className="flex-1 flex flex-col min-w-0">
        <TopNav />
        <main className="flex-1">
          {renderTabContent()}
        </main>
      </div>
    </div>
  );
}

export default App;
