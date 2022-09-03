# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['xosc_dl.py'],
             binaries=[],
             datas=[('assets/gui/icons/controllers/*.png', './assets/gui/icons/controllers/'),
                    ('assets/gui/icons/category/*.png', './assets/gui/icons/category/'),
                    ('assets/gui/*.png', './assets/gui/'),
                    ('assets/themes/*.qss', './assets/themes/'),
                    ('assets/gui/icons/*.gif', './assets/gui/icons/'),
                    ('assets/gui/icons/*.png', './assets/gui/icons/'),
                    ('assets/gui/icons/status/*.png', './assets/gui/icons/status')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='xosc_dl',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False, icon='oscicon.ico')
