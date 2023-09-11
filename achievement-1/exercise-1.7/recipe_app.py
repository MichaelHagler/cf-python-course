from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import Integer, String
from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
engine = create_engine("mysql://cf-python:password@localhost/my_database")

Base = declarative_base()

class Recipe(Base):
  __tablename__ = 'final_recipes'
  id = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String(50))
  ingredients = Column(String(255))
  cooking_time = Column(Integer)
  difficulty = Column(String(20))

  def __repr__(self):
    return f"<Recipe(id={self.id}, name='{self.name}', difficulty='{self.difficulty}')>"

  def __str__(self):
    return f"\nRecipe ID: {self.id}\n{'-'*30}\nName: {self.name}\nDifficulty: {self.difficulty}\nCooking Time: {self.cooking_time} minutes\n{'-'*30}\nIngredients:\n{self.ingredients}\n{'-'*30}"

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def calc_difficulty(cooking_time, recipe_ingredients):
  print('Run the calc_difficulty with: ', cooking_time, recipe_ingredients)

  if (cooking_time < 10) and (len(recipe_ingredients) < 4):
    difficulty_level = 'Easy'
  elif (cooking_time < 10) and (len(recipe_ingredients) >= 4):
    difficulty_level = 'Medium'
  elif (cooking_time >= 10) and (len(recipe_ingredients) < 4):
    difficulty_level = 'Intermediate'
  elif (cooking_time >= 10) and (len(recipe_ingredients) >= 4):
    difficulty_level = 'Hard'
  else:
    print('Something bad happened, please try again')

  print('Difficulty level: ', difficulty_level)
  return difficulty_level

def return_ingredients_as_list():
  recipes_list = session.query(Recipe).all()
  for recipe in recipes_list:
    print('Recipe: ', recipe)
    print('recipe.ingredients: ', recipe.ingredients)
    recipe_ingredients_list = recipe.ingredients.split(', ')
    print(recipe_ingredients_list)

def create_recipe():
  recipe_ingredients = []

  correct_input_name = False
  while correct_input_name == False:
    name = input('\nEnter recipe name: ')
    if len(name) < 50:
      correct_input_name = True

      correct_input_cooking_time = False 
      while correct_input_cooking_time == False:
        cooking_time = input('\nEnter cooking time: ')
        if cooking_time.isnumeric() == True:
          correct_input_cooking_time = True
        else: print('Please enter a number')

    else:
      print('Please enter a name that contains less than 50 characters')
    correct_input_number = False
    while correct_input_number == False:
      ingredient_num = input('How many ingredients do you want to enter?: ')
      if ingredient_num.isnumeric() == True:
        correct_input_number = True

        for _ in range(int(ingredient_num)):
          ingredient = input('Enter an ingredient: ')
          recipe_ingredients.append(ingredient)

      else:
        correct_input_number = False
        print('Please enter a positive number')

  recipe_ingredient_str = ', '.join(recipe_ingredients)
  print(recipe_ingredient_str)
  difficulty = calc_difficulty(int(cooking_time), recipe_ingredients)

  recipe_entry = Recipe(
    name = name,
    cooking_time = int(cooking_time),
    ingredients = recipe_ingredients_str,
    difficulty = difficulty
  )

  print(recipe_entry)

  session.add(recipe_entry)
  session.commit()

  print('Recipe saved!')

def view_all_recipes():
  all_recipes = []
  all_recipes = session.query(Recipe).all()

  if len(all_recipes) == 0:
    print('recipe not found')
    return None

  else:
    print('\nShowing all Recipes')
    print('====================')

    for recipe in all_recipes:
      print(recipe)

def search_by_ingredients():
  if session.query(Recipe).count() == 0:
    print('recipe does not exist')
    return None

  else:
    results = session.query(Recipe.ingredients).all()
    print('results: ', results)

    all_ingredients = []

    for recipe_ingredients_list in results:
      for recipe_ingredients in recipe_ingredients_list:
        recipe_ingredient_split = recipe_ingredients.split(', ')
        all_ingredients.extend(recipe_ingredient_split)

    print('all_ingredients after the loop: ', all_ingredients)
    all_ingredients = list(dict.fromkeys(all_ingredients))
    all_ingredients_list = list(enumerate(all_ingredients))

    print('\nAll ingredients list')
    print('====================')

    for index, tup in enumerate(all_ingredients_list):
      print(str(tup[0]+1) + '. ' + tup[1])

    try:
      ingredient_searched_num = input(
        '\nEnter the number(or numbers with a space between) of the corresponding ingredient from the list'
      )
      ingredients_num_list_searched = ingredient_searched_num.split(' ')

      ingredient_searched_list = []
      for ingredient_searched_num in ingredients_num_list_searched:
        ingredient_searched_index = int(ingredient_searched_num) -1
        ingredient_searched = all_ingredients_list[ingredient_searched_index][1]

        ingredient_searched_list.append(ingredient_searched)

      print('\nYou selected these ingredients: ', ingredient_searched_list)

      conditions = []
      for ingredient in ingredient_searched_list:
        like_term = '%' + ingredient + '%'
        condition = Recipe.ingredients.like(like_term)
        conditions.append(condition)
      print('conditions: ', conditions)
      searched_recipes = session.query(Recipe).filter(*conditions).all()

      print(searched_recipes)

    except:
      print('Oops, something went wrong. Make sure to select a number from the list')

    else:
      print('searched_recipes: ')
      for recipe in searched_recipes:
        print(recipe)

