#!/usr/bin/env python3
"""
Superset API Integration Examples

This script demonstrates common operations with the Superset REST API:
- Authentication
- Database connection management
- Dataset creation and configuration
- Chart creation
- Dashboard management

Prerequisites:
- Superset instance running and accessible
- Admin credentials for authentication
- requests library: pip install requests

Usage:
python api-call-example.py
"""

import requests
import json
from typing import Dict, Any

# Configuration
SUPERSET_URL = "http://localhost:8088"
USERNAME = "admin"
PASSWORD = "admin"


class SupersetClient:
    """Client for interacting with Superset API"""

    def __init__(self, base_url: str, username: str, password: str):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.token = None
        self.headers = {}

    def authenticate(self) -> bool:
        """Authenticate and obtain JWT token"""
        try:
            response = requests.post(
                f"{self.base_url}/api/v1/security/login",
                json={"username": self.username, "password": self.password},
            )
            response.raise_for_status()

            data = response.json()
            self.token = data.get("access_token")
            self.headers = {"Authorization": f"Bearer {self.token}"}

            print("✓ Authentication successful")
            return True
        except requests.exceptions.RequestException as e:
            print(f"✗ Authentication failed: {e}")
            return False

    def list_databases(self) -> list:
        """List all registered databases"""
        try:
            response = requests.get(
                f"{self.base_url}/api/v1/databases", headers=self.headers
            )
            response.raise_for_status()
            databases = response.json().get("result", [])
            print(f"✓ Found {len(databases)} databases")
            for db in databases:
                print(f"  - {db.get('database_name')} (ID: {db.get('id')})")
            return databases
        except requests.exceptions.RequestException as e:
            print(f"✗ Failed to list databases: {e}")
            return []

    def create_database(
        self, name: str, sqlalchemy_uri: str, driver: str = "default"
    ) -> Dict[str, Any]:
        """Create a new database connection"""
        try:
            payload = {
                "database_name": name,
                "sqlalchemy_uri": sqlalchemy_uri,
                "driver": driver,
                "cache_timeout": 3600,
            }

            response = requests.post(
                f"{self.base_url}/api/v1/databases",
                headers=self.headers,
                json=payload,
            )
            response.raise_for_status()

            database = response.json()
            database_id = database.get("id")
            print(f"✓ Database created: {name} (ID: {database_id})")
            return database
        except requests.exceptions.RequestException as e:
            print(f"✗ Failed to create database: {e}")
            return {}

    def test_database_connection(self, sqlalchemy_uri: str) -> bool:
        """Test database connection without creating it"""
        try:
            payload = {"sqlalchemy_uri": sqlalchemy_uri}

            response = requests.post(
                f"{self.base_url}/api/v1/databases/test_connection",
                headers=self.headers,
                json=payload,
            )
            response.raise_for_status()

            print("✓ Database connection successful")
            return True
        except requests.exceptions.RequestException as e:
            print(f"✗ Database connection failed: {e}")
            return False

    def create_dataset(
        self, database_id: int, schema: str, table_name: str
    ) -> Dict[str, Any]:
        """Create a dataset from a table"""
        try:
            payload = {
                "database_id": database_id,
                "schema": schema,
                "table_name": table_name,
                "owner_ids": [1],  # Assuming admin user ID is 1
            }

            response = requests.post(
                f"{self.base_url}/api/v1/datasets",
                headers=self.headers,
                json=payload,
            )
            response.raise_for_status()

            dataset = response.json()
            dataset_id = dataset.get("id")
            print(f"✓ Dataset created: {table_name} (ID: {dataset_id})")
            return dataset
        except requests.exceptions.RequestException as e:
            print(f"✗ Failed to create dataset: {e}")
            return {}

    def configure_columns(
        self, dataset_id: int, columns: list
    ) -> Dict[str, Any]:
        """Configure column properties (temporal, filterable, etc.)"""
        try:
            payload = {"columns": columns}

            response = requests.put(
                f"{self.base_url}/api/v1/datasets/{dataset_id}",
                headers=self.headers,
                json=payload,
            )
            response.raise_for_status()

            print(f"✓ Columns configured for dataset {dataset_id}")
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"✗ Failed to configure columns: {e}")
            return {}

    def create_chart(
        self,
        dataset_id: int,
        chart_title: str,
        visualization_type: str,
        query_context: dict,
    ) -> Dict[str, Any]:
        """Create a chart"""
        try:
            payload = {
                "dataset_id": dataset_id,
                "chart_title": chart_title,
                "visualization_type": visualization_type,
                "query_context": query_context,
            }

            response = requests.post(
                f"{self.base_url}/api/v1/charts",
                headers=self.headers,
                json=payload,
            )
            response.raise_for_status()

            chart = response.json()
            chart_id = chart.get("id")
            print(f"✓ Chart created: {chart_title} (ID: {chart_id})")
            return chart
        except requests.exceptions.RequestException as e:
            print(f"✗ Failed to create chart: {e}")
            return {}

    def create_dashboard(
        self, title: str, description: str = ""
    ) -> Dict[str, Any]:
        """Create a new dashboard"""
        try:
            payload = {
                "dashboard_title": title,
                "description": description,
                "dashboard_layout_version": "GRID_LAYOUT_v1",
            }

            response = requests.post(
                f"{self.base_url}/api/v1/dashboards",
                headers=self.headers,
                json=payload,
            )
            response.raise_for_status()

            dashboard = response.json()
            dashboard_id = dashboard.get("id")
            print(f"✓ Dashboard created: {title} (ID: {dashboard_id})")
            return dashboard
        except requests.exceptions.RequestException as e:
            print(f"✗ Failed to create dashboard: {e}")
            return {}

    def add_chart_to_dashboard(
        self, dashboard_id: int, chart_id: int, position: dict
    ) -> Dict[str, Any]:
        """Add a chart to a dashboard"""
        try:
            # Get current dashboard to preserve existing layout
            response = requests.get(
                f"{self.base_url}/api/v1/dashboards/{dashboard_id}",
                headers=self.headers,
            )
            response.raise_for_status()
            current_dashboard = response.json()

            # Prepare layout with new chart
            dashboard_layout = current_dashboard.get("dashboard_layout", {})
            if "GRID_ID" not in dashboard_layout:
                dashboard_layout["GRID_ID"] = {"GRID_DATA": {}}

            # Add chart to position
            grid_id = str(position.get("grid_id", 0))
            dashboard_layout["GRID_ID"]["GRID_DATA"][grid_id] = {
                "meta": {
                    "chartId": chart_id,
                    "height": position.get("height", 50),
                    "width": position.get("width", 6),
                    "sliceName": position.get("name", f"Chart {chart_id}"),
                }
            }

            # Update dashboard with new chart
            update_payload = {"dashboard_layout": dashboard_layout}

            response = requests.put(
                f"{self.base_url}/api/v1/dashboards/{dashboard_id}",
                headers=self.headers,
                json=update_payload,
            )
            response.raise_for_status()

            print(f"✓ Chart {chart_id} added to dashboard {dashboard_id}")
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"✗ Failed to add chart to dashboard: {e}")
            return {}

    def publish_dashboard(self, dashboard_id: int) -> bool:
        """Publish a dashboard (make it live)"""
        try:
            payload = {"published": True}

            response = requests.put(
                f"{self.base_url}/api/v1/dashboards/{dashboard_id}",
                headers=self.headers,
                json=payload,
            )
            response.raise_for_status()

            print(f"✓ Dashboard {dashboard_id} published")
            return True
        except requests.exceptions.RequestException as e:
            print(f"✗ Failed to publish dashboard: {e}")
            return False


