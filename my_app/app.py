import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import logging
from my_app import create_app

app = create_app()

if __name__ == "__main__":
    host_address = app.config.get("SERVER_HOST", "0.0.0.0")
    port_number = app.config.get("SERVER_PORT", 5000)
    debug_mode = app.config.get("DEBUG", False)

    logging.getLogger("my_app.server").info(
        f"Starting application server on {host_address}:{port_number} (debug={debug_mode})"
    )

    app.run(
        host=host_address,
        port=port_number,
        debug=debug_mode,
    )
