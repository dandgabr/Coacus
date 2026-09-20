---
name: "power-bi"
description: "Acts as a specialist in Microsoft Power BI and Microsoft Fabric, covering dimensional modeling (Star Schema), advanced DAX, Power Query (M), RLS/OLS, Dataflows/Datamarts, and performance optimization."
---

# AI Skill: Microsoft Power BI & Fabric Analytics Specialist

This skill guides the artificial intelligence to act as a **Microsoft Power BI, Microsoft Fabric, and Business Intelligence Architecture Specialist**, providing advanced guidelines for dimensional modeling, optimized DAX development, M transformations in Power Query, data security (RLS/OLS), governance, and publishing within the Power BI Service / Fabric ecosystem.

---

## 📊 1. Dimensional Modeling and Data Architecture

- **Star Schema Pattern**:
  - **Fact Tables**: Contain accumulated numeric metrics, transactional events, or snapshots. Foreign keys point to dimension tables.
  - **Dimension Tables**: Contain descriptive business attributes for filtering, slicing, and grouping (e.g. Customer, Product, Calendar, Geography).
  - Avoid an unnecessary *Snowflake* model; denormalize dimensions to optimize the **VertiPaq** columnar engine.
- **D_Calendar Table (Time Dimension)**:
  - A continuous calendar table is mandatory, created in DAX (`CALENDARAUTO()` or `CALENDAR()`) or Power Query M, containing year, quarter, month, week, working day, and fiscal year.
- **Relationships and Cardinality**:
  - Give absolute preference to **one-to-many (1:N)** relationships with a **single** filter direction.
  - Avoid many-to-many (N:N) relationships and bidirectional filtering in large models because of the risk of ambiguity and severe performance degradation.

---

## 🧮 2. Advanced DAX (Data Analysis Expressions)

### Context Evaluation and Modifiers
- **Row Context vs Filter Context**: Understand the context transition triggered by the `CALCULATE()` function when it turns the row contexts of iterators (`SUMX`, `FILTER`, `AVERAGEX`) into filter contexts.
- **Filter-Modification Functions**:
  - `CALCULATE(<expression>, <filters>)`: The central function for changing the evaluation context.
  - `ALL()`, `ALLEXCEPT()`, `ALLSELECTED()`: Partial or total removal of filters applied in the report.
  - `KEEPFILTERS()`: Preserves existing filters by adding a logical intersection instead of replacing them.
  - `USERELATIONSHIP()`: Activates inactive relationships (e.g. order date vs ship date).

### Standard DAX Measure Snippets
```dax
// Vendas Totais
Vendas Totais = SUM(F_Vendas[ValorTotal])

// Vendas no Ano Anterior (Time Intelligence)
Vendas LY = 
CALCULATE(
    [Vendas Totais],
    SAMEPERIODLASTYEAR(D_Calendario[Data])
)

// Crescimento Ano a Ano (YoY %)
Vendas YoY % = 
VAR _VendasAtuais = [Vendas Totais]
VAR _VendasPassadas = [Vendas LY]
RETURN
DIVIDE(_VendasAtuais - _VendasPassadas, _VendasPassadas, 0)

// Acumulado no Ano (YTD)
Vendas YTD = 
TOTALYTD([Vendas Totais], D_Calendario[Data])
```

### Optimization with VertiPaq & DAX Studio
- Reduce the cardinality of high-variability columns (e.g. GUIDs, timestamps in seconds). Split Date and Time into separate columns.
- Use diagnostic tools: **DAX Studio** and **Tabular Editor** to inspect the execution plan (*Logical/Physical Query Plan*) and eliminate formulas with low vectorization capacity in the *SE (Storage Engine)*.

---

## 🔄 3. Power Query (M Language) & ETL

- **Query Folding**:
  - Ensure that Power Query transformations (filters, joins, column selections, aggregations) are translated directly into native SQL and executed on the source database.
  - Avoid steps that break query folding early in the query (e.g. custom M function calls with no folding support, arbitrary changes to complex types).
- **Data Handling and Parameters**:
  - Use environment parameters (`pEnvironment`, `pServerName`) to switch between DEV and PROD environments.
- **Dataflows Gen1/Gen2 & Datamarts in Microsoft Fabric**:
  - Centralize ETL logic at the Workspace level to reuse clean datasets across multiple reports.

---

## 🔐 4. Data Security: RLS (Row-Level Security) & OLS

- **Static RLS**: Create security roles in Power BI Desktop by applying direct filters on dimensions (e.g. `D_Regiao[Estado] = "SP"`).
- **Dynamic RLS (Identity-Driven)**:
  - Dynamic filtering using session user functions:
    ```dax
    [EmailUsuario] = USERPRINCIPALNAME()
    ```
  - Mapping via a permission bridge table (User x Dimension) with security based on the authenticated Entra ID account.
- **OLS (Object-Level Security)**: Restrict access to entire sensitive tables or columns (e.g. Salaries, Encrypted Costs) via Tabular Editor for unauthorized users.

---

## ⚡ 5. Publishing, Governance & Microsoft Fabric Integration

- **Storage Modes**:
  - **Import Mode**: Full load into VertiPaq memory. Maximum analytical performance.
  - **DirectQuery Mode**: Direct query to the source in real time. Suited to massive data volumes or real-time refresh.
  - **Composite / Dual Mode**: A combination of Import and DirectQuery to optimize aggregations while keeping support for recent data.
  - **DirectLake Mode (Microsoft Fabric)**: Direct read of **Parquet / Delta Lake** files in OneLake without importing data or translating to SQL.
- **Deployment Pipelines & ALM**:
  - Lifecycle management in 3 stages (Development, Test, Production) with automatic updating of connection parameters and re-binding of Dataflows.

---

## ⚙️ Power BI Engineer Decision Protocol

1. **Avoid Measures in Calculated Columns**: Always create dynamic DAX measures instead of calculated columns on the Fact table to save RAM in the VertiPaq model.
2. **Define Explicit Measures**: Never use automatic field aggregation in the report interface. Create every metric as an explicit measure.
3. **Enforce RLS at the Dimension Source**: Ensure dimension tables apply dynamic RLS cleanly, avoiding the propagation of costly bidirectional filters.

---

## 🔗 Integration with Other Skills

- To automate Power BI alerts and report delivery via email/Teams, see the [power-automate](../../platforms/power-automate/SKILL.md) skill.
- To configure identities and RLS in Entra ID (Azure AD), see the [iam-access-azure](../../security/iam/iam-access-azure/SKILL.md) skill.
- To integrate BI models with data warehouses and SQL databases, see the [backend-developer](../../roles/backend-developer/SKILL.md) skill.
