# Dirty Cafe Sales - Data Cleaning

## Dataset Information

Source: https://www.kaggle.com/datasets/oleksiimartusiuk/e-commerce-data-shein

Files:

- appliances
- automotive
- baby_and_maternity
- bags_and_luggage
- beauty_and_health
- curve
- electronics
- home_and_kitchen
- home_textile
- jewelry_and_accessories
- kids
- mens_clothes
- office_and_school_supplies
- pet_supplies
- shoes
- sports_and_outdoors
- swimwear
- tools_and_home_improvement
- toys_and_games
- underwear_and_sleepwear
- womens_clothing

All Columns:

| Column                         | Description                                          | Issues Found               |
| ------------------------------ | ---------------------------------------------------- | -------------------------- |
| `goods-title-link-jump`        | Product title or name (1)                            | OK                         |
| `goods-title-link-jump href`   | Product link (1)                                     | Missing and `error` values |
| `selling_proposition`          | How many sold recently                               | Missing and `error` values |
| `price`                        | Price of the product                                 | Missing and `error` values |
| `discount`                     | Discount off the price (`quantity * price_per_unit`) | Missing and `error` values |
| `rank-title`                   | Rank in subcategory                                  | Missing and `error` values |
| `rank-sub`                     | Subcategory of the product                           | Missing and `error` values |
| `color-count`                  | How many color of the product                        | Missing and `error` values |
| `goods-title-link`             | Product title or name (2)                            | Missing and `error` values |
| `blackfridaybelts-bg src`      | Bacground image of the black friday event            | Missing and `error` values |
| `blackfridaybelts content`     | Discount off the price when black friday             | Missing and `error` values |
| `product-locatelabels-img src` | Product link (2)                                     | Missing and `error` values |

Not all datasets have the columns above, here is further information:

![Table of Dirty Ecommerce Dataset](/images/dataset_dirty_ecommerce.png)

🟢 = Field available
<br>
⚪ = Field unavailable

---

## Cleaning Strategy

### `Columns`

- **Issue:** column names are not in the same format.
- **Actions:**
  - Convert to lowercase.
  - Replace hyphens `-` with underscores `_`.
  - Replace spaces with underscores `_`.
  - Remove double underscores `__`.

### `Product Title`

- **Issue:** column names are not in the same format.
- **Actions:**
  - Remove excessive whitespace using regex pattern `\s+`.
  - Handle cases with both `goods_title_link` and `goods_title_link_jump` columns.
  - Create unified product_name field by prioritizing `goods_title_link_jump` when available.

### `Price`

- **Issue:** column names are not in the same format.
- **Actions:**
  - Remove comma separators from price values.
  - Remove currency symbols `$`.
  - Convert to `float` data type.

### `Discount`

- **Issue:** column names are not in the same format.
- **Actions:**
  - Extract numeric values only using regex `[^0-9]`.
  - Convert percentage to decimal format (divide by 100).
  - Convert to `float` data type.

### `Selling Proposition & Sold Number`

- **Issue:** column names are not in the same format.
- **Actions:**
  - Extract numeric values from `selling_proposition` text.
  - Handle `k` multiplier (multiply by 1000 for values containing `k`).
  - Convert to `float` data type.

### `Rank Title Transformation`

- **Issue:** column names are not in the same format.
- **Actions:**
  - Extract numeric values only using regex `[^0-9]`.

### `Category-Specific Transformations`

- **Issue:** Handle missing or inconsistent data per category.

| **Category**                 | **Transformations Applied**                                       |
| ---------------------------- | ----------------------------------------------------------------- |
| **Appliances**               | Set `color_count = 1`                                             |
| **Automotive**               | Set `rank_num = NaN`, `rank_subcategory = NaN`, `color_count = 1` |
| **Baby & Maternity**         | Set `rank_num = NaN`, `rank_subcategory = NaN`                    |
| **Home & Kitchen**           | Set `goods_title_link_jump_href = NaN`, `color_count = 1`         |
| **Jewelry & Accessories**    | Set `color_count = 1`                                             |
| **Men's Clothes**            | Set `goods_title_link_jump_href = NaN`                            |
| **Office & School**          | Set `color_count = 1`                                             |
| **Swimwear**                 | Set `selling_proposition = NaN`, `sold_number = NaN`              |
| **Tools & Home Improvement** | Set `color_count = 1`                                             |
| **Toys & Games**             | Set `goods_title_link_jump_href = NaN`, `color_count = 1`         |
| **Women's Clothing**         | Set `goods_title_link_jump_href = NaN`                            |

---

## Separate Clean and Reject Data

Data was separated into clean and rejected subsets based on data completeness and validity criteria. A record is rejected if:

- Missing both `product_name` AND `price`.
- Missing `product_name` only.

---

## Dimensional Table

To support analytical processing and improve data organization, the cleaned dataset was modeled into a **dimensional schema**. The schema follows a **star schema** design, separating descriptive attributes (dimensions) from measurable facts.

### Shema Design

- **Dimensional Table:**
  - `dim_category`: Contains `category_id` and `category`.
  - `dim_rank_subcategory`: Contains `rank_subcategory_id` and `rank_subcategory`.
  - `dim_products` (product fact table): Contains `product_id`, `product_name`, `product_link`, `category_id`, `color_count`, `price`, `discount`, `rank_num`, `rank_subcategory_id`, and `sold_number`.

### Diagram

![Dimensional Model of Dirty Ecommerce Dataset](/images/dimensional_model_dirty_ecommerce.jpg)
