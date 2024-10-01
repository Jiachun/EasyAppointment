import click
from flask_migrate import Migrate
from app import create_app
from extensions.db import db
from app.models import User, Role, Permission, Department, user_role, user_department, role_permission, campus, visitor, visitor_log


app = create_app()

# 初始化 Flask-Migrate
migrate = Migrate(app, db)


@app.cli.command("create-db")
def create_db():
    """创建数据库表"""
    with app.app_context():
        db.create_all()
        click.echo("数据库表已创建！")


@app.cli.command("drop-db")
def drop_db():
    """删除数据库表"""
    with app.app_context():
        db.drop_all()
        click.echo("数据库表已删除！")


@app.cli.command("init-migrate")
def init_migrate():
    """初始化数据库迁移"""
    with app.app_context():
        # 创建迁移文件夹
        from flask_migrate import init
        init()
        click.echo("数据库迁移已初始化！")


@app.cli.command("migrate-db")
def migrate_db():
    """生成迁移脚本"""
    with app.app_context():
        from flask_migrate import migrate
        migrate()
        click.echo("迁移脚本已生成！")


@app.cli.command("upgrade-db")
def upgrade_db():
    """应用迁移"""
    with app.app_context():
        from flask_migrate import upgrade
        upgrade()
        click.echo("数据库已升级！")


@app.cli.command("downgrade-db")
@click.argument('revision')
def downgrade_db(revision):
    """回滚迁移"""
    with app.app_context():
        from flask_migrate import downgrade
        downgrade(revision)
        click.echo(f"数据库已降级到版本 {revision}！")


@app.cli.command("run-server")
def run_server():
    """运行服务器"""
    app.run()


if __name__ == '__main__':
    run_server()