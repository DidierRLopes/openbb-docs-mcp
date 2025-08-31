import os
import uvicorn
import requests
from mcp.server.fastmcp import FastMCP
from starlette.middleware.cors import CORSMiddleware

# Dictionary of OpenBB documentation tools
OPENBB_DOCS_TOOLS = {
    # Main developer docs
    "data-integration": {
        "description": "Documentation for integrating data sources into the OpenBB platform",
        "context": "https://raw.githubusercontent.com/OpenBB-finance/openbb-docs/major-refactor/content/workspace/developers/data-integration.md"
    },
    
    # AI Agents
    "ai-agents_ai-agents": {
        "description": "Documentation about AI agents in OpenBB",
        "context": "https://raw.githubusercontent.com/OpenBB-finance/openbb-docs/major-refactor/content/workspace/developers/ai-agents/ai-agents.md"
    },
    
    # Apps
    "apps_apps": {
        "description": "Documentation about OpenBB applications",
        "context": "https://raw.githubusercontent.com/OpenBB-finance/openbb-docs/major-refactor/content/workspace/developers/apps/apps.md"
    },
    
    # JSON Specs
    "json-specs_agents-json-reference": {
        "description": "JSON reference documentation for agents configuration",
        "context": "https://raw.githubusercontent.com/OpenBB-finance/openbb-docs/major-refactor/content/workspace/developers/json-specs/agents-json-reference.md"
    },
    "json-specs_apps-json-reference": {
        "description": "JSON reference documentation for apps configuration",
        "context": "https://raw.githubusercontent.com/OpenBB-finance/openbb-docs/major-refactor/content/workspace/developers/json-specs/apps-json-reference.md"
    },
    "json-specs_widgets-json-reference": {
        "description": "JSON reference documentation for widgets configuration",
        "context": "https://raw.githubusercontent.com/OpenBB-finance/openbb-docs/major-refactor/content/workspace/developers/json-specs/widgets-json-reference.md"
    },
    
    # Widget Configuration
    "widget-configuration_category-subcategory": {
        "description": "Documentation for widget category and subcategory configuration",
        "context": "https://raw.githubusercontent.com/OpenBB-finance/openbb-docs/major-refactor/content/workspace/developers/widget-configuration/category-subcategory.md"
    },
    "widget-configuration_error-handling": {
        "description": "Documentation for widget error handling",
        "context": "https://raw.githubusercontent.com/OpenBB-finance/openbb-docs/major-refactor/content/workspace/developers/widget-configuration/error-handling.md"
    },
    "widget-configuration_grid-size": {
        "description": "Documentation for widget grid size configuration",
        "context": "https://raw.githubusercontent.com/OpenBB-finance/openbb-docs/major-refactor/content/workspace/developers/widget-configuration/grid-size.md"
    },
    "widget-configuration_refetch-interval": {
        "description": "Documentation for widget refetch interval configuration",
        "context": "https://raw.githubusercontent.com/OpenBB-finance/openbb-docs/major-refactor/content/workspace/developers/widget-configuration/refetch-interval.md"
    },
    "widget-configuration_render-functions": {
        "description": "Documentation for widget render functions",
        "context": "https://raw.githubusercontent.com/OpenBB-finance/openbb-docs/major-refactor/content/workspace/developers/widget-configuration/render-functions.md"
    },
    "widget-configuration_run-button": {
        "description": "Documentation for widget run button configuration",
        "context": "https://raw.githubusercontent.com/OpenBB-finance/openbb-docs/major-refactor/content/workspace/developers/widget-configuration/run-button.md"
    },
    "widget-configuration_stale-time": {
        "description": "Documentation for widget stale time configuration",
        "context": "https://raw.githubusercontent.com/OpenBB-finance/openbb-docs/major-refactor/content/workspace/developers/widget-configuration/stale-time.md"
    },
    
    # Widget Parameters
    "widget-parameters_advanced-dropdown": {
        "description": "Documentation for advanced dropdown widget parameters",
        "context": "https://raw.githubusercontent.com/OpenBB-finance/openbb-docs/major-refactor/content/workspace/developers/widget-parameters/advanced-dropdown.md"
    },
    "widget-parameters_boolean-toggle": {
        "description": "Documentation for boolean toggle widget parameters",
        "context": "https://raw.githubusercontent.com/OpenBB-finance/openbb-docs/major-refactor/content/workspace/developers/widget-parameters/boolean-toggle.md"
    },
    "widget-parameters_cell-click-grouping": {
        "description": "Documentation for cell click grouping in widgets",
        "context": "https://raw.githubusercontent.com/OpenBB-finance/openbb-docs/major-refactor/content/workspace/developers/widget-parameters/cell-click-grouping.md"
    },
    "widget-parameters_date-picker": {
        "description": "Documentation for date picker widget parameters",
        "context": "https://raw.githubusercontent.com/OpenBB-finance/openbb-docs/major-refactor/content/workspace/developers/widget-parameters/date-picker.md"
    },
    "widget-parameters_dependent-dropdown": {
        "description": "Documentation for dependent dropdown widget parameters",
        "context": "https://raw.githubusercontent.com/OpenBB-finance/openbb-docs/major-refactor/content/workspace/developers/widget-parameters/dependent-dropdown.md"
    },
    "widget-parameters_dropdown": {
        "description": "Documentation for dropdown widget parameters",
        "context": "https://raw.githubusercontent.com/OpenBB-finance/openbb-docs/major-refactor/content/workspace/developers/widget-parameters/dropdown.md"
    },
    "widget-parameters_input-form": {
        "description": "Documentation for input form widget parameters",
        "context": "https://raw.githubusercontent.com/OpenBB-finance/openbb-docs/major-refactor/content/workspace/developers/widget-parameters/input-form.md"
    },
    "widget-parameters_number-input": {
        "description": "Documentation for number input widget parameters",
        "context": "https://raw.githubusercontent.com/OpenBB-finance/openbb-docs/major-refactor/content/workspace/developers/widget-parameters/number-input.md"
    },
    "widget-parameters_parameter-grouping": {
        "description": "Documentation for parameter grouping in widgets",
        "context": "https://raw.githubusercontent.com/OpenBB-finance/openbb-docs/major-refactor/content/workspace/developers/widget-parameters/parameter-grouping.md"
    },
    "widget-parameters_parameter-positioning": {
        "description": "Documentation for parameter positioning in widgets",
        "context": "https://raw.githubusercontent.com/OpenBB-finance/openbb-docs/major-refactor/content/workspace/developers/widget-parameters/parameter-positioning.md"
    },
    "widget-parameters_text-input": {
        "description": "Documentation for text input widget parameters",
        "context": "https://raw.githubusercontent.com/OpenBB-finance/openbb-docs/major-refactor/content/workspace/developers/widget-parameters/text-input.md"
    },
    
    # Widget Types
    "widget-types_aggrid-table-charts": {
        "description": "Documentation for AgGrid table charts widget type",
        "context": "https://raw.githubusercontent.com/OpenBB-finance/openbb-docs/major-refactor/content/workspace/developers/widget-types/aggrid-table-charts.md"
    },
    "widget-types_file-viewer": {
        "description": "Documentation for file viewer widget type",
        "context": "https://raw.githubusercontent.com/OpenBB-finance/openbb-docs/major-refactor/content/workspace/developers/widget-types/file-viewer.md"
    },
    "widget-types_highcharts": {
        "description": "Documentation for Highcharts widget type",
        "context": "https://raw.githubusercontent.com/OpenBB-finance/openbb-docs/major-refactor/content/workspace/developers/widget-types/highcharts.md"
    },
    "widget-types_html": {
        "description": "Documentation for HTML widget type",
        "context": "https://raw.githubusercontent.com/OpenBB-finance/openbb-docs/major-refactor/content/workspace/developers/widget-types/html.md"
    },
    "widget-types_live-grid": {
        "description": "Documentation for live grid widget type",
        "context": "https://raw.githubusercontent.com/OpenBB-finance/openbb-docs/major-refactor/content/workspace/developers/widget-types/live-grid.md"
    },
    "widget-types_markdown": {
        "description": "Documentation for markdown widget type",
        "context": "https://raw.githubusercontent.com/OpenBB-finance/openbb-docs/major-refactor/content/workspace/developers/widget-types/markdown.md"
    },
    "widget-types_metric": {
        "description": "Documentation for metric widget type",
        "context": "https://raw.githubusercontent.com/OpenBB-finance/openbb-docs/major-refactor/content/workspace/developers/widget-types/metric.md"
    },
    "widget-types_newsfeed": {
        "description": "Documentation for newsfeed widget type",
        "context": "https://raw.githubusercontent.com/OpenBB-finance/openbb-docs/major-refactor/content/workspace/developers/widget-types/newsfeed.md"
    },
    "widget-types_omni": {
        "description": "Documentation for omni widget type",
        "context": "https://raw.githubusercontent.com/OpenBB-finance/openbb-docs/major-refactor/content/workspace/developers/widget-types/omni.md"
    },
    "widget-types_plotly-charts": {
        "description": "Documentation for Plotly charts widget type",
        "context": "https://raw.githubusercontent.com/OpenBB-finance/openbb-docs/major-refactor/content/workspace/developers/widget-types/plotly-charts.md"
    },
    "widget-types_ssrm-mode": {
        "description": "Documentation for SSRM mode in widgets",
        "context": "https://raw.githubusercontent.com/OpenBB-finance/openbb-docs/major-refactor/content/workspace/developers/widget-types/ssrm_mode.md"
    },
    "widget-types_tradingview-charts": {
        "description": "Documentation for TradingView charts widget type",
        "context": "https://raw.githubusercontent.com/OpenBB-finance/openbb-docs/major-refactor/content/workspace/developers/widget-types/tradingview-charts.md"
    }
}

