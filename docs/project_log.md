# Project Log

## Project: AI-Based Customer Behavior Shift Detection

---

## 1. Data Profiling

### Objective

The objective of this stage was to understand the structure, quality, completeness, temporal coverage, customer coverage, and potential anomalies in the Online Retail II dataset before performing data cleaning and feature engineering.

---

### Dataset Source

The project uses the **Online Retail II** dataset from the UCI Machine Learning Repository.

The original workbook contains two sheets:

* `Year 2009-2010`
* `Year 2010-2011`

Both sheets contain the same 8 original features:

* Invoice
* StockCode
* Description
* Quantity
* InvoiceDate
* Price
* Customer ID
* Country

---

### Dataset Structure

The two sheets were loaded and combined programmatically.

#### Year 2009-2010

* Rows: 525,461
* Columns: 8

#### Year 2010-2011

* Rows: 541,910
* Columns: 8

#### Combined Dataset

* Rows: 1,067,371
* Columns: 8

The combined raw dataset was saved as:

`data/raw/online_retail_II.csv`

The raw dataset is kept separate from processed data.

---

## 2. Missing Values

Missing values were identified in two columns:

| Column      | Missing Rows | Missing Rate |
| ----------- | -----------: | -----------: |
| Customer ID |      243,007 |       22.77% |
| Description |        4,382 |        0.41% |

Customer ID is important for this project because the target is based on changes in individual customer behavior over time.

Transactions without Customer ID cannot be assigned to a specific customer and therefore cannot contribute to customer-level behavioral features.

Missing Description values are less critical because Description is not a primary feature used by the final customer-level modeling pipeline.

---

## 3. Duplicate Records

The combined dataset contains:

* Total duplicate rows: 34,335

Duplicates were also examined separately for each original sheet:

* Year 2009-2010: 6,865 duplicate rows
* Year 2010-2011: 5,268 duplicate rows

Rows duplicated across the two sheets:

* 23,221 rows

Unique rows duplicated across sheets:

* 22,202

These results indicate that duplication exists both within individual sheets and across the combined dataset and must be considered during data cleaning.

The raw dataset will not be modified directly. Any duplicate removal will be performed on a processed dataset and documented.

---

## 4. Customer Coverage

The combined dataset contains:

* Total transaction rows: 1,067,371
* Transactions with Customer ID: 824,364
* Transactions without Customer ID: 243,007
* Customer ID coverage: 77.23%

There are:

* 5,942 unique customers with Customer ID
* 5,796 customers with multiple transactions
* 2,890 customers active across multiple years

This confirms that the dataset contains sufficient repeated customer activity for temporal behavioral analysis.

---

## 5. Customer Transaction Distribution

The number of transactions per customer was examined.

Results:

* Mean: 138.74 transactions
* Median: 53 transactions
* Maximum: 13,097 transactions
* Minimum: 1 transaction

The distribution is highly uneven, with some customers having substantially more transactions than others.

This is important because customer activity is not uniformly distributed.

---

## 6. Customer Monthly Activity

The dataset contains:

* Unique customers: 5,942
* Unique months: 25
* Active customer-month observations: 26,993

Not every customer is active in every month.

Therefore, the number of observed customer-month combinations is much smaller than the theoretical:

`5,942 × 25 = 148,550`

This supports the decision to construct a customer-month behavioral dataset rather than treating individual transaction rows as the main modeling observations.

---

## 7. Transaction Quantity Analysis

Negative quantities:

* 22,950 rows

Zero quantities:

* 0 rows

Negative quantities were investigated to determine whether they represented cancellations or other business events.

Among negative-quantity transactions:

* 19,493 were associated with cancellation-style invoice numbers beginning with `C`.
* 3,457 negative-quantity rows were not associated with cancellation invoice numbers.

The non-cancellation negative-quantity records were inspected and included descriptions such as:

* `short`
* `lost`
* `damages`
* `sold as gold`
* `invcd as ...`

These records appear to represent operational adjustments, damaged/lost goods, or other non-standard transactions.

This finding will be considered during the data-cleaning stage.

---

## 8. Cancellation Analysis

Cancellation records were explicitly investigated.

Results:

* Cancellation rows: 19,494
* Cancellation invoices: 8,292
* Cancellation invoices with positive quantity: 1

The large majority of negative-quantity cancellation records therefore follow the expected pattern of representing returned/cancelled quantities.

