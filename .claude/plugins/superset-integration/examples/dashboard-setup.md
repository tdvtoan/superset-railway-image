# Complete Dashboard Setup Example

This example walks through creating a complete sales analytics dashboard in Superset from start to finish.

## Scenario

Build a "Sales Analytics Dashboard" for a retail company with:
- Sales trends over time
- Sales by product category
- Sales by region
- Top customers

Data is stored in a PostgreSQL database with a `sales` table containing:
- `order_id`, `order_date`, `amount`, `product_category`, `region`, `customer_name`, `customer_id`

## Complete Walkthrough

### Phase 1: Setup Data Connection

#### 1.1 Connect to Database

1. Open Superset at `http://localhost:8088`
2. Click **+ Data** menu → **Connect Database**
3. Select **PostgreSQL** from the list
4. Fill in connection details:
   ```
   Host: prod-db.company.com
   Port: 5432
   User: analytics
   Password: ••••••••
   Database: sales_db
   Display Name: Production Sales DB
   ```
5. Click **Test Connection** → Should see "Connection worked!"
6. Click **Connect** to save

#### 1.2 Verify Connection

- Go to **Data** → **Databases**
- You should see "Production Sales DB" listed
- Click the database name to verify tables are visible

### Phase 2: Register Dataset

#### 2.1 Create Dataset from Table

1. Click **+ Data** → **Create Dataset**
2. Select database: **Production Sales DB**
3. Select schema: **public**
4. Select table: **sales**
5. Click **Create Dataset**

**Result:** Dataset "sales" created with all columns auto-detected

#### 2.2 Configure Column Properties

1. Click on **sales** dataset to edit
2. Go to **Columns** tab
3. Configure each column:

   **order_date**
   - Toggle **Temporal Column**: ON
   - Set **Python Date Format**: `%Y-%m-%d %H:%M:%S`
   - This enables time-series analysis

   **product_category**
   - Toggle **Filterable**: ON
   - Toggle **Groupby**: ON
   - Allows grouping and filtering by category

   **region**
   - Toggle **Filterable**: ON
   - Toggle **Groupby**: ON
   - For regional breakdowns

   **customer_name**
   - Toggle **Filterable**: ON
   - For customer-level filtering

   **amount**
   - Keep as numeric (default)
   - Used for sum/average calculations

4. Click **Save Dataset**

### Phase 3: Create Visualizations

#### 3.1 Chart 1: Sales Trend Over Time

1. Click on **sales** dataset
2. **Explore** interface opens
3. **Select Visualization**: Line Chart
4. **Configure Query**:
   - Metrics: `SUM(amount)` → rename to "Total Sales"
   - Granularity: `order_date` with `Monthly` bucketing
   - Time Range: `Last 2 years`
5. **Customize** (right panel):
   - Title: "Sales Trend (Monthly)"
   - X-axis label: "Month"
   - Y-axis label: "Sales Amount ($)"
6. Click **Run** to preview
7. Click **Save**
   - Save to a **New Dashboard** named "Sales Analytics"

**Result:** Chart saved and dashboard created

#### 3.2 Chart 2: Sales by Product Category

1. Click on **sales** dataset
2. **Explore** interface opens
3. **Select Visualization**: Bar Chart
4. **Configure Query**:
   - Metrics: `SUM(amount)`
   - Groupby: `product_category`
   - Sort by: Metric descending (highest sales first)
5. **Customize**:
   - Title: "Sales by Category"
   - Color scheme: Use a colorblind-friendly palette
6. Click **Run** to preview
7. Click **Save**
   - Save to existing dashboard: **Sales Analytics**

**Result:** New chart added to Sales Analytics dashboard

#### 3.3 Chart 3: Sales by Region

1. Click on **sales** dataset
2. **Explore** interface opens
3. **Select Visualization**: Pie Chart
4. **Configure Query**:
   - Metrics: `SUM(amount)`
   - Groupby: `region`
5. **Customize**:
   - Title: "Sales Distribution by Region"
   - Show legend: ON
6. Click **Run** to preview
7. Click **Save**
   - Save to existing dashboard: **Sales Analytics**

#### 3.4 Chart 4: Top 10 Customers

1. Click on **sales** dataset
2. **Explore** interface opens
3. **Select Visualization**: Data Table
4. **Configure Query**:
   - Groupby: `customer_name`
   - Metrics: `SUM(amount)`, `COUNT(order_id)`
   - Sort by: Sum of amount (descending)
   - Limit: 10 rows
5. **Customize**:
   - Title: "Top 10 Customers by Sales"
   - Column names: Make readable
6. Click **Run** to preview
7. Click **Save**
   - Save to existing dashboard: **Sales Analytics**

### Phase 4: Arrange Dashboard Layout

#### 4.1 Edit Dashboard Layout

