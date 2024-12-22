import logging


logger = logging.getLogger("UserController")
class UserController(BaseController):

  @staticmethod
  def createUser(user: UserCreate, db: Session):