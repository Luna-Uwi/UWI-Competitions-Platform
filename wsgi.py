import click, pytest, sys
from flask import Flask
from datetime import datetime, date

from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.main import create_app
from App.controllers import *


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def initialize():
    db.drop_all()
    db.create_all()

    stud1 = create_student('stud1', 'stud1pass')
    stud2 = create_student('stud2', 'stud2pass')
    stud3 = create_student('stud3', 'stud3pass')
    stud4 = create_student('stud4', 'stud4pass')
    stud5 = create_student('stud5', 'stud5pass')
    stud6 = create_student('stud6', 'stud6pass')
    #ranking = create_ranking(bob.id)
    mod1 = create_moderator('mod1', 'mod1pass')
    mod2 = create_moderator('mod2', 'mod2pass')
    mod3 = create_moderator('mod3', 'mod3pass')
    #bill = create_admin('bill', 'billpass', 1)
    Runtime = create_competition('Runtime', '09-02-2024', 'CSL', 'mod1')

    #participant = register_student('bob', 'RunTime')
    #host = join_comp('rob', 'RunTime')

    print('database intialized')

'''
Student Commands
'''

student_cli = AppGroup("student", help="Student commands") 

@student_cli.command("create", help="Creates a student")
@click.argument("username", default="stud1")
@click.argument("password", default="stud1pass")
def create_student_command(username, password):
    student = create_student(username, password)

@student_cli.command("update", help="Updates a student's username")
@click.argument("id", default="1")
@click.argument("username", default="stud1")
def update_student_command(id, username):
    student = update_student(id, username)

@student_cli.command("list", help="Lists students in the database")
@click.argument("format", default="string")
def list_students_command(format):
    if format == 'string':
        print(get_all_students())
    else:
        print(get_all_students_json())
"""
@student_cli.command("register", help="Registers student for a competition")
@click.argument("username", default="stud1")
@click.argument("comp_name", default="Runtime")
def register_student_command(username, comp_name):
    register_student(username, comp_name)
"""
@student_cli.command("display", help="Displays student profile")
@click.argument("username", default="stud1")
def display_student_info_command(username):
    print(display_student_info(username))

@student_cli.command("notifications", help="Gets all notifications")
@click.argument("username", default="stud1")
def display_notifications_command(username):
    print(display_notifications(username))

app.cli.add_command(student_cli)


'''
Moderator Commands
'''

mod_cli = AppGroup("mod", help="Moderator commands") 

@mod_cli.command("create", help="Creates a moderator")
@click.argument("username", default="mod1")
@click.argument("password", default="mod1pass")
def create_moderator_command(username, password):
    mod = create_moderator(username, password)

@mod_cli.command("addMod", help="Adds a moderator to a competition")
@click.argument("mod1_name", default="mod1")
@click.argument("comp_name", default="Runtime")
@click.argument("mod2_name", default="mod2")
def add_mod_to_comp_command(mod1_name, comp_name, mod2_name):
    mod = add_mod(mod1_name, comp_name, mod2_name)

@mod_cli.command("addTeam", help="Adds a team to a competition")
@click.argument("mod_name", default="mod1")
@click.argument("comp_name", default="Runtime")
@click.argument("team_name", default="Coders")
@click.argument("student1", default="stud1")
@click.argument("student2", default="stud2")
@click.argument("student3", default="stud3")
def add_mod_to_comp_command(mod_name, comp_name, team_name, student1, student2, student3):
    students = [student1, student2, student3]
    team = find_team(team_name, students)
    comp = add_team(mod_name, comp_name, team)

@mod_cli.command("addResults", help="Adds results for a team in a competition")
@click.argument("mod_name", default="mod1")
@click.argument("comp_name", default="Runtime")
@click.argument("team_name", default="Coders")
@click.argument("score", default="10")
def add_results_command(mod_name, comp_name, team_name, score):
    comp_team = add_results(mod_name, comp_name, team_name, score)
    #update_rankings()

app.cli.add_command(mod_cli)


'''
Competition commands
'''

comp_cli = AppGroup("comp", help = "Competition commands")   

@comp_cli.command("create", help = "Creates a competition")
@click.argument("name", default = "Runtime")
@click.argument("date", default = date.today())
@click.argument("location", default = "CSL")
@click.argument("mod_name", default = "mod1")
def create_competition_command(name, date, location, mod_name):
    comp = create_competition(name, date, location, mod_name)

@comp_cli.command("details", help = "Displays competition details")
@click.argument("name", default = "Runtime")
def display_competition_details_command(name):
    comp = get_competition_by_name(name)
    print(comp.get_json())

@comp_cli.command("list", help = "list all competitions")
def list_competition_command():
    print(get_all_competitions_json())

@comp_cli.command("results", help = "displays competition results")
@click.argument("name", default = "Runtime")
def display_competition_results_command(name):
    print(display_competition_results(name))

app.cli.add_command(comp_cli)

"""
'''
Ranking commands
'''
ranking_cli = AppGroup('ranking', help = "Ranking commands")

@ranking_cli.command("display", help="Displays ranking")
def display_rankings__command():
    print(display_rankings())

app.cli.add_command(ranking_cli)
"""

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("app", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "IntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))

app.cli.add_command(test)

