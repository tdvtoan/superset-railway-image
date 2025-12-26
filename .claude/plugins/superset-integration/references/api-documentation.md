# Superset REST API Documentation

## API Overview

Apache Superset provides a comprehensive REST API that follows the OpenAPI specification. The API is documented using Swagger React UI and is available at `/swagger/v1` on your Superset instance.

### Access Points

- **Interactive Documentation**: `http://<superset-instance>/swagger/v1`
- **OpenAPI Specification**: `GET http://<superset-instance>/api/v1/openapi`
- **Base API Endpoint**: `http://<superset-instance>/api/v1`

## Authentication

All API requests require authentication using JWT tokens.

### Login Endpoint

```
POST /api/v1/security/login
Content-Type: application/json

{
  "username": "admin",
  "password": "admin"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Using the Token

Include the access token in all subsequent requests:

```
Authorization: Bearer <access_token>
```

**Example with curl:**
```bash
curl -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..." \
  http://localhost:8088/api/v1/databases
```

### Token Refresh

For long-running sessions, use the refresh token to obtain new access tokens without re-authenticating.

**Refresh Token Endpoint:**
```
POST /api/v1/security/refresh
Authorization: Bearer <refresh_token>
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Python Example:**
```python
# Refresh token when access token expires
refresh_response = requests.post(
    f"{base_url}/api/v1/security/refresh",
    headers={"Authorization": f"Bearer {refresh_token}"}
)
new_access_token = refresh_response.json()["access_token"]
headers = {"Authorization": f"Bearer {new_access_token}"}
```

This approach allows maintaining API connections without requiring stored credentials.

## Core API Endpoints

### Databases Management

#### List Databases
```
GET /api/v1/databases
```

Returns all registered database connections.

**Query Parameters:**
- `q` - Filter by name
- `page` - Pagination page number
- `page_size` - Items per page

**Response:**
```json
{
  "result": [
    {
      "id": 1,
      "database_name": "MySQL Database",
      "backend": "mysql",
      "port": 3306,
      "host": "localhost"
    }
  ]
}
```

#### Create Database Connection
```
POST /api/v1/databases
Content-Type: application/json

{
  "database_name": "My Database",
  "sqlalchemy_uri": "mysql://user:password@localhost:3306/dbname",
  "driver": "pymysql",
  "cache_timeout": 3600
}
```

#### Update Database
```
PUT /api/v1/databases/{id}
Content-Type: application/json

{
  "database_name": "Updated Name",
  "cache_timeout": 7200
}
```

#### Test Database Connection
```
POST /api/v1/databases/test_connection
Content-Type: application/json

{
  "sqlalchemy_uri": "mysql://user:password@localhost:3306/dbname"
}
```

### Datasets (Tables) Management

#### List Datasets
```
GET /api/v1/datasets
```

Returns all registered datasets.

**Query Parameters:**
- `q` - Filter by name
- `page` - Pagination page
- `page_size` - Items per page

#### Create Dataset
```
POST /api/v1/datasets
Content-Type: application/json

{
  "database_id": 1,
  "schema": "public",
  "table_name": "customers",
  "owner_ids": [1]
}
```

**Response:**
```json
{
  "id": 5,
  "dataset_name": "customers",
  "database_id": 1,
  "schema": "public",
  "table_name": "customers"
}
```

#### Configure Column Properties
```
PUT /api/v1/datasets/{id}
Content-Type: application/json

{
  "columns": [
    {
      "column_name": "created_at",
      "is_dttm": true,
      "python_date_format": "%Y-%m-%d %H:%M:%S",
      "is_active": true
    },
    {
      "column_name": "customer_id",
      "is_dttm": false,
      "filterable": true,
      "is_active": true
    }
  ]
}
```

**Column Property Definitions:**
- `is_dttm` - Mark column as datetime
- `filterable` - Column available in filters
- `groupby` - Column can be used for grouping
- `python_date_format` - DateTime format string for parsing
- `is_active` - Include column in dataset

#### Get Dataset Details
```
GET /api/v1/datasets/{id}
```

### Charts Management

#### Create Chart
```
POST /api/v1/charts
Content-Type: application/json

{
  "dataset_id": 5,
  "chart_title": "Customer Growth",
  "visualization_type": "line",
  "query_context": {
    "datasource": {
      "id": 5,
      "type": "table"
    },
    "form_data": {
      "granularity_sqla": "created_at",
      "time_range": "Last year",
      "metrics": [{"label": "count"}],
      "groupby": ["country"]
    }
  }
}
```

**Visualization Types:**
- `line` - Line chart
- `bar` - Bar chart
- `pie` - Pie chart
- `scatter` - Scatter plot
- `area` - Area chart
- `table` - Data table
- `pivot_table` - Pivot table
- `map` - Geospatial map
- `heatmap` - Heatmap visualization

#### Update Chart
```
PUT /api/v1/charts/{id}
Content-Type: application/json

{
  "chart_title": "Updated Title",
  "description": "Chart description",
  "visualization_type": "bar"
}
```

#### List Charts
```
GET /api/v1/charts
```

#### Get Chart Data
```
GET /api/v1/charts/{id}/data
```

### Dashboards Management

