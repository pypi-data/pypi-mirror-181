config = Config(".env")
models_pymodule_path = config("models_pymodule", default="models")
user_model_name = config("user_model", default = "User")


### Advanced config options
sqlalchemy_base_name = config("sqlalchemy_base_name", default = "Base")