def edit_recipe():
  if session.query(Recipe).count() == 0:
    print('There are no recipes to edit')
    return None

  else: 
    results = session.query(Recipe).with_entities(Recipe.id, Recipe.name).all()
    print('results: ', results)
    print('List of available recipes: ')
    for recipe in results:
      print('\nID: ', recipe[0])
      print('Name: ', recipe[1])

    recipe_id_for_edit = int(
      input('\nEnter the ID of the recipe you want to edit: '))

    print(session.query(Recipe).with_entities(Recipe.id).all())

    recipes_id_tup_list = session.query(Recipe).with_entities(Recipe.id).all()
    recipes_id_list = []

    for recipe_tup in recipes_id_tup_list:
      print(recipe_tup[0])
      recipes_id_list.append(recipe_tup[0])

    print(recipes_id_list)

    if recipe_id_for_edit not in recipes_id_list:
      print('Not in the ID list, please try again later')
    else:
      print('continuing')
      recipe_to_edit = session.query(Recipe).filter(Recipe.id == recipe_id_for_edit_.one())

      print('\nWARNING: You are about to edit the following recipe: ')
      print(recipe_to_edit)
      column_for_update = int(input(
        '\nEnter the corresponding number to the item you want to edit: '
      ))
      updated_value = input('\nEnter your edit here: ')
      print('Choice: ', updated_value)

      if column_for_update == 1:
        print('Updating name')
        session.query(Recipe).filter(Recipe.id == recipe_id_for_edit).update(
          {Recipe.name: updated_value}
        )
        session.commit()
      
      elif column_for_update == 2:
        print('Updating cooking time')
        session.query(Recipe).filter(Recipe.id == recipe_id_for_edit).update(
          {Recipe.cooking_time: updated_value}
        )
        session.commit()
      
      elif column_for_update == 3:
        print('Updating ingredients')
        session.query(Recipe).filter(Recipe.id == recipe_id_for_edit).update(
          {Recipe.ingredients: updated_value}
        )
        session.commit()

      else:
        print('Wrong input, please try again')
      updated_difficulty = calc_difficulty(
        recipe_id_for_edit.cooking_time, recipe_id_for_edit.ingredients
      )
      print('updated_difficulty: ', updated_difficulty)
      recipe_id_for_edit.difficulty = updated_difficulty
      session.commit()
      print('Update saved!')

def delete_recipe():
  if session.query(Recipe).count() == 0:
    print('There is nothing to delete')
    return None
  else:
    results = session.query(Recipe).with_entities(
      Recipe.id, Recipe.name).all()
    print('results: ', results)
    print('List of available recipes:')
    for recipe in results:
      print('\nID: ', recipe[0])
      print('Name: ', recipe[1])
    recipe_id_for_deletion = (
      input('\nEnter the ID of the recipe you wish to delete: '))

    recipe_to_be_deleted = session.query(Recipe).filter(
      Recipe.id == recipe_id_for_deletion).one()

    print('\nWARNING: you are about to delete this recipe: ')
    print(recipe_to_be_deleted)
    deletion_confirmed = input('\nTo confirm that you want to delete recipe enter (y/n): ')
    if deletion_confirmed == 'y':
      session.delete(recipe_to_be_deleted)
      session.commit()
      print('\nRecipe successfully deleted from the database.')
    else:
      return None

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
    print('   5. view all recipes')
    print("Type 'quit' to exit")
    choice = input('\nYour choice: ')

    if choice == '1':
      create_recipe() 
    elif choice =='2':
      search_by_ingredients()
    elif choice == '3':
      edit_recipe()
    elif choice == '4':
      delete_recipe()
    elif choice == '5':
      view_all_recipes()
    else:
      if choice == 'quit':
        print('goodbye\n')
      else:
        print('Invalid entry, try again')

main_menu()
session.close()