#### Create Dashboard
```
POST /api/v1/dashboards
Content-Type: application/json

{
  "dashboard_title": "Sales Overview",
  "description": "Dashboard for sales metrics",
  "dashboard_layout_version": "GRID_LAYOUT_v1"
}
```

**Response:**
```json
{
  "id": 10,
  "dashboard_title": "Sales Overview",
  "description": "Dashboard for sales metrics"
}
```

#### Add Charts to Dashboard
```
PUT /api/v1/dashboards/{id}
Content-Type: application/json

{
  "dashboard_layout_version": "GRID_LAYOUT_v1",
  "dashboard_layout": {
    "GRID_ID": {
      "GRID_DATA": {
        "123": {
          "meta": {
            "chartId": 1,
            "height": 50,
            "width": 4,
            "sliceName": "Customer Chart"
          }
        }
      }
    }
  }
}
```

#### Publish Dashboard
```
PUT /api/v1/dashboards/{id}
Content-Type: application/json

{
  "published": true
}
```

#### Get Dashboard Details
```
GET /api/v1/dashboards/{id}
```

#### List Dashboards
```
GET /api/v1/dashboards
```

### Query Execution

#### Execute SQL Query
```
POST /api/v1/query/
Content-Type: application/json

{
  "client_id": "query-1",
  "database_id": 1,
  "sql": "SELECT COUNT(*) FROM customers",
  "async": false
}
```

#### Get Query Results
```
GET /api/v1/query/{query_id}
```

## Common API Workflows

### Workflow 1: Setup New Data Source

```python
import requests

base_url = "http://localhost:8088"

# 1. Login
auth_resp = requests.post(
    f"{base_url}/api/v1/security/login",
    json={"username": "admin", "password": "admin"}
)
token = auth_resp.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# 2. Create database
db_resp = requests.post(
    f"{base_url}/api/v1/databases",
    headers=headers,
    json={
        "database_name": "Production DB",
        "sqlalchemy_uri": "postgresql://user:pass@localhost/proddb"
    }
)
database_id = db_resp.json()["id"]

# 3. Create dataset
dataset_resp = requests.post(
    f"{base_url}/api/v1/datasets",
    headers=headers,
    json={
        "database_id": database_id,
        "schema": "public",
        "table_name": "sales"
    }
)
dataset_id = dataset_resp.json()["id"]
```

### Workflow 2: Create and Configure Chart

```python
# Configure columns first
requests.put(
    f"{base_url}/api/v1/datasets/{dataset_id}",
    headers=headers,
    json={
        "columns": [
            {"column_name": "date", "is_dttm": True},
            {"column_name": "region", "filterable": True}
        ]
    }
)

# Create chart
chart_resp = requests.post(
    f"{base_url}/api/v1/charts",
    headers=headers,
    json={
        "dataset_id": dataset_id,
        "chart_title": "Sales by Region",
        "visualization_type": "bar",
        "query_context": {
            "datasource": {"id": dataset_id, "type": "table"},
            "form_data": {
                "granularity_sqla": "date",
                "metrics": [{"label": "sum__amount"}],
                "groupby": ["region"]
            }
        }
    }
)
chart_id = chart_resp.json()["id"]
```

### Workflow 3: Create Dashboard with Charts

```python
# Create dashboard
dashboard_resp = requests.post(
    f"{base_url}/api/v1/dashboards",
    headers=headers,
    json={
        "dashboard_title": "Sales Analytics",
        "description": "Comprehensive sales metrics"
    }
)
dashboard_id = dashboard_resp.json()["id"]

# Add chart to dashboard
requests.put(
    f"{base_url}/api/v1/dashboards/{dashboard_id}",
    headers=headers,
    json={
        "dashboard_layout_version": "GRID_LAYOUT_v1",
        "dashboard_layout": {
            "GRID_ID": {
                "GRID_DATA": {
                    "0": {
                        "meta": {
                            "chartId": chart_id,
                            "height": 50,
                            "width": 12
                        }
                    }
                }
            }
        }
    }
)

# Publish dashboard
requests.put(
    f"{base_url}/api/v1/dashboards/{dashboard_id}",
    headers=headers,
    json={"published": True}
)
```

## Error Handling

API responses follow standard HTTP status codes:

- `200` - Success
- `400` - Bad request (invalid parameters)
- `401` - Unauthorized (invalid token)
- `403` - Forbidden (insufficient permissions)
- `404` - Not found
- `422` - Validation error (schema mismatch)
- `500` - Server error

Error responses include detail:

```json
{
  "errors": [
    {
      "message": "Invalid database configuration",
      "error_type": "DATABASE_ERROR"
    }
  ]
}
```

## Rate Limiting and Performance

- Respect API rate limits if configured
- Use pagination for large result sets
- Cache tokens to avoid repeated authentication
- Consider async query execution for large datasets

## Testing API Calls

Use the Swagger UI to test endpoints:

1. Navigate to `/swagger/v1` on your Superset instance
2. Click "Authorize" and enter credentials
3. Expand endpoint and click "Try it out"
4. Modify request parameters and execute
5. View responses and response schemas

## Additional Resources

- [Superset API Documentation](https://superset.apache.org/docs/api/)
- [OpenAPI Specification Reference](https://swagger.io/specification/)
- Superset instance Swagger UI: `/swagger/v1`
