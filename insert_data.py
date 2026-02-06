import sqlite3


def insert_data():
    connection = sqlite3.connect('database/recipes.db')
    connection.row_factory = sqlite3.Row

    try:
        connection.execute('''
                INSERT INTO user (username, email, hashed_password, type)
                VALUES
                ('Mark123', 'mark@gmail.com', 'password123', 'user'),
                ('Jane_cook', 'jane@gmail.com', 'password111', 'user'),
                ('MasterCook', 'master@gmail.com', 'password222', 'user')               
        ''')
        print('inserted users')

        connection.execute('''
            INSERT OR IGNORE INTO recipe (user_id, title, ingredients, instructions, description, category) 
            VALUES 
            (1, 'Classic Chocolate Chip Cookies', 
            '- 2 ¼ cups all-purpose flour\n- 1 tsp baking soda\n- 1 tsp salt\n- 1 cup butter, softened\n- ¾ cup granulated sugar\n- ¾ cup packed brown sugar\n- 2 large eggs\n- 2 cups chocolate chips',
            '1. Preheat oven to 375°F (190°C)\n2. Mix flour, baking soda, and salt in small bowl\n3. Beat butter, sugars, and vanilla in large bowl\n4. Add eggs one at a time\n5. Gradually beat in flour mixture\n6. Stir in chocolate chips\n7. Drop by rounded tablespoons onto ungreased baking sheets\n8. Bake 9-11 minutes or until golden brown',
            'The best soft and chewy chocolate chip cookies', 'Dessert'),
            
            (1, 'Vegetable Stir Fry',
            '- 2 cups mixed vegetables (bell peppers, broccoli, carrots)\n- 2 tbsp soy sauce\n- 1 tbsp olive oil\n- 2 cloves garlic, minced\n- 1 tsp ginger, grated\n- 1 tbsp sesame oil',
            '1. Heat olive oil in large pan or wok\n2. Add garlic and ginger, stir for 30 seconds\n3. Add vegetables and stir fry for 5-7 minutes\n4. Add soy sauce and sesame oil\n5. Cook for another 2 minutes\n6. Serve hot with rice',
            'Quick and healthy vegetable stir fry', 'Main Course'),
            
            (2, 'Banana Smoothie',
            '- 2 ripe bananas\n- 1 cup milk\n- 1 cup yogurt\n- 2 tbsp honey\n- 1 tsp vanilla extract\n- Handful of ice cubes',
            '1. Peel bananas and break into chunks\n2. Add all ingredients to blender\n3. Blend until smooth\n4. Pour into glasses and serve immediately',
            'Creamy and refreshing banana smoothie', 'Beverage'),

            (3, 'Spaghetti Carbonara',
                '- 1 lb spaghetti\n- 4 large eggs\n- 1 cup grated Parmesan cheese\n- 8 slices bacon, diced\n- 4 cloves garlic, minced\n- Salt and black pepper to taste',
                '1. Cook spaghetti according to package directions\n2. Cook bacon until crispy, add garlic\n3. Whisk eggs and Parmesan together\n4. Drain pasta, reserving 1 cup pasta water\n5. Quickly mix hot pasta with egg mixture\n6. Add bacon and season with pepper',
                'Creamy Italian pasta classic', 'Main Course')  
        ''')
        print('inserted recipes')

        connection.execute('''
                INSERT INTO rating (recipe_id, user_id, value)
                VALUES
                (1, 2, 5),
                (1, 3, 4),
                (2, 1, 5),
                (3, 1, 4),
                (4, 2, 5)
        ''')
        print('inserted ratings')

        connection.execute('''
                INSERT INTO comment (user_id, recipe_id, comment_text)
                VALUES
                (2, 1, 'A really good recipe for cookies, everyone that tried them loved them!'),
                (3, 1, 'I love this recipe!!'),
                (1, 3, 'Smoothie tasted amazing'),
                (2, 4, 'This pasta was perfect for datenight!!! Me and my wife loved it')
        ''')
        
        print('inseted comments')

        connection.execute('''
                INSERT INTO collection (user_id, name, description)
                VALUES
                (1, 'Great Desserts', 'Sharing dessert recipes I love to make'),
                (2, 'Quick Dinners', 'Need a quick and easy dinner? Youve come to the right place'),
                (3, 'Italian Family Recipes', 'Recipes passed down through my family! The best itailian foods you can make.')
        ''')
        print('Inserted collections')

        connection.execute('''
                INSERT INTO recipe_collection (recipe_id, collection_id)
                VALUES
                (1, 1),
                (3, 1),
                (2, 2),
                (4, 3)           
        ''')
        print('added recipes to collections')

        connection.commit()
        print('Data inserted successfully')
    except Exception as e:
        print(f'Error {e}')
        connection.rollback()
    finally:
        connection.close()
    
if __name__ == '__main__':
    insert_data()