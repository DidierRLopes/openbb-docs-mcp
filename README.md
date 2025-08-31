# OpenBB Widgets JSON MCP Server

An MCP server that exposes the OpenBB widgets.json specification as structured, callable tools. Instead of parsing long-form documentation, developers (and AI coding assistants like Claude Code) can directly query widget types, inputs, and configuration examples through this server.

## What This Does

Each widget type is mapped to its own tool—making it easy to generate, mix, and match valid JSON specs when building new OpenBB apps. The server is built with FastMCP, programmatically generated from the OpenBB developer docs, and hosted on Smithery.ai for discoverability.

The server provides:
- Widget configuration and types documentation
- Widget parameters (dropdowns, date pickers, toggles, etc.)
- JSON specifications for widgets, apps, and agents
- Essential boilerplate code for building OpenBB widgets
- Data integration and AI agents documentation

## Prerequisites

- Python 3.12 or higher
- [uv](https://docs.astral.sh/uv/) package manager
- Node.js and npx (optional, for Smithery CLI and playground)

## Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/OpenBB-finance/openbb-widgets-json-mcp.git
   cd openbb-widgets-json-mcp
   ```

2. **Install dependencies:**
   ```bash
   uv sync
   ```

3. **Run the server:**
   ```bash
   uv run python main.py
   ```

4. **Test it's working:**
   The server will start on `http://localhost:8081`

5. **Launch Smithery Playground (optional):**
   ```bash
   npm install -g @smithery/cli
   smithery playground --port 8081
   ```
   
   This opens an interface to test the MCP tools interactively.

## Available MCP Tools

### Via iterating through OpenBB docs

#### Widget Configuration Tools
- `widget_configuration_category_subcategory` - Category and subcategory configuration
- `widget_configuration_error_handling` - Error handling in widgets
- `widget_configuration_grid_size` - Grid size configuration
- `widget_configuration_refetch_interval` - Refetch interval settings
- `widget_configuration_render_functions` - Render functions
- `widget_configuration_run_button` - Run button configuration
- `widget_configuration_stale_time` - Stale time settings

#### Widget Parameter Tools  
- `widget_parameters_text_input` - Text input parameters
- `widget_parameters_date_picker` - Date picker parameters
- `widget_parameters_boolean_toggle` - Boolean toggle parameters
- `widget_parameters_dropdown` - Dropdown parameters
- `widget_parameters_advanced_dropdown` - Advanced dropdown parameters
- `widget_parameters_dependent_dropdown` - Dependent dropdown parameters
- `widget_parameters_number_input` - Number input parameters
- `widget_parameters_input_form` - Input form parameters
- `widget_parameters_parameter_grouping` - Parameter grouping
- `widget_parameters_parameter_positioning` - Parameter positioning
- `widget_parameters_cell_click_grouping` - Cell click grouping

#### Widget Type Tools
- `widget_types_plotly_charts` - Plotly charts
- `widget_types_highcharts` - Highcharts
- `widget_types_tradingview_charts` - TradingView charts
- `widget_types_aggrid_table_charts` - AgGrid table charts
- `widget_types_markdown` - Markdown widgets
- `widget_types_html` - HTML widgets
- `widget_types_metric` - Metric widgets
- `widget_types_newsfeed` - Newsfeed widgets
- `widget_types_file_viewer` - File viewer widgets
- `widget_types_live_grid` - Live grid widgets
- `widget_types_omni` - Omni widgets
- `widget_types_ssrm_mode` - SSRM mode

#### JSON Reference Tools
- `json_specs_widgets_json_reference` - Widgets JSON reference
- `json_specs_apps_json_reference` - Apps JSON reference
- `json_specs_agents_json_reference` - Agents JSON reference

#### Additional Tools
- `data_integration` - Data source integration
- `ai_agents_ai_agents` - AI agents documentation
- `apps_apps` - OpenBB applications documentation

### Added ad-hoc
- `building_widgets_on_openbb` - Essential boilerplate code for OpenBB widgets (ALWAYS call this first)


## Deploy to Smithery

To deploy your MCP server:
- Push your code to GitHub (include `smithery.yaml` and `Dockerfile`)
- Connect your repository at [https://smithery.ai/new](https://smithery.ai/new)

Your server will be available over HTTP and ready to use with any MCP-compatible client!

## Stopping the Server

Press `Ctrl+C` in the terminal to stop the server.
