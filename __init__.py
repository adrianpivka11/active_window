import sys

if sys.platform in ['linux', 'linux2']:
    from time_tracking.active_window.linux import get_active_window_title
elif sys.platform in ['Windows', 'win32', 'cygwin']:
    from time_tracking.active_window.windows import get_active_window_title
elif sys.platform in ['Mac', 'darwin', 'os2', 'os2emx']:
    from time_tracking.active_window.macos import get_active_window_title
else:
    raise ImportError(f"Environment [{sys.platform}] not supported!")
