# -*- mode: python -*-

block_cipher = None

added_files = [
         ( 'assets', 'assets' ),
         ( 'ESP32', 'ESP32' ),
         ( 'kivymd/fonts', 'kivymd/fonts' ),
         ( 'kivymd/images', 'kivymd/images' ),
         ( '*.json', '.' ),
         ( '*.kv', '.' )
         ]

a = Analysis(['main.py'],
             pathex=['C:\\git_repos\\PolyExpressive\\app\\kivy'],
             binaries=[],
             datas=added_files,
             hiddenimports=['plyer.platforms.win.filechooser'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='polyexpressive',
          debug=False,
          strip=False,
          upx=True,
          console=False , icon='assets\\poly.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='polyexpressive')
