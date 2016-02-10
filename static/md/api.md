# BattleSnake API Documentation

## Teams API

### GET /api/teams/

List all public teams, as well as the currently signed in team (whether public or not)

##### Parameters
None

##### Response
* **data** - A list of team objects
  * **teamname** - Snake name
  * **member_emails** - List of emails for members of this team
  * **snake_url** - Full URL to the team's current snake AI, or null if not set

```json
{
  "data": [
    {
      "teamname": "TEAM1",
      "member_emails": ["user@domain.com"],
      "snake_url": "http://localhost:6000/"
    }
  ]
}
```

### GET /api/teams/current

Get the currently signed-in team.

##### Parameters
None

##### Response
* **data** - A team object for the team that's currently signed in
  * **teamname** - Snake name
  * **member_emails** - List of emails for members of this team
  * **snake_url** - Full URL to the team's current snake AI, or null if not set

```json
{
  "data": [
    {
      "teamname": "TEAM1",
      "member_emails": ["user@domain.com"],
      "snake_url": "http://localhost:6000/"
    }
  ]
}
```
