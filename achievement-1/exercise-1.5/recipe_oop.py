class Recipe:
  all_ingredients = []

  def __init__(self, name, ingredients, cooking_time):
    self.name = name
    self.ingredients = []
    self.cooking_time = int(0)
    self.difficulty = ""

  def calculate_difficulty(self, cooking_time, ingredients):
    # number_of_ingredients = len(self.ingredients)
    if (cooking_time < 10) and (len(ingredients) < 4):
      difficulty_level = 'Easy'
    elif (cooking_time < 10) and (len(ingredients) >= 4):
      difficulty_level = 'Medium'
    elif (cooking_time >= 10) and (len(ingredients) <4):
      difficulty_level = 'Intermediate'
    elif (cooking_time >= 10) and (len(ingredients) >= 4):
      difficulty_level = 'Hard'
    else:
      print('Something went wrong, try again')

    return difficulty_level

  def add_ingredients(self, *args):
    self.ingredients = args
    self.update_all_ingredients()

  def search_ingredient(self, ingredient, ingredients):
    if (ingredient in ingredients):
      return True
    else:
      return False

  def update_all_ingredients(self):
    for ingredient in self.ingredients:
      if ingredient not in self.all_ingredients:
        self.all_ingredients.append(ingredients)
  
  def recipe_search(self, recipes_list, ingredient):
    data = recipes_list
    search_term = ingredient
    for recipe in data:
      if self.search_ingredient(search_term, recipe.ingredients):
        print(recipe)

  def get_name(self):
    return self.name

  def get_ingredients(self):
    print('\nIngredients: ')
    for ingredient in self.ingredients:
      print('-' + str(ingredient))

  def get_cooking_time(self):
    return self.cooking_time
  
  def get_difficulty(self):
    difficulty = self.calculate_difficulty(self.cooking_time, self.ingredients)
    output = 'Difficulty: ' + str(self.cooking_time)
    self.difficulty = difficulty
    return output

  def set_name(self, name):
    self.name = name

  def set_cooking_time(self, cooking_time):
    self.cooking_time = cooking_time

  def __str__(self):
    output = 'Name: ' + self.name + '\n'
    'Cooking Time: ' + str(self.cooking_time) + '\n'
    'Ingredients: ' + str(self.ingredients) + '\n'
    'Difficulty: ' + str(self.difficulty) + '\n'
    for ingredient in self.ingredients:
      output =+ '- ' + ingredient + '\n'
      return output

  
recipes_list = []


tea = Recipe('Tea')
tea.add_ingredients('Tea Leaves', 'Water', 'Sugar')
tea.set_cooking_time(5)
tea.get_difficulty()

recipes_list.append(tea)

for recipe in recipes_list:
  print(recipe)