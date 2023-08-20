import pickle

def display_recipe(recipe):
  print('Name: ', recipe['name'])
  print('Cooking time: ', recipe['cooking_time'])
  print('Ingredients: ', ', '.join(recipe['ingredients']))
  print('Difficulty: ', recipe['difficulty'])

def search_ingredients(data):
  ingredients_list = data['all_ingredients']
  index_of_ingredient = list(enumerate(ingredients_list, 1))

  for ingredient in index_of_ingredient:
    print('No.', ingredient[0], ' - ', ingredient[1])

  try:
    chosen_ingredient = int(input('Enter the number of your chosen ingredient: '))
    index = chosen_ingredient - 1
    ingredient_searched = ingredients_list[index]
  except IndexError:
    print('The number you entered does not appear on the ingredient list.')
  except:
    print('Oops, either the ingredient does not exist or it ran off.')
  else:
    for recipe in data['recipes_list']:
      for recipe_ingredient in recipe['ingredients']:
        if(recipe_ingredient == ingredient_searched):
          print('The recipe has these ingredients:')
          display_recipe(recipe)

filename = input('Enter the filename where the recipe is stored: ')

try:
  recipes_file = open(filename, 'rb')
  data = pickle.load(recipes_file)
except FileNotFoundError:
  print('File does not exist in this directory')
  data = {'recipes_list': [], 'all_ingredients': []}
except:
  print('An unexpected error has occurred')
  data = {'recipes_list': [], 'all_ingredients': []}
else:
  search_ingredients(data)
finally:
  recipes_file.close()