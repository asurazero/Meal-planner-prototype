from kivy_deps import sdl2, glew
# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:\\Users\\asura\\PycharmProjects\\Meal planner app\\src\\mealplanner.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Users\\asura\\PycharmProjects\\Meal planner app\\src\\addedbread.py', '.'), ('C:\\Users\\asura\\PycharmProjects\\Meal planner app\\src\\addedbreakfast.py', '.'), ('C:\\Users\\asura\\PycharmProjects\\Meal planner app\\src\\addeddesserts.py', '.'), ('C:\\Users\\asura\\PycharmProjects\\Meal planner app\\src\\addedentree.py', '.'), ('C:\\Users\\asura\\PycharmProjects\\Meal planner app\\src\\addedfish.py', '.'), ('C:\\Users\\asura\\PycharmProjects\\Meal planner app\\src\\addedmexicanfd.py', '.'), ('C:\\Users\\asura\\PycharmProjects\\Meal planner app\\src\\addedsalad.py', '.'), ('C:\\Users\\asura\\PycharmProjects\\Meal planner app\\src\\addedsides.py', '.'), ('C:\\Users\\asura\\PycharmProjects\\Meal planner app\\src\\fnv.jpg', '.'), ('C:\\Users\\asura\\PycharmProjects\\Meal planner app\\src\\fnv1.jpg', '.'), ('C:\\Users\\asura\\PycharmProjects\\Meal planner app\\src\\fnv2.jpg', '.'), ('C:\\Users\\asura\\PycharmProjects\\Meal planner app\\src\\fnv3.jpg', '.'), ('C:\\Users\\asura\\PycharmProjects\\Meal planner app\\src\\fnv4.jpg', '.'), ('C:\\Users\\asura\\PycharmProjects\\Meal planner app\\src\\Help.txt', '.'), ('C:\\Users\\asura\\PycharmProjects\\Meal planner app\\src\\Meal Plan Gen.txt', '.'), ('C:\\Users\\asura\\PycharmProjects\\Meal planner app\\src\\Meal Plan.txt', '.'), ('C:\\Users\\asura\\PycharmProjects\\Meal planner app\\src\\morekivy.kv', '.'), ('C:\\Users\\asura\\PycharmProjects\\Meal planner app\\src\\MP1.png', '.'), ('C:\\Users\\asura\\PycharmProjects\\Meal planner app\\src\\MP1.txt', '.'), ('C:\\Users\\asura\\PycharmProjects\\Meal planner app\\src\\MP2.png', '.'), ('C:\\Users\\asura\\PycharmProjects\\Meal planner app\\src\\MP2.txt', '.'), ('C:\\Users\\asura\\PycharmProjects\\Meal planner app\\src\\MP3.png', '.'), ('C:\\Users\\asura\\PycharmProjects\\Meal planner app\\src\\MP3.txt', '.'), ('C:\\Users\\asura\\PycharmProjects\\Meal planner app\\src\\MP4.png', '.'), ('C:\\Users\\asura\\PycharmProjects\\Meal planner app\\src\\MP4.txt', '.'), ('C:\\Users\\asura\\PycharmProjects\\Meal planner app\\src\\MP5.png', '.'), ('C:\\Users\\asura\\PycharmProjects\\Meal planner app\\src\\MP5.txt', '.'), ('C:\\Users\\asura\\PycharmProjects\\Meal planner app\\src\\datafiles', 'datafiles/'), ('C:\\Users\\asura\\PycharmProjects\\Meal planner app\\src\\recipebooks', 'recipebooks/'), ('C:\\Users\\asura\\PycharmProjects\\Meal planner app\\src\\recipes', 'recipes/'), ('C:\\Users\\asura\\PycharmProjects\\Meal planner app\\src\\shopping_list', 'shopping_list/')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)
a.datas += [('Code\morekivy.kv',""C:\\Users\\asura\\PycharmProjects\\Meal planner app\\src\morekivy.kv",'DATA')]

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='mealplanner',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='mealplanner',
)
