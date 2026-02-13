from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.util.config_loader import Config

# Create database engine
engine = create_engine(Config.value('SQLALCHEMY_APPOINTMENT_URI'), echo=False)

# Create database session
Session = sessionmaker(bind=engine)
session = Session()

# Create database engine
stack_optimizer_engine = create_engine(Config.value('SQLALCHEMY_STACK_OPTIMIZER_URI'), echo=False)

# Create database session
StackOptimizerSession = sessionmaker(bind=stack_optimizer_engine)
stack_optimizer_session = StackOptimizerSession()
