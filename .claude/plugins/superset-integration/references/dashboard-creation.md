# Creating Your First Dashboard in Superset

This guide walks through the complete process of creating a dashboard in Superset using the web interface.

## Prerequisites

- Access to a running Superset instance
- Basic understanding of your data sources
- Admin or user permissions to create dashboards

## Step-by-Step Guide

### Step 1: Connect to a Database

**Objective:** Register a new database connection with Superset.

**Process:**

1. Click the **`+`** menu (top right) and select **Data**
2. Click **Connect Database**
3. Select your database type from the dropdown:
   - PostgreSQL
   - MySQL
   - SQLite
   - Oracle
   - Redshift
   - Snowflake
   - BigQuery
   - And many others

4. Fill in connection details:
   - **Host**: Database server address (e.g., `localhost`)
   - **Port**: Database port (e.g., `5432` for PostgreSQL)
   - **Username**: Database user
   - **Password**: User password
   - **Database**: Database name

5. Click **Test Connection** to verify credentials work

6. If successful, click **Connect**

**What happens next:**
- Superset connects to your database
- Database appears in the data sources list
- Tables become available for dataset registration

### Step 2: Register a Table as a Dataset

**Objective:** Import a table from your database as a Superset dataset.

**Process:**

1. Click the **`+`** menu and select **Data**
2. Click **Create Dataset** (or **`+ Dataset`**)
3. Select your database from the dropdown
4. Choose the schema from the second dropdown
5. Select the table name from the third dropdown
6. Click **Create Dataset**

**What gets created:**
- A dataset linking to the table
- Column metadata automatically populated
- Available for chart creation

### Step 3: Configure Column Properties

**Objective:** Define how columns behave in charts and filters.

**Process:**

1. Click on your dataset name to edit it
2. Navigate to the **Columns** tab
3. For each column, configure:

   **Datetime Columns:**
   - Toggle **Temporal Column** if this is a date/time field
   - Set **Python Date Format** if automatic parsing fails
   - Example format: `%Y-%m-%d %H:%M:%S`

   **Filterable Columns:**
   - Toggle **Filterable** to make available in dashboard filters
   - Users can filter charts by these columns

   **Dimensional Columns:**
   - Toggle **Groupby** to allow grouping in charts
   - Used for breaking down metrics by categories

4. Click **Save** to apply changes

**Column Property Definitions:**

- **Temporal**: Marks column as time-based for time-series analyses
- **Filterable**: Makes column available in dashboard filter dropdowns
- **Groupby**: Allows this column for "group by" operations in charts
- **Count Distinct**: Can compute distinct count on this column
- **Sum/Min/Max**: Can aggregate these values

### Step 4: Create Charts Using the Explore Interface

**Objective:** Build visualizations from your dataset.

**Process:**

1. Click on your dataset name
2. The **Explore** interface opens
3. **Select Visualization Type** (left panel):
   - Scroll through chart types or search
   - Options include: Line, Bar, Pie, Scatter, Area, Table, Pivot Table, Map, Heatmap, etc.
4. **Configure Query** (middle panel):
   - **Metrics**: Aggregations to display (count, sum, average, etc.)
   - **Groupby**: Columns to group/dimension by
   - **Filters**: Add WHERE conditions
   - **Time Range**: Select date range if applicable
   - **Granularity**: For time series, set time bucketing (day, week, month, etc.)

5. **Preview Changes**:
   - Adjust settings and click **Run** to see results
   - Preview updates in real-time

6. **Customize Appearance** (right panel):
   - Chart title and description
   - Colors, formatting, axis labels
   - Legend and tooltip settings
   - Number formatting

7. Click **Save** to save the chart

### Step 5: Save and Add to Dashboard

**Objective:** Create or update a dashboard with your chart.

**Process:**

1. After creating a chart, click **Save**
2. Choose save option:
   - **Save & Add to Dashboard** - Add to existing or new dashboard
   - **Save & Go to Dashboard** - Save and view in dashboard context

3. If creating new dashboard:
   - Enter dashboard name
   - Click **Create New Dashboard**

4. If adding to existing:
   - Select dashboard from dropdown
   - Click **Save to Dashboard**

**What happens:**
- Chart is saved with a unique ID
- Chart is positioned in dashboard grid
- Ready for dashboard layout editing

### Step 6: Edit and Customize Dashboard Layout

**Objective:** Arrange charts and customize dashboard appearance.

**Process:**

1. Click **Edit Dashboard** (top right button)
2. Dashboard enters edit mode
3. **Resize Charts**:
   - Drag chart corners to resize
   - Charts snap to a 12-column grid

