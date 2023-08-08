recipes_list = []
ingredients_list = []

def take_recipe():
  name = input("Enter the name of your recipe: ")
  cooking_time = int(input("Enter the cooking time: "))
  ingredients = input("Enter the ingredients: ").split(", ")

  recipe = {'name': name, 'cooking_time': cooking_time, 'ingredients': ingredients}

  return recipe

n = int(input("How many recipes would you like to enter?: "))

for i in range(n):
  recipe = take_recipe()
  for ingredient in recipe['ingredients']:
    if not ingredient in ingredients_list:
      ingredients_list.append(ingredient)
  recipes_list.append(recipe)

for recipe in recipes_list:
  if recipe['cooking_time'] < 10 and len(recipe['ingredients']) < 4:
    recipe['difficulty'] = 'Easy'
  elif recipe['cooking_time'] < 10 and len(recipe['ingredients']) >= 4:
    recipe['difficulty'] = 'Medium'
  elif recipe['cooking_time'] >= 10 and len(recipe['ingredients']) < 4:
    recipe['difficulty'] = 'Intermediate'
  elif recipe['cooking_time'] >= 10 and len(recipe['ingredients']) >= 4:
    recipe['difficulty'] = 'Hard'

for recipe in recipes_list:
  print('Recipe:', recipe['name'])
  print('Cooking time:', recipe['cooking_time'], 'minutes')
  print('Ingredients:')
  for ingredient in recipe['ingredients']:
    print(ingredient)
  print('Difficulty:', recipe['difficulty'])

def print_ingredients():
  ingredients_list.sort()
  print('All Ingredients')
  print('_ _ _ _ _ _ _ _ _')
  for ingredient in ingredients_list:
    print(ingredient)

print_ingredients()