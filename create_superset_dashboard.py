#!/usr/bin/env python3
"""
Create Log Event Dashboard in Superset

This script creates a complete dashboard for analyzing log events from the peter_log_event table.

Prerequisites:
- Superset instance running at: https://superset-railway-image-production-6d86.up.railway.app
- Database connection "supabase staging" already configured
- pip install requests python-dotenv

Usage:
python create_superset_dashboard.py
"""

import requests
import json
import os
from dotenv import load_dotenv
from typing import Dict, Any, Optional

# Load environment variables
load_dotenv(".env.local")

# Configuration
SUPERSET_URL = "https://superset-railway-image-production-6d86.up.railway.app"
SUPERSET_USERNAME = os.getenv("SUPERSET_USERNAME", "admin")
SUPERSET_PASSWORD = os.getenv("SUPERSET_PASSWORD", "#Stayahead88")
DATABASE_NAME = "supabase staging"
SCHEMA = "public"
TABLE_NAME = "peter_log_event"


class SupersetClient:
    """Client for Superset API operations"""

    def __init__(self, base_url: str, username: str, password: str):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.token = None
        self.headers = {}
        self.session = requests.Session()

    def authenticate(self) -> bool:
        """Authenticate and obtain JWT token"""
        try:
            # Disable SSL warnings for self-signed certs
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

            response = self.session.post(
                f"{self.base_url}/api/v1/security/login",
                json={
                    "username": self.username,
                    "password": self.password,
                    "provider": "db"  # Required by Flask-AppBuilder
                },
                verify=False,  # For Railway SSL issues
                timeout=10,
                allow_redirects=False,
            )

            # Check for various success codes
            if response.status_code not in [200, 201, 400, 401, 422]:
                print(f"Status code: {response.status_code}")
                print(f"Response text: {response.text[:500]}")

            response.raise_for_status()

            data = response.json()
            self.token = data.get("access_token")
            if not self.token:
                print(f"✗ No access token in response: {data}")
                return False

            self.headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
            }

            print("✓ Authentication successful")
            return True
        except requests.exceptions.RequestException as e:
            print(f"✗ Authentication failed: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response status: {e.response.status_code}")
                print(f"Response text: {e.response.text[:500]}")
            return False

    def get_database_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Get database ID by name"""
        try:
            response = self.session.get(
                f"{self.base_url}/api/v1/databases",
                headers=self.headers,
                verify=False,
            )
            response.raise_for_status()

            databases = response.json().get("result", [])
            for db in databases:
                if db.get("database_name") == name:
                    print(f"✓ Found database: {name} (ID: {db.get('id')})")
                    return db

            print(f"✗ Database '{name}' not found")
            print(f"Available databases: {[db.get('database_name') for db in databases]}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"✗ Failed to get databases: {e}")
            return None

    def create_dataset(
        self, database_id: int, schema: str, table_name: str
    ) -> Optional[Dict[str, Any]]:
        """Create dataset from table"""
        try:
            payload = {
                "database_id": database_id,
                "schema": schema,
                "table_name": table_name,
            }

            response = self.session.post(
                f"{self.base_url}/api/v1/datasets",
                headers=self.headers,
                json=payload,
                verify=False,
            )
            response.raise_for_status()

            dataset = response.json()
            dataset_id = dataset.get("id")
            print(f"✓ Dataset created: {table_name} (ID: {dataset_id})")
            return dataset
        except requests.exceptions.RequestException as e:
            print(f"✗ Failed to create dataset: {e}")
            return None

    def configure_columns(
        self, dataset_id: int, columns: list
    ) -> bool:
        """Configure column properties"""
        try:
            payload = {"columns": columns}

            response = self.session.put(
                f"{self.base_url}/api/v1/datasets/{dataset_id}",
                headers=self.headers,
                json=payload,
                verify=False,
            )
            response.raise_for_status()

            print(f"✓ Columns configured for dataset {dataset_id}")
            return True
        except requests.exceptions.RequestException as e:
            print(f"✗ Failed to configure columns: {e}")
            return False

    def create_chart(
        self,
        dataset_id: int,
        chart_title: str,
        visualization_type: str,
        query_context: dict,
    ) -> Optional[Dict[str, Any]]:
        """Create chart"""
        try:
            payload = {
                "dataset_id": dataset_id,
                "chart_title": chart_title,
                "visualization_type": visualization_type,
                "query_context": query_context,
            }

            response = self.session.post(
                f"{self.base_url}/api/v1/charts",
                headers=self.headers,
                json=payload,
                verify=False,
            )
            response.raise_for_status()

            chart = response.json()
            chart_id = chart.get("id")
            print(f"✓ Chart created: {chart_title} (ID: {chart_id})")
            return chart
        except requests.exceptions.RequestException as e:
            print(f"✗ Failed to create chart: {e}")
            print(f"Response: {e.response.text if hasattr(e, 'response') else 'N/A'}")
            return None

    def create_dashboard(
        self, title: str, description: str = ""
    ) -> Optional[Dict[str, Any]]:
        """Create dashboard"""
        try:
            payload = {
                "dashboard_title": title,
                "description": description,
                "dashboard_layout_version": "GRID_LAYOUT_v1",
            }

            response = self.session.post(
                f"{self.base_url}/api/v1/dashboards",
                headers=self.headers,
                json=payload,
                verify=False,
            )
            response.raise_for_status()

            dashboard = response.json()
            dashboard_id = dashboard.get("id")
            print(f"✓ Dashboard created: {title} (ID: {dashboard_id})")
            return dashboard
        except requests.exceptions.RequestException as e:
            print(f"✗ Failed to create dashboard: {e}")
            return None

    def add_charts_to_dashboard(
        self, dashboard_id: int, chart_configs: list
    ) -> bool:
        """Add multiple charts to dashboard with positions"""
        try:
            dashboard_layout = {
                "GRID_ID": {
                    "GRID_DATA": {}
                }
            }

            for config in chart_configs:
                grid_id = str(config["grid_id"])
                dashboard_layout["GRID_ID"]["GRID_DATA"][grid_id] = {
                    "meta": {
                        "chartId": config["chart_id"],
                        "height": config["height"],
                        "width": config["width"],
                        "sliceName": config["name"],
                    }
                }

            payload = {"dashboard_layout": dashboard_layout}

            response = self.session.put(
                f"{self.base_url}/api/v1/dashboards/{dashboard_id}",
                headers=self.headers,
                json=payload,
                verify=False,
            )
            response.raise_for_status()

            print(f"✓ Charts added to dashboard {dashboard_id}")
            return True
        except requests.exceptions.RequestException as e:
            print(f"✗ Failed to add charts to dashboard: {e}")
            return False

    def publish_dashboard(self, dashboard_id: int) -> bool:
        """Publish dashboard"""
        try:
            payload = {"published": True}

            response = self.session.put(
                f"{self.base_url}/api/v1/dashboards/{dashboard_id}",
                headers=self.headers,
                json=payload,
                verify=False,
            )
            response.raise_for_status()

            print(f"✓ Dashboard {dashboard_id} published")
            return True
        except requests.exceptions.RequestException as e:
            print(f"✗ Failed to publish dashboard: {e}")
            return False


def main():
    """Create complete log event dashboard"""

    print("\n" + "=" * 60)
    print("Creating Log Event Dashboard in Superset")
    print("=" * 60 + "\n")

    # Initialize client
    client = SupersetClient(SUPERSET_URL, SUPERSET_USERNAME, SUPERSET_PASSWORD)

    # Step 1: Authenticate
    print("[1/7] Authenticating...")
    if not client.authenticate():
        print("Failed to authenticate. Exiting.")
        return

    # Step 2: Find database
    print("\n[2/7] Finding database...")
    database = client.get_database_by_name(DATABASE_NAME)
    if not database:
        print("Failed to find database. Exiting.")
        return

    database_id = database.get("id")

    # Step 3: Create dataset
    print("\n[3/7] Creating dataset...")
    dataset = client.create_dataset(database_id, SCHEMA, TABLE_NAME)
    if not dataset:
        print("Failed to create dataset. Exiting.")
        return

    dataset_id = dataset.get("id")

    # Step 4: Configure columns
    print("\n[4/7] Configuring columns...")
    columns = [
        {
            "column_name": "created_at",
            "is_dttm": True,
            "python_date_format": "%Y-%m-%d %H:%M:%S.%f",
        },
        {"column_name": "event_type", "filterable": True, "groupby": True},
        {"column_name": "user_id", "filterable": True, "groupby": True},
        {"column_name": "session_id", "filterable": True},
    ]

    client.configure_columns(dataset_id, columns)

    # Step 5: Create charts
    print("\n[5/7] Creating charts...")
    charts = []

    # Chart 1: Events over time
    chart1 = client.create_chart(
        dataset_id=dataset_id,
        chart_title="Log Events Timeline",
        visualization_type="line",
        query_context={
            "datasource": {"id": dataset_id, "type": "table"},
            "form_data": {
                "granularity_sqla": "created_at",
                "time_range": "Last 7 days",
                "metrics": [{"label": "count"}],
                "datasource_name": TABLE_NAME,
            },
        },
    )
    if chart1:
        charts.append(chart1)

    # Chart 2: Events by type
    chart2 = client.create_chart(
        dataset_id=dataset_id,
        chart_title="Events by Type",
        visualization_type="bar",
        query_context={
            "datasource": {"id": dataset_id, "type": "table"},
            "form_data": {
                "metrics": [{"label": "count"}],
                "groupby": ["event_type"],
                "datasource_name": TABLE_NAME,
            },
        },
    )
    if chart2:
        charts.append(chart2)

    # Chart 3: Events by user
    chart3 = client.create_chart(
        dataset_id=dataset_id,
        chart_title="Top Users by Events",
        visualization_type="horizontal_bar",
        query_context={
            "datasource": {"id": dataset_id, "type": "table"},
            "form_data": {
                "metrics": [{"label": "count"}],
                "groupby": ["user_id"],
                "row_limit": 10,
                "datasource_name": TABLE_NAME,
            },
        },
    )
    if chart3:
        charts.append(chart3)

    # Chart 4: Recent events table
    chart4 = client.create_chart(
        dataset_id=dataset_id,
        chart_title="Recent Events",
        visualization_type="table",
        query_context={
            "datasource": {"id": dataset_id, "type": "table"},
            "form_data": {
                "datasource_name": TABLE_NAME,
                "row_limit": 100,
                "all_columns": [
                    "created_at",
                    "event_type",
                    "user_id",
                    "session_id",
                ],
            },
        },
    )
    if chart4:
        charts.append(chart4)

    if not charts:
        print("Failed to create charts. Exiting.")
        return

    print(f"✓ Created {len(charts)} charts")

    # Step 6: Create dashboard
    print("\n[6/7] Creating dashboard...")
    dashboard = client.create_dashboard(
        title="Log Events Dashboard",
        description="Real-time analysis of application log events from peter_log_event table",
    )
    if not dashboard:
        print("Failed to create dashboard. Exiting.")
        return

    dashboard_id = dashboard.get("id")

    # Step 7: Add charts to dashboard and publish
    print("\n[7/7] Adding charts to dashboard...")
    chart_configs = [
        {
            "grid_id": 0,
            "chart_id": charts[0].get("id"),
            "height": 50,
            "width": 12,
            "name": "Log Events Timeline",
        },
        {
            "grid_id": 1,
            "chart_id": charts[1].get("id"),
            "height": 50,
            "width": 6,
            "name": "Events by Type",
        },
        {
            "grid_id": 2,
            "chart_id": charts[2].get("id"),
            "height": 50,
            "width": 6,
            "name": "Top Users",
        },
        {
            "grid_id": 3,
            "chart_id": charts[3].get("id"),
            "height": 100,
            "width": 12,
            "name": "Recent Events",
        },
    ]

    if client.add_charts_to_dashboard(dashboard_id, chart_configs):
        client.publish_dashboard(dashboard_id)

    # Summary
    print("\n" + "=" * 60)
    print("✓ Dashboard Created Successfully!")
    print("=" * 60)
    print(f"\nDashboard URL:")
    print(
        f"{SUPERSET_URL}/dashboard/{dashboard_id}"
    )
    print(f"\nDashboard Name: Log Events Dashboard")
    print(f"Dashboard ID: {dashboard_id}")
    print(f"Table: {SCHEMA}.{TABLE_NAME}")
    print(f"Database: {DATABASE_NAME}")
    print(f"\nCharts created:")
    for i, chart in enumerate(charts, 1):
        print(f"  {i}. {chart.get('chart_title')} (ID: {chart.get('id')})")
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
