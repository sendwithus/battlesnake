import uuid
from lib.models.team import Team
from pymongo.errors import DuplicateKeyError


""" For performance testing I needed teams to add to games.

    This creates teams.
    * It uses a list of names from a file as a source of team names and email addresses.
    * The snake_url is the URL to a cloned python-client running on a unique port.  I generate the ports.

    The result of a run is:
    * N new teams
    * a file containing the port of the snake_url and the uuid IDs of the corresponding team
      to be used by a provided script to launch them.
      eg.  8090,c2526fb3-ff19-46ab-95c3-b7700a75329c

"""
SNAKE_URL_HOST = "http://192.168.1.25" # NOTE: This will need to be your IP
PASSWORD_HASH = "pbkdf2:sha1:1000-bashf5f01f19c4715a655cd28d4b53fcca5c20f440a"
GAME_MODE = 'advanced'

names_file = open('lib/tools/names.txt', 'r')

ids = []
ports = []
names = []
TEAM_SIZE = 12
team_counter = 1
team_id_counter = 0

# zip/iterate over port and names to construct teams
for port, name in zip(["%.3d" % port for port in range(90, (90 + 304))], [name.strip() for name in names_file]):

    team_counter += 1
    _id = str(uuid.uuid4())
    member_email = "%s@email.com" % name
    team_name = name
    snake_url = "%s:8%s" % (SNAKE_URL_HOST, port)

    # save names for manual add of teams to games
    names += [name]

    team = Team(
        teamname=team_name,
        password=PASSWORD_HASH,
        member_emails=[member_email],
        game_mode=GAME_MODE,
        snake_url=snake_url,
        is_public=True
    )

    try:
        team.insert()
    except DuplicateKeyError:
        print "Team %s already exists!!" % team_name

    # save _id and port for appending to port/id file
    ids += [team.id]
    ports += ["8%s" % port]

    # write TEAM_SIZE team_names to a file
    # NOTE: may be unnecessary
    if team_counter > TEAM_SIZE:
        team_id_counter += 1
        # write TEAM_SIZE team_names to a file
        team_name_outfile = open('lib/tools/teams/team%.3d.txt' % team_id_counter, 'w')
        for name in names:
            team_name_outfile.write("%s\n" % name)
        team_name_outfile.close()
        names = []

        # write TEAM_SIZE port,id to file
        port_team_outfile = open('lib/tools/teams/port_team%.3d.txt' % team_id_counter, 'w')
        for port, id in zip([port for port in ports], [id for id in ids]):
            port_team_outfile.write("%s,%s\n" % (port, id))
        port_team_outfile.close()

        team_counter = 1

if team_counter <= TEAM_SIZE:
    team_id_counter += 1
    # write TEAM_SIZE team_names to a file
    team_name_outfile = open('lib/tools/teams/team%.3d.txt' % team_id_counter, 'w')
    for name in names:
        team_name_outfile.write("%s\n" % name)
    team_name_outfile.close()
    names = []

    # write TEAM_SIZE port,id to file
    port_team_outfile = open('lib/tools/teams/port_team%.3d.txt' % team_id_counter, 'w')
    for port, id in zip([port for port in ports], [id for id in ids]):
        port_team_outfile.write("%s,%s\n" % (port, id))
    port_team_outfile.close()
