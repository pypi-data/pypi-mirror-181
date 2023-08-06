

""""""# start delvewheel patch
def _delvewheel_init_patch_1_1_4():
    import os
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'nyxus.libs'))
    is_pyinstaller = getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')
    if not is_pyinstaller or os.path.isdir(libs_dir):
        os.add_dll_directory(libs_dir)


_delvewheel_init_patch_1_1_4()
del _delvewheel_init_patch_1_1_4
# end delvewheel patch

from .nyxus import Nyxus
from .nyxus import Nested
from .functions import gpu_is_available, get_gpu_properties

from . import _version
__version__ = _version.get_versions()['version']
