# -*- mode: python ; coding: utf-8 -*-

datas = [('assets/gui/icons/peripherals/light/*.png', './assets/gui/icons/peripherals/light/'),
         ('assets/gui/icons/peripherals/dark/*.png', './assets/gui/icons/peripherals/dark/'),
         ('assets/gui/icons/peripherals/README.md', './assets/gui/icons/peripherals/'),
         ('assets/gui/icons/platforms/*.png', './assets/gui/icons/platforms/'),
         ('assets/gui/icons/category/*.png', './assets/gui/icons/category/'),
         ('assets/gui/*.png', './assets/gui/'),
         ('assets/gui/icons/*.gif', './assets/gui/icons/'),
         ('assets/gui/icons/*.png', './assets/gui/icons/'),
         ('assets/gui/icons/status/*.png', './assets/gui/icons/status')]

a = Analysis(['oscdl.py'],
             binaries=[],
             datas=datas,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             noarchive=False)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='oscdl',
          debug=False,
          strip=False,
          upx=True,
          console=False,
          icon='oscicon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='oscdl')
