"""users and notes tables

Revision ID: b97b444a7a41
Revises: 
Create Date: 2020-07-18 20:25:17.275460

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b97b444a7a41'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('notes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('userid', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(length=100), nullable=True),
    sa.Column('folder', sa.String(length=100), nullable=True),
    sa.Column('contents', sa.Text(), nullable=True),
    sa.Column('status', sa.String(length=10), nullable=True),
    sa.Column('ts', sa.BigInteger(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_notes_folder'), 'notes', ['folder'], unique=False)
    op.create_index(op.f('ix_notes_userid'), 'notes', ['userid'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('public_id', sa.String(length=50), nullable=True),
    sa.Column('guserid', sa.String(length=50), nullable=True),
    sa.Column('gmail', sa.String(length=120), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_gmail'), 'users', ['gmail'], unique=True)
    op.create_index(op.f('ix_users_guserid'), 'users', ['guserid'], unique=True)
    op.create_index(op.f('ix_users_public_id'), 'users', ['public_id'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_public_id'), table_name='users')
    op.drop_index(op.f('ix_users_guserid'), table_name='users')
    op.drop_index(op.f('ix_users_gmail'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_notes_userid'), table_name='notes')
    op.drop_index(op.f('ix_notes_folder'), table_name='notes')
    op.drop_table('notes')
    # ### end Alembic commands ###