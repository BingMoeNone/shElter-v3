﻿﻿﻿﻿﻿# Data Model: Wiki Platform

## Entity: User
**Description**: Represents a registered member with profile information, authentication credentials, and social connections

**Fields**:
- `id` (UUID): Unique identifier for the user
- `username` (String(30), unique): Unique username for login/display
- `email` (String(255), unique): User's email address
- `password_hash` (String(255)): Hashed password for authentication
- `display_name` (String(50), nullable): Name displayed publicly
- `bio` (Text, nullable): User biography/description
- `avatar_url` (String(500), nullable): URL to user's profile picture
- `created_at` (DateTime): Account creation timestamp
- `updated_at` (DateTime): Last profile update timestamp
- `is_active` (Boolean): Account status flag
- `role` (String(20), default: "user"): User permission level (user, moderator, admin)
- `level` (Integer, default: 1): User Level (1-10, for v1 integration)
- `contribution_count` (Integer, default: 0): Number of articles contributed

**Relationships**:
- One-to-many with Article (user creates articles)
- One-to-many with Comment (user writes comments)
- Many-to-many with User through Connection (social connections)
- One-to-many with Revision (user creates revisions)

## Entity: Article
**Description**: Represents a wiki entry with content, metadata, version history, author information, and associated categories/tags

**Fields**:
- `id` (UUID): Unique identifier for the article
- `title` (String(200)): Title of the article
- `slug` (String(250), unique): URL-friendly identifier
- `content` (Text): Main content of the article
- `summary` (Text, nullable): Brief summary/description
- `status` (String(20), default: "draft"): Publication status (draft, published, archived)
- `author_id` (UUID): Reference to the user who created the article
- `published_at` (DateTime, nullable): Publication timestamp
- `created_at` (DateTime): Creation timestamp
- `updated_at` (DateTime): Last update timestamp
- `view_count` (Integer, default: 0): Number of times viewed
- `is_featured` (Boolean, default: false): Flag for featured articles
- `is_approved` (Boolean, default: true): Moderation status flag

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
- `status` (String(20), default: "pending"): Connection status (pending, accepted, blocked)
- `connection_type` (String(20)): Type of connection (friend, follow)
- `created_at` (DateTime): Connection request timestamp
- `accepted_at` (DateTime, nullable): Connection acceptance timestamp

**Relationships**:
- Many-to-one with User (follower relationship)
- Many-to-one with User (followed relationship)

## Entity: Category
**Description**: Represents a classification system for organizing articles by topic

**Fields**:
- `id` (UUID): Unique identifier for the category
- `name` (String(100), unique): Name of the category
- `slug` (String(120), unique): URL-friendly identifier
- `description` (Text, nullable): Detailed description of the category
- `parent_id` (UUID, nullable): Reference to parent category for hierarchy
- `created_at` (DateTime): Creation timestamp
- `updated_at` (DateTime): Last update timestamp
- `article_count` (Integer, default: 0): Number of articles in this category

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
- `is_approved` (Boolean, default: true): Moderation status

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
- `title` (String(200)): Title at the time of revision
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
- `name` (String(50), unique): Name of the tag
- `slug` (String(60), unique): URL-friendly identifier
- `created_at` (DateTime): Creation timestamp
- `usage_count` (Integer, default: 0): Number of times this tag is used

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

## Additional Entities

### Entity: AuditLog
**Description**: Represents audit logs for tracking system activities and user actions

**Fields**:
- `id` (UUID): Unique identifier for the audit log
- `operator_id` (UUID): Reference to the user who performed the action
- `operator_username` (String(30)): Username of the user who performed the action
- `action` (String(50)): Type of action performed
- `target_type` (String(50)): Type of entity affected by the action
- `target_id` (UUID, nullable): ID of the entity affected by the action
- `target_info` (Text, nullable): Additional information about the target entity
- `details` (Text, nullable): Additional details about the action
- `ip_address` (String(45), nullable): IP address of the user who performed the action
- `user_agent` (String(500), nullable): User agent string from the client
- `status` (String(20), default: "success"): Status of the action (success, failed)
- `error_message` (Text, nullable): Error message if the action failed
- `created_at` (DateTime): Timestamp when the action was performed

### Entity: Station (Metro Integration)
**Description**: Represents a metro station in the metro map system

**Fields**:
- `id` (UUID): Unique identifier for the station
- `name` (String): Name of the station
- `slug` (String, unique): URL-friendly identifier
- `description` (Text, nullable): Description of the station
- `line_id` (UUID, nullable): Reference to the line this station belongs to
- `position_x` (Integer): X coordinate on the metro map
- `position_y` (Integer): Y coordinate on the metro map
- `created_at` (DateTime): Creation timestamp
- `updated_at` (DateTime): Last update timestamp

### Entity: Line (Metro Integration)
**Description**: Represents a metro line in the metro map system

**Fields**:
- `id` (UUID): Unique identifier for the line
- `name` (String): Name of the line
- `color` (String): Color of the line in hex format
- `description` (Text, nullable): Description of the line
- `created_at` (DateTime): Creation timestamp
- `updated_at` (DateTime): Last update timestamp

### Entity: StationLineJunction (Metro Integration)
**Description**: Association table between stations and lines (many-to-many relationship)

**Fields**:
- `station_id` (UUID): Reference to the station
- `line_id` (UUID): Reference to the line
- `order` (Integer): Order of the station in the line
- `created_at` (DateTime): Creation timestamp

### Entity: Track (Music Integration)
**Description**: Represents a music track in the music player system

**Fields**:
- `id` (UUID): Unique identifier for the track
- `title` (String): Title of the track
- `artist_id` (UUID): Reference to the artist who created the track
- `album_id` (UUID, nullable): Reference to the album this track belongs to
- `duration` (Integer): Duration of the track in seconds
- `file_path` (String): Path to the audio file
- `play_count` (Integer, default: 0): Number of times this track has been played
- `created_at` (DateTime): Creation timestamp
- `updated_at` (DateTime): Last update timestamp

### Entity: Album (Music Integration)
**Description**: Represents a music album in the music player system

**Fields**:
- `id` (UUID): Unique identifier for the album
- `title` (String): Title of the album
- `artist_id` (UUID): Reference to the artist who created the album
- `release_date` (DateTime, nullable): Release date of the album
- `cover_path` (String, nullable): Path to the album cover image
- `created_at` (DateTime): Creation timestamp
- `updated_at` (DateTime): Last update timestamp

### Entity: Artist (Music Integration)
**Description**: Represents a music artist in the music player system

**Fields**:
- `id` (UUID): Unique identifier for the artist
- `name` (String): Name of the artist
- `description` (Text, nullable): Description of the artist
- `created_at` (DateTime): Creation timestamp
- `updated_at` (DateTime): Last update timestamp

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