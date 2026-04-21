from backend.app.db.database import engine
from backend.app.models.user_model import Base

print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Done!")