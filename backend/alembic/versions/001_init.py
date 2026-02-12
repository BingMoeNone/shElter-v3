"""init wiki platform tables

Revision ID: 001
Create Date: 2026-02-12

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('username', sa.String(30), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('display_name', sa.String(50), nullable=True),
        sa.Column('bio', sa.Text(), nullable=True),
        sa.Column('avatar_url', sa.String(500), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('role', sa.String(20), nullable=False, server_default='user'),
        sa.Column('contribution_count', sa.Integer(), nullable=False, server_default='0'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username'),
        sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=False)

    op.create_table(
        'categories',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('slug', sa.String(120), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('parent_id', sa.String(36), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('article_count', sa.Integer(), nullable=False, server_default='0'),
        sa.ForeignKeyConstraint(['parent_id'], ['categories.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
        sa.UniqueConstraint('slug')
    )
    op.create_index(op.f('ix_categories_slug'), 'categories', ['slug'], unique=False)
    op.create_index(op.f('ix_categories_parent_id'), 'categories', ['parent_id'], unique=False)

    op.create_table(
        'tags',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('slug', sa.String(60), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('usage_count', sa.Integer(), nullable=False, server_default='0'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
        sa.UniqueConstraint('slug')
    )
    op.create_index(op.f('ix_tags_slug'), 'tags', ['slug'], unique=False)

    op.create_table(
        'articles',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('slug', sa.String(250), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('summary', sa.Text(), nullable=True),
        sa.Column('status', sa.String(20), nullable=False, server_default='draft'),
        sa.Column('author_id', sa.String(36), nullable=False),
        sa.Column('published_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('view_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('is_featured', sa.Boolean(), nullable=False, server_default='0'),
        sa.ForeignKeyConstraint(['author_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('slug')
    )
    op.create_index(op.f('ix_articles_slug'), 'articles', ['slug'], unique=False)
    op.create_index(op.f('ix_articles_author_id'), 'articles', ['author_id'], unique=False)

    op.create_table(
        'article_categories',
        sa.Column('article_id', sa.String(36), nullable=False),
        sa.Column('category_id', sa.String(36), nullable=False),
        sa.Column('assigned_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['article_id'], ['articles.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('article_id', 'category_id')
    )

    op.create_table(
        'article_tags',
        sa.Column('article_id', sa.String(36), nullable=False),
        sa.Column('tag_id', sa.String(36), nullable=False),
        sa.Column('assigned_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['article_id'], ['articles.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('article_id', 'tag_id')
    )

    op.create_table(
        'revisions',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('article_id', sa.String(36), nullable=False),
        sa.Column('author_id', sa.String(36), nullable=False),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('change_summary', sa.Text(), nullable=True),
        sa.Column('revision_number', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['article_id'], ['articles.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['author_id'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_revisions_article_id'), 'revisions', ['article_id'], unique=False)
    op.create_index(op.f('ix_revisions_author_id'), 'revisions', ['author_id'], unique=False)

    op.create_table(
        'comments',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('author_id', sa.String(36), nullable=False),
        sa.Column('article_id', sa.String(36), nullable=False),
        sa.Column('parent_id', sa.String(36), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('is_approved', sa.Boolean(), nullable=False, server_default='1'),
        sa.ForeignKeyConstraint(['author_id'], ['users.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['article_id'], ['articles.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['parent_id'], ['comments.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_comments_article_id'), 'comments', ['article_id'], unique=False)
    op.create_index(op.f('ix_comments_author_id'), 'comments', ['author_id'], unique=False)
    op.create_index(op.f('ix_comments_parent_id'), 'comments', ['parent_id'], unique=False)

    op.create_table(
        'connections',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('follower_id', sa.String(36), nullable=False),
        sa.Column('followed_id', sa.String(36), nullable=False),
        sa.Column('status', sa.String(20), nullable=False, server_default='pending'),
        sa.Column('connection_type', sa.String(20), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('accepted_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['follower_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['followed_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_connections_follower_id'), 'connections', ['follower_id'], unique=False)
    op.create_index(op.f('ix_connections_followed_id'), 'connections', ['followed_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_connections_followed_id'), table_name='connections')
    op.drop_index(op.f('ix_connections_follower_id'), table_name='connections')
    op.drop_table('connections')
    
    op.drop_index(op.f('ix_comments_parent_id'), table_name='comments')
    op.drop_index(op.f('ix_comments_author_id'), table_name='comments')
    op.drop_index(op.f('ix_comments_article_id'), table_name='comments')
    op.drop_table('comments')
    
    op.drop_index(op.f('ix_revisions_author_id'), table_name='revisions')
    op.drop_index(op.f('ix_revisions_article_id'), table_name='revisions')
    op.drop_table('revisions')
    
    op.drop_table('article_tags')
    op.drop_table('article_categories')
    
    op.drop_index(op.f('ix_articles_author_id'), table_name='articles')
    op.drop_index(op.f('ix_articles_slug'), table_name='articles')
    op.drop_table('articles')
    
    op.drop_index(op.f('ix_tags_slug'), table_name='tags')
    op.drop_table('tags')
    
    op.drop_index(op.f('ix_categories_parent_id'), table_name='categories')
    op.drop_index(op.f('ix_categories_slug'), table_name='categories')
    op.drop_table('categories')
    
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
