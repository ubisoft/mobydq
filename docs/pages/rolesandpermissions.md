---
layout: page
title: Roles & Permissions
use-site-title: true
---

# Roles

Roles and permissions are managed using the internal PostgreSQL role concepts. MobyDQ uses 4 roles which define to which database objects users can access to (object-level security).

## Anonymous

The `anonymous` role is the default role used to query the database for non-authenticated users. It grants permissions to read data on all tables and views of the base schema except:

-   Table `base.password` which contains users' passwords.
-   View `base.data_source_password` which displays decrypted data sources' passwords.

## Standard

The `standard` role is the default role for all authenticated users who wish to create and execute data quality indicators. It inherits permissions from the `anonymous` role. In addition, it grants permissions to write and delete the following objects:

-   Indicators
-   Indicator groups
-   Indicator parameters
-   Batches
-   Sessions
-   Session results

## Advanced

The `advanced` role is the role for users who need to manage data sources and their password. It inherits permissions from the `standard` role. In addition, it grants permissions to write and delete the following objects:

-   Data sources

## Admin

The `admin` role is used to manage application users and configuration. It grants the same permissions as the `advanced` role, plus the permissions to write and delete the following objects:

-   Data source types
-   Indicator types
-   Indicator parameter types
-   Users
-   User groups

---

# Row Level Security (RLS)

In addition to object-level security, MobyDQ also implements PostgreSQL row-level security. It is used to manage visibility rules on the data so that users only see the data of the user groups they belong to. Row-level security is implemented for the following objects:

-   Data sources
-   Indicators
-   Indicator groups
-   Indicator parameters
-   Batches
-   Sessions
-   Session results
