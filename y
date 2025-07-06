from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {'packages': [], 'excludes': []}

base = 'gui'

executables = [
    Executable('C:\\Users\\asura\\PycharmProjects\\Meal planner app\\.venv\\Meal Planner With Ui assembling.py', base=base, target_name = 'MealPlanner')
]

setup(name='Meal Planner',
      version = '0.1',
      description = 'Meal Planning App',
      options = {'build_exe': build_options},
      executables = executables)
