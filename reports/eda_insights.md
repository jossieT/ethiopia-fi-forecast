# Task 2: Exploratory Data Analysis & Key Insights

## Executive Summary

This report summarizes the findings from the exploratory data analysis of Ethiopia's financial inclusion landscape (2014-2025). The analysis highlights a critical market shift: while access growth has plateaued, usage of digital rails is exploding.

## Data Limitations

A transparent accounting of data constraints is essential for interpreting these findings:

1.  **Sparse Time Series**: Core "Access" data (Global Findex) is only available for 4 time points (2014, 2017, 2021, 2024), limiting our ability to model year-to-year volatility or precise event attribution.
2.  **Proxy Reliance**: Annual operational data (Telebirr/EthSwitch) is used as a proxy for holistic inclusion, but may overrepresent urban/connected populations compared to national surveys.
3.  **Disaggregation Gaps**: We lack consistent gender-disaggregated data for _usage_ (transaction volumes), limiting our view of the gender gap to _access_ (account ownership) only.
4.  **Inconsistent Definitions**: "Active" users are defined differently across operators (90-day vs 30-day), requiring normalization which introduces uncertainty.

## Key Insights

### 1. The "Access-Usage Paradox" (See Notebook Section 3)

**Observation**: Account ownership growth has decelerated significantly, rising only **3 percentage points** (46% to 49%) between 2021 and 2024. In stark contrast, digital transaction volumes have surged.
**Implication**: The "easy to reach" population is already banked. Future access growth requires targeting harder-to-reach rural segments, while current growth is driven by deepening engagement among existing users.

### 2. Infrastructure as a Leading Indicator (See Notebook Section 5)

**Observation**: 4G Population coverage doubled from **37.5% (2023)** to **70.8% (2025)**.
**Implication**: Historically, connectivity improvements lead financial adoption by 12-18 months. This massive infrastructure upgrade serves as a strong predictor for a delayed spike in digital financial adoption in the 2026-2027 forecast period.

### 3. The Digital Substitution Tipping Point (See Notebook Section 4)

**Observation**: In FY2024/25, **P2P transaction counts (128M)** surpassed **ATM withdrawals (119M)** for the first time (Ratio: 1.08).
**Implication**: This is a historic milestone confirming that digital transfers have replaced cash as the primary value movement mechanism for the connected population.

### 4. The Stubborn Gender Gap (See Notebook Section 4)

**Observation**: The gender gap in account ownership remains high at **~20 percentage points** (56% Male vs 36% Female). Furthermore, women hold only **14%** of mobile money accounts.
**Implication**: Digital channels are not automatically closing the gender gap; structural barriers (ID, handset ownership) persist and require targeted policy interventions.

### 5. Policy Impact Lag (See Notebook Section 2)

**Observation**: The launch of Telebirr (May 2021) did not immediately spike unique account ownership in 2021/2022 data. However, the operational impact is now evident in 2024/25 active user counts (54M+).
**Implication**: Major events (like the 2025 Foreign Bank entry) will likely have a **2-3 year lag** before reflecting in national inclusion statistics.

## Hypotheses for Task 3 Modeling

- **H1**: Usage forecast should be modeled independently of Access, driven by _Product Events_.
- **H2**: Access forecast should use _Infrastructure (4G)_ and _ID Enrollment_ as primary regressors.
- **H3**: The 2025 Foreign Bank Entry will primarily impact _Service Quality_ and _Depth_, not immediate Access numbers.
