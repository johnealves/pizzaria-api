from sqlalchemy.orm import Session

from db.database import SessionLocal
from seeds.seed_products import seed_products


def run():
    session: Session = SessionLocal()

    try:
        seed_products(session)
    finally:
        session.close()


if __name__ == "__main__":
    run()
