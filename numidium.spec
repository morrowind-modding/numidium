import shutil
import tomlkit

print("Cleaning dist directory...")
shutil.rmtree("dist", ignore_errors=True)

# -- Begin PyInstaller --

block_cipher = None

a = Analysis(
    ["numidium\\__main__.py"],
    pathex=[],
    binaries=[],
    datas=[
        ("numidium/ui/icons/*.svg", "numidium/ui/icons/"),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Remove some stuff we don't care about.
a.binaries -= TOC([("opengl32sw.dll", None, None)])

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="numidium",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[
        # "_asyncio.pyd",
        # "_bz2.pyd",
        # "_ctypes.pyd",
        # "_decimal.pyd",
        # "_hashlib.pyd",
        # "_lzma.pyd",
        # "_multiprocessing.pyd",
        # "_overlapped.pyd",
        # "_queue.pyd",
        # "_socket.pyd",
        # "_ssl.pyd",
        "_tes3.pyd",
        # "libcrypto-1_1.dll",
        # "libffi-7.dll",
        # "libssl-1_1.dll",
        # "pyexpat.pyd",
        # "pyside6.abi3.dll",
        # "python310.dll",
        # "qtcore.pyd",
        # "qtgui.pyd",
        # "qtnetwork.pyd",
        # "qtsvg.pyd",
        # "qtwidgets.pyd",
        # "select.pyd",
        # "shiboken.pyd",
        # "shiboken6.abi3.dll",
        # "unicodedata.pyd",
    ],
    name="numidium",
)

# -- End PyInstaller --

print("Creating Archive...")

project = tomlkit.load(open("pyproject.toml", "rb"))
version = project.item("tool")["poetry"]["version"]

shutil.make_archive("build/numidium", "zip", "dist")
shutil.move("build/numidium.zip", f"dist/numidium.{version}.zip")

print("Finished!")