def main():
    """Example workflow: Create database, dataset, chart, and dashboard"""

    # Initialize client
    client = SupersetClient(SUPERSET_URL, USERNAME, PASSWORD)

    # Step 1: Authenticate
    print("\n=== Step 1: Authentication ===")
    if not client.authenticate():
        return

    # Step 2: List existing databases
    print("\n=== Step 2: List Databases ===")
    databases = client.list_databases()

    # Step 3: Create database (example - comment out if using existing)
    print("\n=== Step 3: Create Database ===")
    # Uncomment to create a new database:
    # db = client.create_database(
    #     name="My Test Database",
    #     sqlalchemy_uri="sqlite:////tmp/test.db"
    # )
    # database_id = db.get('id')

    # Use first database if available
    if databases:
        database_id = databases[0]["id"]
        print(f"Using database ID: {database_id}")
    else:
        print("No databases available. Please create one first.")
        return

    # Step 4: Create dataset
    print("\n=== Step 4: Create Dataset ===")
    dataset = client.create_dataset(
        database_id=database_id, schema="main", table_name="orders"  # Adjust table name
    )

    if not dataset:
        print("Failed to create dataset. Exiting.")
        return

    dataset_id = dataset.get("id")

    # Step 5: Configure columns
    print("\n=== Step 5: Configure Columns ===")
    columns = [
        {
            "column_name": "order_date",
            "is_dttm": True,
            "python_date_format": "%Y-%m-%d",
        },
        {"column_name": "customer_id", "filterable": True},
        {"column_name": "product_category", "groupby": True},
    ]
    client.configure_columns(dataset_id, columns)

    # Step 6: Create chart
    print("\n=== Step 6: Create Chart ===")
    query_context = {
        "datasource": {"id": dataset_id, "type": "table"},
        "form_data": {
            "granularity_sqla": "order_date",
            "time_range": "Last year",
            "metrics": [{"label": "count"}],
            "groupby": ["product_category"],
        },
    }

    chart = client.create_chart(
        dataset_id=dataset_id,
        chart_title="Orders by Category",
        visualization_type="bar",
        query_context=query_context,
    )

    if not chart:
        print("Failed to create chart. Exiting.")
        return

    chart_id = chart.get("id")

    # Step 7: Create dashboard
    print("\n=== Step 7: Create Dashboard ===")
    dashboard = client.create_dashboard(
        title="Sales Overview", description="Dashboard for sales metrics"
    )

    if not dashboard:
        print("Failed to create dashboard. Exiting.")
        return

    dashboard_id = dashboard.get("id")

    # Step 8: Add chart to dashboard
    print("\n=== Step 8: Add Chart to Dashboard ===")
    client.add_chart_to_dashboard(
        dashboard_id=dashboard_id,
        chart_id=chart_id,
        position={"grid_id": 0, "height": 50, "width": 12},
    )

    # Step 9: Publish dashboard
    print("\n=== Step 9: Publish Dashboard ===")
    client.publish_dashboard(dashboard_id)

    print(
        f"\n✓ Complete! Dashboard available at: {SUPERSET_URL}/dashboard/{dashboard_id}"
    )


if __name__ == "__main__":
    main()
