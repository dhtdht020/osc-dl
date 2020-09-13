# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['xosc_dl.py'],
             binaries=[],
             datas=[('assets/gui/windowicon.png', './assets/gui/'),
                    ('assets/gui/icons/add-fake-listing.png', './assets/gui/icons/'),
                    ('assets/gui/icons/announcement-banner.png', './assets/gui/icons/'),
                    ('assets/gui/icons/clear-log.png', './assets/gui/icons/'),
                    ('assets/gui/icons/close-shop.png', './assets/gui/icons/'),
                    ('assets/gui/icons/enable-log.png', './assets/gui/icons/'),
                    ('assets/gui/icons/experimental.png', './assets/gui/icons/'),
                    ('assets/gui/icons/update-wizard.png', './assets/gui/icons/')],
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
          console=False , icon='oscicon.ico')
