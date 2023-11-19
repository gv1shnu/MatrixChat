
# Internal imports
from app import create_app
from utl.logger import Logger

logger = Logger()


if __name__ == '__main__':
    app = create_app()
    app.run()
