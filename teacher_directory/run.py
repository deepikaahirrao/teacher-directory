from teacher_directory.app import create_app


def main():
    """
    initialize app object to run flask application
    :return: None
    """
    app = create_app("config.yaml")
    app.run(debug=True,
            host=app.config['service_config'].host,
            port=app.config['service_config'].port)


if __name__ == "__main__":
    main()