1. Go to **Dashboards** → Click **Sales Analytics**
2. Click **Edit Dashboard** button (top right)
3. Dashboard enters edit mode
4. Arrange charts:

   **Row 1: Main KPI**
   - Sales Trend (Monthly) - spans full width (12 columns)
   - Height: Medium (50px)

   **Row 2: Comparisons**
   - Sales by Category - left side (6 columns)
   - Sales Distribution by Region - right side (6 columns)
   - Height: Medium (50px each)

   **Row 3: Details**
   - Top 10 Customers - full width (12 columns)
   - Height: Large (100px)

5. Drag charts to desired positions
6. Resize by dragging corners

**Layout Grid:**
```
┌─────────────────────────────────┐
│  Sales Trend (12 cols)          │
├──────────────┬──────────────────┤
│ Sales by Cat │ Sales by Region  │
│  (6 cols)    │   (6 cols)       │
├─────────────────────────────────┤
│  Top 10 Customers (12 cols)     │
└─────────────────────────────────┘
```

#### 4.2 Add Filters

1. Click **+ Add Filter**
2. Create filter for **Product Category**:
   - Select "product_category" column
   - Filter Type: Dropdown
   - Name: "Product Category"
   - Apply to: All charts
3. Click **Add Filter**
4. Create filter for **Date Range**:
   - Select "order_date" column
   - Filter Type: Date Range
   - Name: "Date Range"
   - Apply to: All charts

**Result:** Filters appear at top of dashboard and control all charts

#### 4.3 Save Layout

1. Click **Save** button (top right)
2. Dashboard layout is preserved

### Phase 5: Publish Dashboard

#### 5.1 Publish

1. Look for **Draft** label on dashboard
2. Click **Draft** to toggle
3. Button changes to **Published**
4. Dashboard is now live and visible to others

#### 5.2 Share Dashboard

**URL Sharing:**
```
http://localhost:8088/dashboard/1  (assuming dashboard ID is 1)
```

**Send to team:**
- Share URL in Slack/email
- Users can now access and interact with dashboard
- All filters work for exploration

### Phase 6: Monitor and Refine

#### 6.1 Add Dashboard Title and Description

1. Click dashboard title "Sales Analytics"
2. Edit description:
   ```
   Sales Analytics Dashboard

   This dashboard provides real-time visibility into sales metrics:
   - Monthly sales trends
   - Sales by product category
   - Geographic distribution
   - Top customers

   Data updates daily at 2 AM UTC.
   Questions? Contact analytics-team@company.com
   ```
3. Click Save

#### 6.2 Adjust Time Defaults

1. Edit dashboard (if needed)
2. Chart configs can have default time ranges
3. Example: Set "Sales Trend" to default to "Last 12 months"
4. Save changes

### Phase 7: Advanced Features (Optional)

#### Enable Scheduled Email Reports

1. Go to dashboards list
2. Click **menu** on Sales Analytics
3. Select **Schedule email**
4. Configure:
   - Recipients: team@company.com
   - Frequency: Weekly on Monday 8 AM
   - Include: All visualizations
5. Save

**Result:** Dashboard emailed weekly to team

#### Set Up Alert on Sales Metric

1. Go to Sales Trend chart
2. Click **menu** → **Set up alert**
3. Configure:
   - Alert if: Total Sales < $50,000
   - Frequency: Check daily
   - Notify: team@company.com
4. Save

**Result:** Alert sent if sales dip below threshold

## Final Dashboard

After completing all steps:

- ✓ Database connected and verified
- ✓ Dataset registered with configured columns
- ✓ 4 visualizations created and working
- ✓ Dashboard layout arranged professionally
- ✓ Filters added for exploration
- ✓ Dashboard published and live
- ✓ Team can access and interact with dashboard
- ✓ Automated email reports configured (optional)
- ✓ Alerts set up for monitoring (optional)

## Troubleshooting

### Charts show "No Data"
- Verify date range includes actual data
- Check filters aren't excluding all records
- Query the database directly to confirm data exists

### Filters not working
- Verify column is marked "Filterable" in dataset
- Check chart has compatible groupby dimension
- Ensure data types match

### Dashboard loads slowly
- Reduce number of charts
- Limit data with narrow time ranges
- Cache frequently accessed queries

## Next Steps

1. Monitor dashboard usage
2. Gather user feedback
3. Create additional dashboards for other departments
4. Explore advanced visualizations (maps, heatmaps, etc.)
5. Set up row-level security if sensitive data

## Dashboard Best Practices Applied

✓ Clear, descriptive titles
✓ Logical chart arrangement
✓ Interactive filters for exploration
✓ Time-series prominent for trends
✓ Supporting detailed data table
✓ Responsive to different screen sizes
✓ Published and shareable
✓ Documented with description
