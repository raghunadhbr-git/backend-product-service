import pytest
from app import create_app
from app.extensions import db


@pytest.fixture
def app():
    app = create_app(testing=True)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()



# ⚠️ Do NOT use relative imports here
# ❌ from ..app import create_app
# ✔ from app import create_app

# Step 1: Sanity check (VERY IMPORTANT)
# Run this before pytest:
# python -c "import app; print(app)"

# Step 2: Check for import errors
# Step : Run pytest again
# pytest

# Step 3: Check test coverage
# Then coverage:
# pytest --cov=app --cov-report=term-missing


# =================================================
# Overall Summary:-
# =================================================
# 🧠 Why this worked in auth-service but not here
# Auth-service already had one of these:
# •	pytest.ini with pythonpath = .
# •	or PYTHONPATH implicitly set
# Product-service didn’t — that’s it.
# No code bug. No Flask issue.




