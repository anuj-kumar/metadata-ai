from typing import Dict, Any
# Import OpenMetadata SDK
from metadata.ingestion.ometa.ometa_api import OpenMetadata
from metadata.generated.schema.entity.data.dashboard import Dashboard
from metadata.generated.schema.entity.services.connections.metadata.openMetadataConnection import OpenMetadataConnection


class MetadataContextGatherer:
    """
    Gathers context from OpenMetadata API based on the selected strategy using the OpenMetadata Python SDK.
    """
    def __init__(self, server_config: Dict[str, Any] = None):
        # server_config should contain 'api_endpoint' and 'auth_provider' keys
        self.server_config = server_config or {
            "api_endpoint": "http://localhost:8585/api",
            "auth_provider_type": "no-auth"
        }
        connection = OpenMetadataConnection(**self.server_config)
        self.metadata = OpenMetadata(connection)

    def get_dashboard_performance(self, dashboard_id: str) -> Dict[str, Any]:
        dashboard: Dashboard = self.metadata.get_by_id(Dashboard, dashboard_id)
        # Placeholder: You may need to fetch performance metrics from dashboard's extension or custom fields
        return {"dashboard": dashboard.displayName, "performance": "N/A (customize as needed)"}

    def get_broken_dashboard(self, dashboard_id: str) -> Dict[str, Any]:
        dashboard: Dashboard = self.metadata.get_by_id(Dashboard, dashboard_id)
        # Placeholder: You may need to fetch error details from dashboard's extension or custom fields
        return {"dashboard": dashboard.displayName, "errors": "N/A (customize as needed)"}

    def get_similar_assets(self, asset_id: str) -> Dict[str, Any]:
        # Placeholder: Implement semantic search using SDK if available
        return {"similar_assets": []}

    def get_dashboard_details(self, dashboard_id: str) -> Dict[str, Any]:
        dashboard: Dashboard = self.metadata.get_by_id(Dashboard, dashboard_id)
        return dashboard.to_dict() if dashboard else {"error": "Dashboard not found"}

    def gather(self, strategy: str, **kwargs) -> Dict[str, Any]:
        if not hasattr(self, strategy):
            raise ValueError(f"Unknown strategy: {strategy}")
        return getattr(self, strategy)(**kwargs)

def gather_context(intent: Dict[str, Any], **kwargs):
    gatherer = MetadataContextGatherer()
    strategy = intent.get('strategy')
    return gatherer.gather(strategy, **kwargs)
