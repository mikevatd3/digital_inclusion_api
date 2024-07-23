from sqlalchemy import create_engine

import tomli 


with open("config.toml", "rb") as f:
    config = tomli.load(f)


di_engine = create_engine(
    f"postgresql+psycopg2://{config['db']['username']}@"
    f"{config['db']['hostname']}:{config['db']['port']}/{config['db']['database']}"
)
