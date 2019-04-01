import os
import logging
import pymysql
import logging.config
from flask import Flask
import conf.config as CONFIG
from flask_sqlalchemy import SQLAlchemy

pymysql.install_as_MySQLdb()
app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI']="mysql://root:654321@localhost:3306/blog"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config["SECRET_KEY"] = "renyizifuchuan"
app.debug = True
app.use_reloader = False

def main():
    # 注册蓝图
    from src.views.user import user
    from src.views.blog import blog
    app.register_blueprint(user)
    app.register_blueprint(blog)

    logging.config.fileConfig(CONFIG.LOGGING)
    logging.info('start server. host:[%s], port:[%s]' % (CONFIG.HOST, CONFIG.PORT))
    with open('./.pid', 'w') as f:
        f.write(str(os.getpid()))
    app.run(host=CONFIG.HOST, port=CONFIG.PORT)

if __name__ == '__main__':
    main()
