# Global Freelancers - Data Cleaning

## Dataset Information

Source: https://www.kaggle.com/datasets/urvishahir/global-freelancers-raw-dataset

![Table of Global Freelancers Dataset](/images/table_global_freelancers.png)

| Column                | Description                            | Issues Found                               |
| --------------------- | -------------------------------------- | ------------------------------------------ |
| `freelancer_id`       | Unique identifier for every freelancer | OK                                         |
| `name`                | Freelancer name                        | OK                                         |
| `gender`              | Gender information                     | Inconsistent (upper/lower case)            |
| `age`                 | Age information                        | Some missing values                        |
| `country`             | Country origin                         | OK                                         |
| `language`            | Used language                          | OK                                         |
| `primary_skill`       | Primary skill                          | OK                                         |
| `years_of_experience` | Years of work experience               | Missing values                             |
| `hourly_rate_usd`     | Hourly rate in USD                     | Missing values and inconsistent format     |
| `rating`              | Rating from client                     | Missing values                             |
| `is_active`           | Freelancer's active status             | Inconsistent format (1, Y, True, yes, etc) |
| `client_satisfaction` | Client satisfaction level              | Inconsistent format                        |

## Cleaning Strategy

### `gender`

- **Issue:** Inconsistent value `'f', 'FEMALE', 'male', 'F', 'female', 'm', 'MALE', 'Female', 'M', 'Male'`.
- **Action:**
  - All values are converted to lowercase letters.
  - Standardization into 2 categories, `male` and `female`.

### `age`

- **Issue:** Some missing values.
- **Action:** Leave it as missing to avoid introducing bias from arbitrary imputation; missing values can be handled appropriately during modeling or further analysis.

### `years_of_experience`

- **Issue:** Some missing values.
- **Action:** Filled missing (NaN) values with 0 to indicate no prior experience, ensuring numerical consistency for further analysis.

### `hourly_rate_usd`

- **Issue:** Missing values and inconsistent format, `'100', 'USD 100', '50', '$40', '30', '$30', 'USD 75', 'USD 40', nan, '$50', '40', '75', 'USD 50', 'USD 30', '$20', '20', '$75', '$100', 'USD 20'`.
- **Action:**
  - Delete letters and symbols other than numbers.
  - Convert to a numeric type (float).

### `rating`

- **Issue:** Missing values.
- **Action:** Left as missing to preserve data integrity, since imputing ratings could introduce subjective bias and reduce the reliability of analytical results.

### `is_active`

- **Issue:** Inconsistent format, `'0', '1', 'N', 'False', 'True', 'yes', 'Y', nan, 'no'`.
- **Action:**
  - Mapping all value variations to `True` (active) and `False` (inactive).
  - Changing the data type to `bool`.

### `client_satisfaction`

- **Issue:** Inconsistent format, some percentage have `%` and some don't.
- **Action:**
  - Delete letters and symbols other than numbers.
  - Convert to a numeric type (float).

## Dimensional Table

To support analytical processing and improve data organization, the cleaned dataset was modeled into a **dimensional schema**.  
The schema follows a **star schema** design, separating descriptive attributes (dimensions) from measurable facts.

### Shema Design

- **Fact Table:** `fact_freelancers`
  - Contains measurable attributes, such as `years_of_experience`, `hourly_rate_usd`, `rating`, `client_satisfaction`, `is_active`.
- **Dimensional Table:**
  - `dim_genders`: Contains `gender_id` and `gender`.
  - `dim_countries`: Contains `country_id` and `country`.
  - `dim_languages`: Contains `language_id` and `language`.
  - `dim_primary_skills`: Contains `primary_skill_id` and `primary_skill`.

### Diagram

![Dimensional Model of Global Freelances Dataset](/images/dimensional_model_global_freelances.jpg)

**Note:**

- Why I don't create dimensional table for information like `name`, `age`, and `is_active`?

  Since each freelancer record is unique and static (not changing over time), attributes such as `name`, `age`, and `is_active` are retained in the fact table for simplicity and efficiency. Only categorical attributes with repeated values across multiple freelancers (e.g., gender, country, language, and primary_skill) are separated into dimension tables.
