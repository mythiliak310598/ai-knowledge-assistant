from app.db.database import engine

try:
    # with automatically opens/manages a resource and safely closes/cleans it up 
    # after use, while try/except handles errors.

    # # Without with
    # file = open("data.txt", "r")
    # content = file.read()
    # file.close()
    # # With with
    # with open("data.txt", "r") as file:
    #     content = file.read()
    # # File is automatically closed here
    with engine.connect() as connection:
        print("Database connection successful!")
except Exception as e:
    print(f"Database connection failed: {e}")