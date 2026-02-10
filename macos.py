"""Active window's helper for MacOs."""
import pygetwindow as gw


def get_active_window_title() -> str:
    """Return the tittle of the active window."""
    # Based on: https://stackoverflow.com/questions/7142342/get-window-position-size-with-python/77406474#77406474
    try:
        activeAppName = gw.getActiveWindow()
        return activeAppName
    except Exception:
        return "Error read activity"

if __name__ == "__main__":
    print(get_active_window_title())
