from flask import (
    request, g, session,
    render_template, redirect, flash,
    abort, url_for
)

from lib.server import form_error, json_response, app
from lib.models.team import Team
from lib.forms import TeamUpdateForm


@app.route('/api/team', methods=['GET'])
def get_api_team(team_id=None):
    """
    Get the current team instance
    """
    return json_response({
        'team': g.team.serialize(),
        'is_admin': (g.team.type == Team.TYPE_ADMIN)
    })

@app.route('/team', methods=['GET'])
@app.route('/admin/teams/<team_id>', methods=['GET'])
def get_team(team_id=None):
    """
    Show team profile page

    Can be used by admins to view any team by adding ?admin_override_id=<team_id> to URL
    """
    is_admin = (g.team.type == Team.TYPE_ADMIN)
    team = g.team

    # Admin override
    if team_id:
        team = Team.find_one({'_id': team_id})
        if not is_admin or not team:
            abort(404)

    form = TeamUpdateForm(obj=team)

    return render_template('team.html', team=team, is_admin=is_admin, form=form)


@app.route('/team', methods=['POST'])
@app.route('/admin/teams/<team_id>', methods=['POST'])
def update_team(team_id=None):
    """
    Update team profile
    """
    is_admin = (g.team.type == Team.TYPE_ADMIN)
    team = g.team

    # Admin override
    if team_id:
        team = Team.find_one({'_id': team_id})
        if not is_admin or not team:
            abort(404)

    form = TeamUpdateForm(obj=team)
    if not form.validate_on_submit():
        app.logger.error('form errors: %s', form.errors)

        # render errors in form
        return render_template('team.html', team=team, is_admin=is_admin, form=form)

    # Validate teamname
    teamname = form.teamname.data
    other_team = Team.find_one({'$and': [
        {'teamname': teamname},
        {'_id': {'$ne': team.id}},
    ]})
    if other_team:
        return form_error('Snake name already in use')
    team.teamname = teamname

    # Set snake_url if provided
    if form.snake_url.data:
        team.snake_url = form.snake_url.data

    # Set is_public
    team.is_public = form.is_public.data

    # Add member_email if provided
    email = form.add_member.data
    if email and email not in team.member_emails:
        team.member_emails.append(email)

    # Set password if provided
    if form.password.data:
        team.set_password(form.password.data)

    # Set game_mode
    team.game_mode = form.game_mode.data

    # Set team type
    team.type = form.type.data

    team.save()

    flash('Team updated')
    return redirect(request.url)

@app.route('/team/remove', methods=['POST'])
@app.route('/admin/teams/<team_id>/remove', methods=['POST'])
def remove_team_member(team_id=None):
    """
    Remove a team member
    """
    is_admin = (g.team.type == Team.TYPE_ADMIN)
    team = g.team
    redirect_url = '/team'

    # Admin override
    if team_id:
        team = Team.find_one({'_id': team_id})
        if not is_admin or not team:
            abort(404)
        redirect_url = '/admin/teams/%s' %  team_id

    email = request.args.get('email')
    if not (email and email in team.member_emails):
        return form_error('Email was not a member of a team')

    if len(team.member_emails) == 1:
        return form_error('Cannot remove last member of a team')

    team.member_emails.remove(email)
    team.save()

    flash('Team member removed')
    return redirect(redirect_url)

@app.route('/team/delete', methods=['POST'])
@app.route('/admin/teams/<team_id>/delete', methods=['POST'])
def delete_team(team_id=None):
    """
    Delete team profile
    """
    is_admin = (g.team.type == Team.TYPE_ADMIN)
    team = g.team

    # Admin override
    if team_id:
        team = Team.find_one({'_id': team_id})
        if not is_admin or not team:
            abort(404)

    team.remove()

    if team_id:
        flash('Team deleted')
        return redirect(url_for('list_teams'))

    return redirect(url_for('logout'))

@app.route('/api/teams/')
def teams_list():
    """
    List all public teams as well as the current team (whether it's public or not).
    Sample response:
    {
      "data": [
        {
          "teamname": "TEAM1",
          "member_emails": ["user@domain.com"],
          "snake_url": "http://localhost:6000/"
        }
      ]
    }
    """
    teams = Team.find(
        {'$and': [
            {'$or': [
                {'is_public': True},
                {'_id': g.team.id}
            ]},
            {'type': {'$ne': Team.TYPE_ADMIN}},
        ]}, limit=50)
    return json_response([team.serialize() for team in teams])


@app.route('/api/teams/current')
def team_info():
    """
    Get information about the current signed in team.

    Sample response:
    {
      "teamname": "TEAM1",
      "member_emails": ["user@domain.com"],
      "snake_url": "http://localhost:6000/"
    }
    """
    app.logger.info(session)
    return json_response(data=g.team.serialize())