---

## 9. Price Analysis

Negative-price rows:

* 5

All five negative-price records were manually inspected.

They had:

* Description: `Adjust bad debt`
* Quantity: 1
* Customer ID: missing
* Negative prices

These records represent financial adjustments rather than normal customer purchases.

Because they do not represent identifiable customer purchasing behavior and have no Customer ID, they should not contribute to customer-level behavioral modeling.

Zero-price rows:

* 6,202

The zero-price records were also investigated.

Among them:

* 6,131 had missing Customer ID

The quantity distribution of zero-price rows was also examined and showed that these records include both positive and negative quantities.

Zero-price records will therefore be handled carefully during data cleaning rather than automatically assuming that every zero-price row is a valid purchase.

---

## 10. Description Analysis

Missing descriptions:

* 4,382 rows

Several frequent non-product descriptions were identified, including:

* `check`
* `?`
* `damages`
* `damaged`
* `found`
* `missing`
* `adjustment`
* `dotcom`
* `amazon`
* `smashed`

These values suggest that some records contain operational notes or adjustments rather than standard product descriptions.

Since Description is not a primary modeling feature, missing descriptions alone are not considered sufficient reason to remove a transaction.

---

## 11. Temporal Coverage

The dataset spans:

* Minimum date: 2009-12-01 07:45:00
* Maximum date: 2011-12-09 12:50:00

There are:

* 47,635 unique `InvoiceDate` timestamps

The `InvoiceDate` column contains both date and time, so the number of unique timestamps is not equivalent to the number of unique calendar days.

The temporal coverage is sufficient for constructing monthly customer behavior features.

---

## 12. Monthly Transaction Activity

Transaction volume varies considerably across months.

Higher transaction volumes were observed around October-November, while some early-year months had lower activity.

December 2011 contains fewer transactions because the dataset ends on December 9, 2011, making it a partial month.

This is important when interpreting temporal patterns.

---

## 13. Monthly Customer ID Missingness

The missing Customer ID rate varies across months.

Examples:

* 2010-10: approximately 14.45%
* 2010-12: approximately 35.92%
* 2011-01: approximately 37.66%
* 2011-07: approximately 30.41%
* 2011-12: approximately 30.81%

This confirms that missing Customer ID values are not distributed uniformly over time.

Because Customer ID is required for customer-level behavioral analysis, transactions without Customer ID cannot be used to construct identifiable customer behavior histories.

---

## 14. Profiling Conclusions

The profiling stage confirmed that:

1. The dataset contains sufficient temporal information for behavior-shift analysis.
2. Customer ID is available for 77.23% of transaction rows.
3. There are 5,942 identifiable customers and 26,993 active customer-month observations.
4. Duplicate records exist and require explicit handling.
5. Negative quantities are mostly associated with cancellations, but some represent other operational events.
6. Negative-price records were identified as bad-debt adjustments rather than normal purchases.
7. Zero-price transactions require additional investigation before deciding how to handle them.
8. Customer activity varies substantially over time.
9. December 2011 is a partial month and must be considered when interpreting temporal patterns.
10. The raw dataset should remain unchanged, while cleaning and filtering should be performed on processed data.

---

## 15. Next Step

The next stage is **Data Cleaning**.

The cleaning process will define explicit rules for:

* customer identification,
* duplicate handling,
* cancellations and negative quantities,
* zero-price transactions,
* invalid or non-customer transactions,
* and preparation of the customer-level temporal dataset.

All cleaning decisions will be documented before model training to maintain a reproducible and leakage-aware pipeline.

## Data Cleaning & Validation

- Combined the two Online Retail II sheets into a single transaction-level dataset.
- Kept transactions with a valid Customer ID because customer-level behavior analysis requires customer identification.
- Removed cancellation transactions identified by negative quantities and cancellation invoice codes.
- Removed zero-price transactions because they do not represent normal positive-value purchases.
- Removed non-product transactions such as postage, bank charges, and discounts.
- Removed exact duplicate transaction rows.
- Added a monthly time feature (`Month`) derived from `InvoiceDate`.
- Performed final data-quality validation.

### Final Clean Dataset

- Rows: 776,844
- Columns: 9
- Missing values: 0
- Negative quantities: 0
- Zero quantities: 0
- Negative prices: 0
- Zero prices: 0
- Exact duplicates: 0
- Date range: December 2009 – December 2011
- Number of months: 25