mcp = FastMCP(name="OpenBB Docs MCP")

# Create MCP tools for each documentation file
for tool_name, tool_info in OPENBB_DOCS_TOOLS.items():
    # Create a closure to capture the current tool_info
    def create_tool_function(name, info):
        def tool_function() -> str:
            """Fetch and return OpenBB documentation content."""
            try:
                response = requests.get(info["context"])
                response.raise_for_status()
                return response.text
            except requests.exceptions.RequestException as e:
                return f"Error fetching documentation: {str(e)}"
        
        # Set function attributes for MCP
        tool_function.__name__ = name.replace("-", "_")
        tool_function.__doc__ = info["description"]
        return tool_function
    
    # Register the tool with MCP
    tool_func = create_tool_function(tool_name, tool_info)
    mcp.tool()(tool_func)

# Get the Starlette app and add CORS middleware
app = mcp.streamable_http_app()

# Add CORS middleware with proper header exposure for MCP session management
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this more restrictively in production
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["mcp-session-id", "mcp-protocol-version"],  # Allow client to read session ID
    max_age=86400,
)

if __name__ == "__main__":

    # Use PORT environment variable
    port = int(os.environ.get("PORT", 8081))

    # Run the MCP server with HTTP transport using uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",  # Listen on all interfaces for containerized deployment
        port=port,
        log_level="debug"
    )