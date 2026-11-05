from my_app import create_app

app = create_app()

if __name__ == "__main__":
    host_address = app.config.get("SERVER_HOST", "0.0.0.0")
    port_number = app.config.get("SERVER_PORT", 5000)
    debug_mode = app.config.get("DEBUG", False)

    app.run(
        host=host_address,
        port=port_number,
        debug=debug_mode,
    )
