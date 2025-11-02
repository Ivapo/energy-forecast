## 📊 Epic 2: Data Exploration & Analysis Tasks

### **Task 1: Data Quality Assessment.**

Load processed data and examine basic statistics, data quality, and temporal coverage

### **Task 2: Temporal Pattern Visualization**

Create time series plots to visualize electricity demand patterns over different time periods (daily, weekly, monthly, yearly)

### **Task 3: Seasonality & Trend Analysis**

Analyze seasonal patterns and trends using decomposition techniques to identify underlying components

`seasonal_decompose` separates your time series into distinct, interpretable components, by using either **additive** or **multiplicative** models:
  - **Additive**: `Observed = Trend + Seasonal + Residual` (what we're using)
  - **Multiplicative**: `Observed = Trend × Seasonal × Residual`

**where,**

**📈 `Observed`**: The oringal time series

**📊 `Trend` Component**: 
   - The long-term direction of electricity demand over time
   - Shows whether demand is generally increasing, decreasing, or stable
   - Removes short-term fluctuations to reveal the underlying trajectory
   - *Inisght Example*: Sweden's electricity demand might show an upward trend due to economic growth

**🌡️ `Seasonal` Component**: 
   - Regular, predictable patterns that repeat over fixed periods (yearly cycles)
   - Captures recurring variations like winter heating vs summer cooling
   - Always has the same pattern each year (high in winter, low in summer)
   - *Inisght Example*: Higher demand in December-February, lower in June-August

**🎲 `Residual` Component** (also called "Irregular" or "Noise"):
   - What's left after removing trend and seasonal patterns
   - Captures unexpected events, random variations, and model errors
   - Should look like random noise if decomposition worked well
   - *Inisght Example*: Unusual demand spikes during heat waves, economic disruptions, etc.

**Why is this useful for forecasting?**
- **Trend**: Helps predict long-term demand growth/decline
- **Seasonal**: Enables accurate seasonal adjustments in forecasts
- **Residuals**: Shows forecast uncertainty and identifies outliers

**🤔 Additive vs Multiplicative Decomposition**

**The Key Difference:**
- **Additive**: `Observed = Trend + Seasonal + Residual`
  - Seasonal variations are **constant in magnitude** over time
  - Example: Always ±4,000 MW seasonal swing regardless of baseline demand level

- **Multiplicative**: `Observed = Trend × Seasonal × Residual`  
  - Seasonal variations **scale with the trend** level
  - Example: Seasonal swing grows from ±10% to ±15% as baseline demand increases

**How to Choose:**
1. **Plot your data** - Look at seasonal patterns over time
2. **Constant amplitude** → Use Additive
3. **Growing/shrinking amplitude** → Use Multiplicative
4. **Statistical test** - Compare model residuals (lower variance = better fit)

**For Electricity Demand:**
- Sweden's seasonal patterns are driven by **heating/cooling needs**
- Winter heating demand is roughly the same absolute MW regardless of economic growth
- Physical infrastructure limits create relatively stable seasonal swings
- **Result**: Additive model is typically more appropriate for electricity demand


### **Task 4: Daily/Weekly Cycle Analysis**

Examine daily and weekly patterns to understand business vs weekend demand cycles

**Task 5: Anomaly Detection & Analysis**

Identify and analyze anomalies, outliers, and unusual demand events in the time series

**Task 6: Forecast vs Actual Analysis**

Compare actual demand vs forecast to understand baseline prediction accuracy and identify systematic biases

**Task 7: Statistical Properties Analysis**

Analyze statistical properties like stationarity, autocorrelation, and distribution characteristics

**Task 8: Generate EDA Insights Summary**

Create summary insights and identify key patterns that will inform feature engineering decisions