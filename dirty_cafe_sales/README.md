# Dirty Cafe Sales - Data Cleaning

## Dataset Information

Source: https://www.kaggle.com/datasets/ahmedmohamed2003/cafe-sales-dirty-data-for-cleaning-training

![Table of Dirty Cafe Sales Dataset](/images/table_dirty_cafe_sales.png)

| Column             | Description                                      | Issues Found               |
| ------------------ | ------------------------------------------------ | -------------------------- |
| `transaction_id`   | Unique identifier for every transaction          | OK                         |
| `item`             | Name of the purchased item                       | Missing and `error` values |
| `quantity`         | Number of item purchased                         | Missing and `error` values |
| `price_per_unit`   | Price per single unit of the item                | Missing and `error` values |
| `total_spent`      | Total amount spent (`quantity * price_per_unit`) | Missing and `error` values |
| `payment_method`   | Method used for payment                          | Missing and `error` values |
| `location`         | Order method                                     | Missing and `error` values |
| `transaction_date` | Date when the transaction was recorded           | Missing and `error` values |

---

## Cleaning Strategy

### `item`

- **Issue:** Missing and `error` values `'Coffee' 'Cake' 'Cookie' 'Salad' 'Smoothie' 'UNKNOWN' 'Sandwich' nan 'ERROR' 'Juice' 'Tea'`.
- **Action:**
  - `'ERROR', 'UNKNOWN', and nan` values are converted to `'Unknown'`.

### `payment_method`

- **Issue:** Missing and `error` values `''Credit Card' 'Cash' 'UNKNOWN' 'Digital Wallet' 'ERROR' nan`.
- **Action:**
  - `'ERROR', 'UNKNOWN', and nan` values are converted to `'Unknown'`.

### `location`

- **Issue:** Missing and `error` values `'Takeaway' 'In-store' 'UNKNOWN' nan 'ERROR'`.
- **Action:**
  - `'ERROR', 'UNKNOWN', and nan` values are converted to `'Unknown'`.

### `quantity`

- **Issue:** Missing and `error` values like `'UNKNOWN', nan, 'ERROR'`.
- **Action:**
  - Replaced invalid entries `'ERROR' and 'UNKNOWN'` with `nan` and converted the column to numeric `float` type.
  - For records where both `price_per_unit` and `total_spent` are available, recovered the quantity value using the formula `total_spent / price_per_unit`.
  - Remaining missing values were left as `nan` if recovery was not possible.

### `price_per_unit`

- **Issue:** Missing and `error` values like `'UNKNOWN', nan, 'ERROR'`.
- **Action:**
  - Replaced invalid entries `'ERROR' and 'UNKNOWN'` with `nan` and converted the column to numeric `float` type.
  - For records where both `quantity` and `total_spent` are available, recovered the quantity value using the formula `total_spent / quantity`.
  - Restore `price_per_unit` value by mapping with `item`.
  - Remaining missing values were left as `nan` if recovery was not possible.

### `total_spent`

- **Issue:** Missing and `error` values like `'UNKNOWN', nan, 'ERROR'`.
- **Action:**
  - Replaced invalid entries `'ERROR' and 'UNKNOWN'` with `nan` and converted the column to numeric `float` type.
  - For records where both `quantity` and `price_per_unit` are available, recovered the quantity value using the formula `quantity * price_per_unit`.
  - Remaining missing values were left as `nan` if recovery was not possible.

### `transaction_date`

- **Issue:** Missing and `error` values.
- **Action:**
  - Convert all data to `datetime`.

## Separate Clean and Reject Data

Data was separated into clean and rejected subsets based on data completeness and validity criteria. A record is rejected if:

- It does not have at least two of the following values: `quantity`, `price_per_unit`, or `total_spent`.
- It has an invalid or missing value in the transaction_date column, since this field is essential for any time-based analysis and cannot be inferred reliably.

---

## Dimensional Table

To support analytical processing and improve data organization, the cleaned dataset was modeled into a **dimensional schema**. The schema follows a **star schema** design, separating descriptive attributes (dimensions) from measurable facts.

### Shema Design

- **Fact Table:** `fact_transactions`
  - Contains measurable attributes, such as `transaction_date`, `quantity`, `total_spent`.
- **Dimensional Table:**
  - `dim_items`: Contains `item_id`, `item`, and `price_per_unit`.
  - `dim_locations`: Contains `location_id` and `location`.
  - `dim_payment_methods`: Contains `payment_method_id` and `payment_method`.

### Diagram

![Dimensional Model of Dirty Cafe Sales Dataset](/images/dimensional_model_dirty_cafe_sales.jpg)
