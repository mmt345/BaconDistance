import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

"""
This Module initializes the SQLalchemy engine and session.
It uses DATABASE_URL from environment variables (Provided in the docker-compose file).
I enabled the pool_pre_ping to revive the connection if it had died.
"""
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

local_session = sessionmaker(bind=engine)