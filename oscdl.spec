# -*- mode: python ; coding: utf-8 -*-
import os

datas = [('assets/gui/icons/peripherals/light/*.png', './assets/gui/icons/peripherals/light/'),
         ('assets/gui/icons/peripherals/dark/*.png', './assets/gui/icons/peripherals/dark/'),
         ('assets/gui/icons/peripherals/README.md', './assets/gui/icons/peripherals/'),
         ('assets/gui/icons/platforms/*.png', './assets/gui/icons/platforms/'),
         ('assets/gui/icons/category/*.png', './assets/gui/icons/category/'),
         ('assets/gui/*.png', './assets/gui/'),
         ('assets/gui/icons/*.gif', './assets/gui/icons/'),
         ('assets/gui/icons/*.png', './assets/gui/icons/'),
         ('assets/gui/icons/status/*.png', './assets/gui/icons/status')]

if os.path.exists('build_info.json'):
    datas.append(('build_info.json', '.'))

# Qt and PIL components that OSCDL doesn't use
excludes = ['PySide6.QtQml',
            'PySide6.QtQuick',
            'PySide6.QtNetwork',
            'PySide6.QtOpenGL',
            'PySide6.QtPdf',
            'PIL._avif']

a = Analysis(['oscdl.py'],
             binaries=[],
             datas=datas,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=excludes,
             noarchive=False)

# Remove the software OpenGL fallback renderer, which is very large and not needed by a QtWidgets app,
# and the Qt virtual keyboard and PDF plugins along with the QML machinery only they depend on
excluded_binaries = ('opengl32sw.dll',
                     'qtvirtualkeyboardplugin.dll',
                     'Qt6VirtualKeyboard.dll',
                     'qpdf.dll',
                     'Qt6Pdf.dll',
                     'Qt6Quick.dll',
                     'Qt6Qml.dll',
                     'Qt6QmlMeta.dll',
                     'Qt6QmlModels.dll',
                     'Qt6QmlWorkerScript.dll',
                     'Qt6OpenGL.dll',
                     'Qt6Network.dll')
a.binaries = [binary for binary in a.binaries if not binary[0].endswith(excluded_binaries)]

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
