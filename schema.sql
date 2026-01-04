CREATE TABLE user (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(30) UNIQUE NOT NULL,
    email VARCHAR(60) UNIQUE NOT NULL,
    hashed_password VARCHAR(60) NOT NULL,
    type CHAR NOT NULL
);

CREATE TABLE recipe (
    recipe_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    title VARCHAR NOT NULL,
    ingredients VARCHAR NOT NULL,
    instructions VARCHAR NOT NULL,
    description VARCHAR,
    category CHAR,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(user_id)
);

CREATE TABLE comment (
    comment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    recipe_id INTEGER,
    comment_text VARCHAR NOT NULL,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(user_id),
    FOREIGN KEY (recipe_id) REFERENCES recipe(recipe_id)
);

CREATE TABLE rating (
    rating_id INTEGER PRIMARY KEY AUTOINCREMENT,
    recipe_id INTEGER,
    user_id INTEGER,
    value INTEGER CHECK (value >= 1 AND value <= 5),
    FOREIGN KEY (recipe_id) REFERENCES recipe(recipe_id),
    FOREIGN KEY (user_id) REFERENCES user(user_id)
    UNIQUE(recipe_id, user_id)
);

CREATE TABLE collection (
    collection_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    name VARCHAR NOT NULL,
    description VARCHAR,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(user_id)
);

CREATE TABLE recipe_collection (
    recipe_id INTEGER,
    collection_id INTEGER,
    added  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (recipe_id, collection_id),
    FOREIGN KEY (recipe_id) REFERENCES recipe(recipe_id),
    FOREIGN KEY (collection_id) REFERENCES collection(collection_id)
);
