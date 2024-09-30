import click
from app import create_app
from extensions.db import db
from app.models import User, Role, Permission, Department, user_role, user_department, role_permission

app = create_app()


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


@app.cli.command("run-server")
def run_server():
    """运行服务器"""
    app.run()


if __name__ == '__main__':
    run_server()