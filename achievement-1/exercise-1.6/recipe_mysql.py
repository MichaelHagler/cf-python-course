import mysql.connector

conn = mysql.connector.connect(
  host = 'localhost', user = 'cf-python', passwd = 'password'
)

cursor = conn.cursor()

cursor.execute('CREATE DATABASE IF NOT EXISTS task_database')

cursor.execute('USE task_database')

cursor.execute('''CREATE TABLE IF NOT EXISTS Recipes(
id INT PRIMARY KEY AUTO_INCREMENT,
name VARCHAR(50),
ingredients VARCHAR(50),
cooking_time INT,
difficulty VARCHAR(20)
)''')

def main_menu(conn, cursor):
  choice = ''
  while (choice != 'quit'):
    print('\n======================')
    print('Main Menu')
    print('Pick a choice:')
    print('   1. Create a new recipe')
    print('   2. Search for a recipe by ingredient')
    print('   3. Update an existing recipe')
    print('   4. Delete a recipe')
    print("Type 'quit' to exit")
    choice = input('\nYour choice: ')

    if choice == '1':
      create_recipe(conn, cursor) 
    elif choice =='2':
      search_recipe(conn, cursor)
    elif choice == '3':
      update_recipe(conn, cursor)
    elif choice == '4':
      delete_recipe(conn, cursor)


def create_recipe(conn, cursor):
  recipe_ingredients = []
  name = str(input('\nEnter the name of the recipe: '))
  cooking_time = int(input('Enter cooking time: '))
  ingredient = input('Enter ingredients: ')
  recipe_ingredients.append(ingredient)
  difficulty = calc_difficulty(cooking_time, recipe_ingredients)
  sql_recipe_ingredients = ", ".join(recipe_ingredients)
  sql = 'INSERT INTO Recipes (name, ingredients, cooking_time, difficulty) VALUES (%s, %s, %s, %s)'
  val = (name, sql_recipe_ingredients, cooking_time, difficulty)

  cursor.execute(sql, val)
  conn.commit()
  print('Recipe saved!')

def calc_difficulty(cooking_time, recipe_ingredients):
  if (cooking_time < 10) and (len(recipe_ingredients) < 4):
    difficulty_level = 'Easy'
  elif (cooking_time < 10) and (len(recipe_ingredients) >= 4):
    difficulty_level = 'Medium'
  elif (cooking_time >= 10) and (len(recipe_ingredients) < 4):
    difficulty_level = 'Intermediate'
  elif (cooking_time >= 10) and (len(recipe_ingredients) >= 4):
    difficulty_level = 'Hard'
  else:
    print('something went wrong')

  return difficulty_level

def search_recipe(conn, cursor):
  all_ingredients = []
  cursor.execute('SELECT ingredients FROM Recipes')
  results = cursor.fetchall()

  for recipe_ingredients_list in results:
    for recipe_ingredients in recipe_ingredients_list:
      recipe_ingredient_split = recipe_ingredients.split(', ')
      all_ingredients.extend(recipe_ingredient_split)

  all_ingredients = list(dict.fromkeys(all_ingredients))

  all_ingredients_list = list(enumerate(all_ingredients))

  print('\nIngredient list:')

  for index, tup in enumerate(all_ingredients_list):
    print(str(tup[0] + 1) + '. ' + tup[1])

  try:
    ingredient_searched_num = input('\nEnter the number from the ingredient list above: ')

    ingredient_searched_index = int(ingredient_searched_num) - 1

    ingredient_searched = all_ingredients_list[ingredient_searched_index][1]

    print(ingredient_searched)
  
  except:
    print('Oops, something went wrong. Select the number from the ingredient list.')

  else:
    cursor.execute('SELECT * FROM Recipes WHERE ingredients LIKE %s', ('%' + ingredient_searched + '%', ))

    recipe_with_ingredient = cursor.fetchall()
    for row in recipe_with_ingredient:
      print('\nID: ', row[0])
      print('Name: ', row[1])
      print('Ingredients: ', row[2])
      print('Cooking Time: ', row[3])
      print('Difficulty: ', row[4])

def update_recipe(conn, cursor):
  view_all_recipes(conn, cursor)
  recipe_id_for_update = int(input('\nEnter the ID of the recipe you want to update: '))
  column_for_update = str(input('\nEnter the category you want to update(name, cooking_time, or ingredients): '))
  updated_value = input("\nEnter the new value for the recipe: ")
  print('Choice: ', updated_value)

  if column_for_update == 'name':
    cursor.execute('UPDATE Recipes SET name = %s WHERE id = %s', (updated_value, recipe_id_for_update))
    print('Update complete')

  elif column_for_update == 'cooking_time':
    cursor.execute('UPDATE Recipes SET cooking_time = %s WHERE id = %s', (updated_value, recipe_id_for_update))
    cursor.execute('SELECT * FROM Recipes WHERE id = %s', (recipe_id_for_update, )) 
    result_recipe_for_update = cursor.fetchall()

    name = result_recipe_for_update[0][1]
    recipe_ingredients = tuple(result_recipe_for_update[0][2].split(', '))
    cooking_time = result_recipe_for_update[0][3]

    updated_difficulty = calc_difficulty(cooking_time, recipe_ingredients)
    print('Updated difficulty: ', updated_difficulty)
    cursor.execute('UPDATE Recipes SET difficulty = %s WHERE id = %s', (updated_difficulty, recipe_id_for_update))
    print('Update complete')

  elif column_for_update == 'ingredients':
    cursor.execute('UPDATE Recipes SET ingredients = %s WHERE id = %s', (updated_value, recipe_id_for_update))
    cursor.execute('SELECT * FROM Recipes WHERE id = %s', (recipe_id_for_update, ))
    result_recipe_for_update = cursor.fetchall()

    print('result_recipe_for_update: ', result_recipe_for_update)

    name = result_recipe_for_update[0][1]
    recipe_ingredients = tuple(result_recipe_for_update[0][2].split(', '))
    cooking_time = result_recipe_for_update[0][3]
    difficulty = result_recipe_for_update[0][4]

    updated_difficulty = calc_difficulty(cooking_time, recipe_ingredients)
    print('Updated difficulty: ', updated_difficulty)
    cursor.execute('UPDATE Recipes SET difficulty = %s WHERE id = %s', (updated_difficulty, recipe_id_for_update))
    print('Update complete')

    conn.commit()

def delete_recipe(conn, cursor):
  view_all_recipes(conn, cursor)
  recipe_id_for_deletion = (input('\nEnter ID of the recipe you want to delete: '))
  cursor.execute('DELETE FROM Recipes WHERE id = (%s)', (recipe_id_for_deletion, ))

  conn.commit()
  print('\nRecipe deleted')

def view_all_recipes(conn, cursor):
  print('\nShowing all recipes')
  print('====================')

  cursor.execute('SELECT * FROM Recipes')
  results = cursor.fetchall()

  for row in results:
    print('\nID: ', row[0])
    print('Name: ', row[1])
    print('Ingredients: ', row[2])
    print('Cooking Time: ', row[3])
    print('Difficulty: ', row[4])



main_menu(conn, cursor)