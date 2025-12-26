---
name: Superset Integration
description: This skill should be used when the user asks to "create a Superset dashboard", "use the Superset API", "configure Superset", "interact with Superset programmatically", "query data in Superset", "set up Superset charts", or needs guidance on Superset integration and API operations.
version: 0.1.0
---

# Superset Integration Skill

This skill provides comprehensive guidance for working with Apache Superset, a modern data visualization and business intelligence platform. It covers both the programmatic API approach and the user interface for creating dashboards and visualizations.

## Overview

Apache Superset is a self-hosted, open-source data visualization and exploration platform. There are two primary ways to work with Superset:

1. **REST API** - Programmatic access to create dashboards, charts, and manage data sources
2. **Web UI** - Interactive interface for building dashboards and visualizations

This skill helps you understand when to use each approach and how to execute common tasks.

## When to Use Superset API vs UI

### Use the REST API when:
- Automating dashboard creation from code
- Integrating Superset with other systems
- Bulk operations on multiple dashboards or datasets
- Building custom tools or integrations
- Managing Superset programmatically as part of infrastructure

### Use the Web UI when:
- Exploring data interactively
- Creating visualizations exploratively
- Configuring column properties and settings
- Testing and refining charts before automation
- Non-technical users need dashboard access

## Quick Start: Create a Dashboard via UI

Follow this straightforward approach to create a dashboard:

1. **Connect a Database** - Add database credentials through Data menu
2. **Register a Table** - Import tables as datasets
3. **Create Charts** - Use Explore interface to build visualizations
4. **Build Dashboard** - Combine charts into a dashboard layout
5. **Publish** - Toggle Draft status to make it live

For detailed step-by-step instructions, refer to `references/dashboard-creation.md`.

## API Integration Approach

The Superset REST API follows the OpenAPI specification and provides endpoints for:

- **Authentication** - Login and token management
- **Data Sources** - Create and manage database connections
- **Datasets** - Register tables and configure columns
- **Charts** - Create and configure visualizations
- **Dashboards** - Create, update, and publish dashboards
- **Queries** - Execute queries against datasets

### Key API Endpoints

The API structure follows REST conventions:

```
POST   /api/v1/security/login           - Authenticate
GET    /api/v1/databases                - List databases
POST   /api/v1/datasets                 - Create dataset
POST   /api/v1/charts                   - Create chart
POST   /api/v1/dashboards               - Create dashboard
PUT    /api/v1/dashboards/{id}          - Update dashboard
GET    /api/v1/dashboards/{id}          - Get dashboard details
POST   /api/v1/dashboards/{id}/publish  - Publish dashboard
```

For complete API endpoint specifications, consult `references/api-documentation.md`.

## Authentication

All API requests require authentication. Obtain a token via:

```python
import requests

response = requests.post(
    'http://localhost:8088/api/v1/security/login',
    json={'username': 'admin', 'password': 'admin'}
)
token = response.json()['access_token']
headers = {'Authorization': f'Bearer {token}'}
```

Use the `headers` with all subsequent API requests.

## Working with the OpenAPI Swagger Documentation

Superset provides interactive API documentation via Swagger UI:

1. Access at: `http://<your-superset-instance>/swagger/v1`
2. Explore available endpoints with interactive interface
3. Test API calls directly from the documentation
4. View request/response schemas
5. Understand required parameters

To view the full OpenAPI specification programmatically:
```
GET /api/v1/openapi
```

## Common Workflows

### Workflow 1: Create Database Connection
- Connect to a new database via `/api/v1/databases`
- Test connection to verify credentials
- Store database ID for dataset creation

### Workflow 2: Create Dataset from Table
- Register table as dataset via `/api/v1/datasets`
- Configure column properties (temporal, filterable, dimensional)
- Set up column-level metadata

### Workflow 3: Create and Configure Chart
- Create chart via `/api/v1/charts`
- Specify visualization type, metrics, and grouping
- Link to dataset and configure query parameters

### Workflow 4: Build and Publish Dashboard
- Create dashboard via `/api/v1/dashboards`
- Add charts to dashboard
- Configure dashboard layout and permissions
- Publish by toggling draft status

## Configuration and Setup

### Column Property Configuration

When registering datasets, configure columns with properties:

- **Temporal**: Mark datetime columns for time-based filtering
- **Filterable**: Columns available in dashboard filters
- **Dimensional**: Columns used for grouping and drilling

### Visualization Types

Superset supports diverse visualization types:
- Time series charts
- Bar and column charts
- Pie and donut charts
- Scatter plots
- Maps and geospatial visualizations
- Tables and pivot tables
- And many more

## Access and Permissions

Control dashboard visibility through:

1. **Dataset Permissions** - Restrict who can query specific tables
2. **Dashboard Role-Based Access** - Limit dashboard visibility to specific roles (if enabled)
3. **Draft Status** - Keep dashboards private until ready to publish

## Troubleshooting

For authentication and API errors, consult `references/api-documentation.md` error handling section.
For chart and dashboard issues, see `references/dashboard-creation.md` troubleshooting section.

## Additional Resources

### Reference Files

For comprehensive guidance, consult these reference documents:

- **`references/api-documentation.md`** - Complete API endpoint reference with examples
- **`references/dashboard-creation.md`** - Step-by-step UI guide for dashboard creation

### Examples

Working examples in `examples/`:

- **`examples/api-call-example.py`** - Python code for common API operations
- **`examples/dashboard-setup.md`** - Complete dashboard setup walkthrough

## Next Steps

1. Determine whether to use API or UI for your use case
2. If using API: Consult the API documentation reference
3. If using UI: Follow the dashboard creation guide
4. Test with sample data before moving to production
5. Configure permissions appropriately for your organization
