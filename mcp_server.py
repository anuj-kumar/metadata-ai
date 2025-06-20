from mcp.server.fastmcp import FastMCP
from typing import Dict, Any, Optional, List
from metadata.ingestion.ometa.ometa_api import OpenMetadata
from metadata.generated.schema.entity.data.dashboard import Dashboard
from metadata.generated.schema.entity.data.table import Table
from metadata.generated.schema.entity.data.query import Query
from metadata.generated.schema.type.basic import SqlQuery
from metadata.generated.schema.entity.services.connections.metadata.openMetadataConnection import OpenMetadataConnection, AuthProvider
from metadata.generated.schema.security.client.openMetadataJWTClientConfig import OpenMetadataJWTClientConfig
from config import Config
from rag.retriever import RAGRetriever
from rag.vector_store import MongoVectorStore
from rag.embedder import LangchainEmbedder
from rag.mongo import get_collection


mcp = FastMCP("OpenMetadata MCP Server", stateless_http=True)

server_conf = OpenMetadataConnection(
    hostPort=Config.METADATA_ENDPOINT,
    authProvider=AuthProvider.openmetadata,
    securityConfig=OpenMetadataJWTClientConfig(
        jwtToken=Config.METADATA_JWT_TOKEN,
    ),
)
metadata = OpenMetadata(server_conf)

# mongo_host = Config.MONGO_HOST
# mongo_user = Config.MONGO_USER
# mongo_password = Config.MONGO_PASSWORD
# collection = get_collection(mongo_host, mongo_user, mongo_password, "assets")
# vector_store = MongoVectorStore(collection)
# embedder = LangchainEmbedder()
# retriever = RAGRetriever(vector_store, embedder)

@mcp.resource("ometa://dashboard/{dashboard_id}/performance")
def get_dashboard_performance(dashboard_id: str) -> Dict[str, Any]:
    dashboard: Dashboard = metadata.get_by_id(Dashboard, dashboard_id)
    # Placeholder: You may need to fetch performance metrics from dashboard's extension or custom fields
    return {"dashboard": dashboard.displayName, "performance": "N/A (customize as needed)"}

@mcp.resource("ometa://dashboard/{dashboard_id}/broken")
def get_broken_dashboard(dashboard_id: str) -> Dict[str, Any]:
    dashboard: Dashboard = metadata.get_by_id(Dashboard, dashboard_id)
    # Placeholder: You may need to fetch error details from dashboard's extension or custom fields
    return {"dashboard": dashboard.displayName, "errors": "N/A (customize as needed)"}

@mcp.resource("ometa://asset/{asset_id}/similar")
def get_similar_assets(asset_id: str) -> Dict[str, Any]:
    # Placeholder: Implement semantic search using SDK if available
    return {"similar_assets": []}

@mcp.resource("ometa://dashboard/{dashboard_id}")
def get_dashboard_details(dashboard_id: str) -> Dict[str, Any]:
    dashboard: Dashboard = metadata.get_by_id(Dashboard, dashboard_id)
    return dashboard.to_dict() if dashboard else {"error": "Dashboard not found"}

@mcp.tool("update_table_by_id", "Update a table's metadata using its ID")
def update_table(tableId: Optional[str] = None) -> Dict[str, Any]:
    table: Table = metadata.get_by_id(Table, tableId)
    return {"message": f"{table.name}"}

@mcp.tool("say_hello", "Will say hello to the user")
def say_hello(user: Optional[str] = None) -> Dict[str, Any]:
    return {"message": f"Hello. {user}"}

@mcp.tool("update_table_by_name", "Update a table's metadata using its name")
def update_table_by_name(tableName: Optional[str] = None) -> Dict[str, Any]:
    table: Table = metadata.get_by_name(Table, tableName)
    return {"message": f"{table.name}"}

@mcp.resource("ometa://table/?limit={limit}&after={after}")
def list_tables(limit=100, after=None) -> str:
    tables = metadata.list_entities(Table, limit, after).model_dump()
    return f"Here are the tables {tables}"

@mcp.tool("get_query", "Get query for a specific query ID")
def get_query(query_id: str) -> Dict[str, Any]:
    query = metadata.get_by_id(Query, query_id)
    if not query:
        return {"error": "Query not found"}
    return query.model_dump()

@mcp.tool("optimize_query", "Optimize a query using query ID")
def optimize_query(query: Query, updated_query: SqlQuery) -> Dict[str, Any]:
    query.query = updated_query
    metadata.create_or_update(query)
    if not query:
        return {"error": "Query not found"}
    return query.model_dump()

@mcp.tool("similar_assets", "Find semantically similar data assets from OpenMetadata using RAG")
def get_similar_assets(query: str, top_k: int = 5) -> list:
    # results = retriever.retrieve_similar(query, top_k=top_k)
    # return [{"asset_id": doc["_id"], "metadata": doc["metadata"]} for doc in results]
    pass


if __name__ == "__main__":
    mcp.run()
