import pickle

def take_recipe():
  name = input("Enter the name of your recipe: ")
  cooking_time = int(input("Enter the cooking time: "))
  ingredients = input("Enter the ingredients: ").split(", ")

  recipe = {'name': name, 'cooking_time': cooking_time, 'ingredients': ingredients}

  recipe['Difficulty'] = calc_difficulty(recipe)

  return recipe


def calc_difficulty(recipe):
  if recipe['cooking_time'] < 10 and len(recipe['ingredients']) < 4:
    difficulty = 'Easy'
  if recipe['cooking_time'] < 10 and len(recipe['ingredients']) >= 4:
    difficulty = 'Medium'
  if recipe['cooking_time'] >= 10 and len(recipe['ingredients']) < 4:
    difficulty = 'Intermediate'
  if recipe['cooking_time'] >= 10 and len(recipe['ingredients']) >= 4:
    difficulty = 'Hard'

  return difficulty

recipes_list = []
all_ingredients = []

filename = input('Enter your recipe filename: ')

try:
  recipes_file = open(filename, 'rb')
  data = pickle.load(recipes_file)
except FileNotFoundError:
  print('File not found. Creating a new file.')
  data = {'recipes_list': [], 'all_ingredients': []}
except:
  print('Unexpected error. Creating a new file. ')
  data = {'recipes_list': [], 'all_ingredients': []}
else:
  recipes_files.close()
finally:
  recipes_list = data['recipes_list']
  all_ingredients = data['all_ingredients']

num = int(input('How many recipes would you like to enter?: '))

for i in range(num):
  recipe = take_recipe()
  print(recipe)

  for ingredients in recipe['ingredients']:
    if ingredients not in all_ingredients:
      all_ingredients.append(ingredients)

  recipes_list.append(recipe)

data = {'recipes_list': recipes_list, 'all_ingredients': all_ingredients}

new_file_name = input('Enter a name for your file.')
with open(new_file_name, 'wb') as f:
  pickle.dump(data, f)