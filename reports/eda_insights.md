# Task 2: Exploratory Data Analysis & Key Insights

## Data Quality Assessment

- **Temporal Coverage**: Sparse data points (2014, 2017, 2021, 2024 for Findex). High-frequency measurement (annual/daily) is available only for operational metrics like Telebirr and EthSwitch data starting ~2021.
- **Gaps**: Missing specific "Active User" data for banks comparable to mobile money. Gender disaggregation is only consistently available for Account Ownership.
- **Confidence**: High confidence in Findex and Operator reports; Medium confidence in derived 2024/2025 estimates.

## Key Insights

### 1. The "Access-Usage Paradox"

While **Account Ownership** slowed significantly (growing only +3pp from 46% in 2021 to 49% in 2024), **Usage** exploded. P2P transaction volumes grew ~158% YoY in 2024/25. This suggests the market has shifted from "acquiring new users" to "deepening usage among existing users." The saturation point for "easy" access may have been reached, and future growth will require reaching harder segments (rural/unbanked).

### 2. Infrastructure as a Leading Indicator

4G Population Coverage doubled from 37.5% to 70.8% (2023-2025). Historically, connectivity improvements lead financial service adoption by 12-18 months. This massive infrastructure upgrade predicts a delayed but significant jump in digital financial service adoption in 2025-2026, especially in rural areas previously uncovered.

### 3. The Digital Substitution Tipping Point

For the first time in FY2024/25, **P2P transaction counts (128M) surpassed ATM withdrawals (119M)**, with a ratio of 1.08. This is a historic milestone indicating that digital transfers are replacing cash as the primary mechanism for value movement for connected users.

### 4. Gender Gap Persistence

The gender gap in account ownership remains stubbornly high at ~20 percentage points (56% Male vs 36% Female in 2021). Despite the "democratizing" promise of mobile money, women only hold 14% of mobile money accounts (Source: NBE/Shega). This indicates that structural barriers (ID, phone ownership which has a 24% gap) are preventing women from accessing the new digital rails.

### 5. Policy Impact Lag

The launch of Telebirr (May 2021) did not immediately spike _unique_ account ownership in the 2021 Findex data (collected mid-year). However, the "Telebirr Effect" is clearly visible in the 2024 active user numbers (54M+). The lag between "product launch" and "measured Findex impact" is approximately 2-3 years, suggesting the full impact of the 2023 M-Pesa entry and 2025 Foreign Bank entry will likely be captured in the 2027 Findex survey, not 2024.

## Hypotheses for Modeling (Task 3)

1.  **Usage** is now decoupled from **Access** and should be modeled as a function of _Product Events_ (Telebirr/M-Pesa) rather than population growth.
2.  **Access** growth is now constrained by **Infrastructure** (4G/ID) and **Gender** barriers. Future growth equals "Rural 4G Expansion" + "Fayda ID Rollout".
3.  **Foreign Bank Entry (2025)** will primarily impact **Quality** and **Depth** (credit/savings) rather than basic Access.
