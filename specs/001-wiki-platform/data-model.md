# Data Model: Wiki Platform

## Entity: User
**Description**: Represents a registered member with profile information, authentication credentials, and social connections

**Fields**:
- `id` (UUID): Unique identifier for the user
- `username` (String, unique): Unique username for login/display
- `email` (String, unique): User's email address
- `password_hash` (String): Hashed password for authentication
- `display_name` (String): Name displayed publicly
- `bio` (Text, nullable): User biography/description
- `avatar_url` (String, nullable): URL to user's profile picture
- `created_at` (DateTime): Account creation timestamp
- `updated_at` (DateTime): Last profile update timestamp
- `is_active` (Boolean): Account status flag
- `role` (Enum: user, moderator, admin): User permission level
- `contribution_count` (Integer): Number of articles contributed

**Relationships**:
- One-to-many with Article (user creates articles)
- One-to-many with Comment (user writes comments)
- Many-to-many with User through Connection (social connections)
- One-to-many with Revision (user creates revisions)

## Entity: Article
**Description**: Represents a wiki entry with content, metadata, version history, author information, and associated categories/tags

**Fields**:
- `id` (UUID): Unique identifier for the article
- `title` (String): Title of the article
- `slug` (String, unique): URL-friendly identifier
- `content` (Text): Main content of the article
- `summary` (Text): Brief summary/description
- `status` (Enum: draft, published, archived): Publication status
- `author_id` (UUID): Reference to the user who created the article
- `published_at` (DateTime, nullable): Publication timestamp
- `created_at` (DateTime): Creation timestamp
- `updated_at` (DateTime): Last update timestamp
- `view_count` (Integer): Number of times viewed
- `is_featured` (Boolean): Flag for featured articles

**Relationships**:
- Many-to-one with User (author relationship)
- One-to-many with Revision (version history)
- One-to-many with Comment (article comments)
- Many-to-many with Category through ArticleCategory (categories association)
- Many-to-many with Tag through ArticleTag (tags association)

## Entity: Connection
**Description**: Represents relationships between users (friendships, follows, etc.)

**Fields**:
- `id` (UUID): Unique identifier for the connection
- `follower_id` (UUID): ID of the user initiating the connection
- `followed_id` (UUID): ID of the user being connected to
- `status` (Enum: pending, accepted, blocked): Connection status
- `connection_type` (Enum: friend, follow): Type of connection
- `created_at` (DateTime): Connection request timestamp
- `accepted_at` (DateTime, nullable): Connection acceptance timestamp

**Relationships**:
- Many-to-one with User (follower relationship)
- Many-to-one with User (followed relationship)

## Entity: Category
**Description**: Represents a classification system for organizing articles by topic

**Fields**:
- `id` (UUID): Unique identifier for the category
- `name` (String): Name of the category
- `slug` (String, unique): URL-friendly identifier
- `description` (Text, nullable): Detailed description of the category
- `parent_id` (UUID, nullable): Reference to parent category for hierarchy
- `created_at` (DateTime): Creation timestamp
- `updated_at` (DateTime): Last update timestamp
- `article_count` (Integer): Number of articles in this category

**Relationships**:
- Self-referencing many-to-one (parent category)
- Many-to-many with Article through ArticleCategory (articles in category)

## Entity: Comment
**Description**: Represents user-generated discussion attached to articles

**Fields**:
- `id` (UUID): Unique identifier for the comment
- `content` (Text): Content of the comment
- `author_id` (UUID): Reference to the user who wrote the comment
- `article_id` (UUID): Reference to the article the comment belongs to
- `parent_id` (UUID, nullable): Reference to parent comment for threading
- `created_at` (DateTime): Creation timestamp
- `updated_at` (DateTime): Last update timestamp
- `is_approved` (Boolean): Moderation status

**Relationships**:
- Many-to-one with User (author relationship)
- Many-to-one with Article (article relationship)
- Self-referencing many-to-one (parent comment for threading)

## Entity: Revision
**Description**: Represents a version of an article with timestamp, author, and change summary

**Fields**:
- `id` (UUID): Unique identifier for the revision
- `article_id` (UUID): Reference to the article being revised
- `author_id` (UUID): Reference to the user who made the revision
- `title` (String): Title at the time of revision
- `content` (Text): Content at the time of revision
- `change_summary` (Text, nullable): Summary of changes made
- `revision_number` (Integer): Sequential revision number
- `created_at` (DateTime): Creation timestamp

**Relationships**:
- Many-to-one with Article (article relationship)
- Many-to-one with User (author relationship)

## Entity: Tag
**Description**: Represents tags that can be associated with articles for categorization

**Fields**:
- `id` (UUID): Unique identifier for the tag
- `name` (String, unique): Name of the tag
- `slug` (String, unique): URL-friendly identifier
- `created_at` (DateTime): Creation timestamp
- `usage_count` (Integer): Number of times this tag is used

**Relationships**:
- Many-to-many with Article through ArticleTag (articles tagged with this tag)

## Junction Tables

### ArticleCategory
**Description**: Association table between articles and categories

**Fields**:
- `article_id` (UUID): Reference to the article
- `category_id` (UUID): Reference to the category
- `assigned_at` (DateTime): Timestamp when article was categorized

### ArticleTag
**Description**: Association table between articles and tags

**Fields**:
- `article_id` (UUID): Reference to the article
- `tag_id` (UUID): Reference to the tag
- `assigned_at` (DateTime): Timestamp when tag was assigned

## Validation Rules

### User Validation
- Username: 3-30 characters, alphanumeric and underscores only
- Email: Valid email format
- Password: Minimum 8 characters with mixed case, numbers, and special characters

### Article Validation
- Title: 1-200 characters
- Content: Minimum 10 characters for published articles
- Slug: Alphanumeric, hyphens, and underscores only

### Comment Validation
- Content: 1-10000 characters
- Cannot be a reply to its own parent thread

## State Transitions

### Article Status Transitions
- draft 鈫?published (on first publication)
- published 鈫?draft (on unpublishing)
- published 鈫?archived (on archiving)
- draft 鈫?archived (on archiving draft)

### Connection Status Transitions
- pending 鈫?accepted (when connection request accepted)
- pending 鈫?blocked (when connection request rejected)
- accepted 鈫?blocked (when connection blocked)
- blocked 鈫?pending (when blocked user sends new request)