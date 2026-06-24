Here is a clean, relational database structure for a universal e-commerce platform. This schema is designed to be scalable and normalizes the data to prevent redundancy, which is especially helpful when mapping these tables to an ORM (like Django's or SQLAlchemy) for full-stack development.

### **Core Entities & Relationships**

#### **1. Users**

The central table for customer authentication and profile data.

| Column Name | Data Type | Constraints / Relations |
| --- | --- | --- |
| `id` | UUID / Integer | Primary Key, Auto-increment |
| `email` | String | Unique, Not Null |
| `password_hash` | String | Not Null |
| `first_name` | String |  |
| `last_name` | String |  |
| `created_at` | Timestamp | Default: Current Time |

#### **2. Categories**

Allows products to be grouped. Including a `parent_id` allows for sub-categories (e.g., Electronics -> Laptops).

| Column Name | Data Type | Constraints / Relations |
| --- | --- | --- |
| `id` | Integer | Primary Key, Auto-increment |
| `name` | String | Not Null |
| `slug` | String | Unique (for URL routing) |
| `parent_id` | Integer | Foreign Key (`Categories.id`), Nullable |

#### **3. Products**

The core catalog.

| Column Name | Data Type | Constraints / Relations |
| --- | --- | --- |
| `id` | UUID / Integer | Primary Key, Auto-increment |
| `category_id` | Integer | Foreign Key (`Categories.id`) |
| `name` | String | Not Null |
| `description` | Text |  |
| `price` | Decimal(10, 2) | Not Null |
| `stock_quantity` | Integer | Default: 0 |
| `is_active` | Boolean | Default: True (to hide discontinued items) |
| `created_at` | Timestamp | Default: Current Time |

#### **4. Reviews (Ratings & Comments)**

Combines both the star rating and the text comment into a single entity to ensure a user's comment is always tied to their rating.

| Column Name | Data Type | Constraints / Relations |
| --- | --- | --- |
| `id` | Integer | Primary Key, Auto-increment |
| `product_id` | UUID / Integer | Foreign Key (`Products.id`) |
| `user_id` | UUID / Integer | Foreign Key (`Users.id`) |
| `rating` | Integer | Check: 1 to 5, Not Null |
| `comment` | Text | Nullable |
| `created_at` | Timestamp | Default: Current Time |

*(Note: You would typically add a Unique Constraint on `[product_id, user_id]` so a user can only leave one review per product).*

#### **5. Saved Items (Wishlist)**

A junction table linking users to the products they want to save for later.

| Column Name | Data Type | Constraints / Relations |
| --- | --- | --- |
| `id` | Integer | Primary Key, Auto-increment |
| `user_id` | UUID / Integer | Foreign Key (`Users.id`) |
| `product_id` | UUID / Integer | Foreign Key (`Products.id`) |
| `added_at` | Timestamp | Default: Current Time |

#### **6. Orders**

Tracks the overarching checkout event for a user.

| Column Name | Data Type | Constraints / Relations |
| --- | --- | --- |
| `id` | UUID / Integer | Primary Key, Auto-increment |
| `user_id` | UUID / Integer | Foreign Key (`Users.id`) |
| `status` | Enum/String | 'Pending', 'Shipped', 'Delivered', 'Cancelled' |
| `total_amount` | Decimal(10, 2) | Not Null |
| `shipping_address` | Text | Not Null |
| `created_at` | Timestamp | Default: Current Time |

#### **7. Order Items**

A bridge table that records the specific products bought within a single order. It is crucial to store the `price_at_purchase` here, as the live product price might change in the future, but historical order records must remain accurate.

| Column Name | Data Type | Constraints / Relations |
| --- | --- | --- |
| `id` | Integer | Primary Key, Auto-increment |
| `order_id` | UUID / Integer | Foreign Key (`Orders.id`) |
| `product_id` | UUID / Integer | Foreign Key (`Products.id`) |
| `quantity` | Integer | Check: > 0 |
| `price_at_purchase` | Decimal(10, 2) | Not Null |

---

### **Implementation Notes**

* **Database Choice:** This relational structure is ideal for SQL databases like PostgreSQL or MySQL.
* **Indexing:** To keep API responses fast, you should add indexes to frequently queried foreign keys (like `category_id` in the Products table, and `user_id` in the Orders table).
* **Images:** For product images, it's best practice to create a separate `Product_Images` table with a `product_id` foreign key and an `image_url` string field. This allows a one-to-many relationship where a single product can feature a carousel of multiple images.