4. **Reposition Charts**:
   - Drag charts by header to move
   - Charts can be stacked or arranged side-by-side

5. **Add Filters**:
   - Click **Add Filter** in edit mode
   - Select column to filter by
   - Filter applies to all compatible charts

6. **Add Text or Links**:
   - Click **Add Tab** for multi-page dashboards
   - Add headers, instructions, or markdown text

7. Click **Save** to save layout changes

**Grid System:**
- Dashboard is 12 columns wide
- Each row is flexible height
- Charts flow and reflow with browser size

### Step 7: Publish and Manage Access

**Objective:** Make dashboard live and control who can see it.

**Process:**

1. Look for **Draft** button (top right)
2. Click **Draft** to toggle to **Published**
   - Dashboard is now accessible to others
   - Appears in dashboard lists

3. **Control Visibility**:
   - **Dataset Permissions**: Users can only see charts from datasets they have access to
   - **Dashboard Permissions** (if enabled): Restrict dashboard to specific roles
   - **Public Sharing**: Some Superset instances allow anonymous sharing links

4. Click dashboard title to customize:
   - Title and description
   - Owner
   - Tags for organization

## Common Chart Types and Their Uses

### Time Series / Line Chart
- **Best for**: Trends over time
- **Requires**: Temporal column and metric
- **Example**: Daily revenue over the past year

### Bar Chart
- **Best for**: Comparing values across categories
- **Requires**: Groupby column and metric
- **Example**: Sales by region

### Pie Chart
- **Best for**: Showing composition/proportions
- **Requires**: Groupby column and metric
- **Example**: Market share by company

### Scatter Plot
- **Best for**: Correlation between two metrics
- **Requires**: Two metrics on X and Y axes
- **Example**: Marketing spend vs revenue

### Data Table
- **Best for**: Detailed row-level data
- **Requires**: Columns to display
- **Example**: Customer list with details

### Pivot Table
- **Best for**: Multi-dimensional analysis
- **Requires**: Row/column dimensions and metrics
- **Example**: Sales by region and product category

### Map / Geospatial
- **Best for**: Geographic distribution
- **Requires**: Latitude/longitude or country columns
- **Example**: Sales locations by country

## Dashboard Best Practices

### Layout and Design
- Keep related charts together
- Use consistent visualization sizes
- Order visualizations by importance
- Leave adequate spacing for readability

### Performance
- Avoid overly complex dashboards (>10-15 charts)
- Use appropriate time ranges to limit data
- Cache frequently accessed data
- Set cache timeouts for updated data

### Interactivity
- Add filters for common drill-down dimensions
- Enable cross-filtering between charts (if available)
- Use clear filter labels
- Provide default filter values

### Data Accuracy
- Verify data is current
- Document data refresh frequency
- Note any limitations or calculations
- Include units (dollars, percentages, etc.)

### Accessibility
- Use descriptive chart titles
- Add descriptions explaining insights
- Use colors accessible to colorblind users
- Ensure text is readable at all sizes

## Troubleshooting Common Issues

### Chart Shows "No Data"
- Verify dataset has data for selected time range
- Check filters aren't excluding all records
- Ensure metric columns are numeric

### Slow Dashboard Performance
- Reduce number of charts
- Limit time range queried
- Simplify or remove heavy visualizations
- Check database query performance

### Missing Columns in Dataset
- Refresh dataset metadata
- Verify database connection still works
- Check user has permission to see columns

### Filter Not Working
- Verify column is marked "Filterable"
- Check filter value matches data values
- Ensure chart has compatible groupby dimension

### Permission Issues
- Contact Superset admin for dataset access
- Verify role has dashboard view permission
- Check row-level security (RLS) constraints

## Advanced Features

### Dashboard Parameters
- Create parameterized dashboards
- Pass values via URL parameters
- Dynamic filtering based on parameters

### Scheduled Emails
- Configure email delivery of dashboard
- Set schedule (daily, weekly, etc.)
- Include chart images and data

### Alerts
- Set alerts on metric thresholds
- Trigger notifications on conditions
- Monitor KPI metrics automatically

### Custom Visualizations
- Install third-party visualization plugins
- Create custom visualization code
- Extend Superset visualization library

## Next Steps

After creating your first dashboard:

1. Share dashboard with team members
2. Gather feedback on usefulness
3. Refine visualizations and layout
4. Create additional dashboards for other metrics
5. Explore advanced features (alerts, scheduling, etc.)

## Additional Resources

- [Superset Official Documentation](https://superset.apache.org)
- [Superset Chart Types Guide](https://superset.apache.org/docs/using-superset/creating-your-first-dashboard)
- Superset instance help: Click **Help** menu in Superset UI
