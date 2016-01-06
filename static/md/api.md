# BattleSnake API Documentation

## Teams API

### GET /api/teams/

List all teams.

##### Parameters
None

##### Response
* **data** - A list of team objects
  * **teamname** - Team name
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
  * **teamname** - Team name
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


### PUT /api/teams/current

Update the team that's currently signed in.

##### Parameters
* **snake_url** - Full URL to the team's current snake AI, or null if not set
* **teamname** - Team name - *Not currently updateable*
* **password** - The team's new password - *Not currently updateable*

```json
{
  "teamname": "TEAM2",
  "snake_url": "http://localhost:7000/",
  "password": "SECRET"
}
```

##### Response
* **data** - The updated team object
  * **teamname** - Team name
  * **member_emails** - List of emails for members of this team
  * **snake_url** - Full URL to the team's current snake AI, or null if not set

```json
{
  "data": [
    {
      "teamname": "TEAM2",
      "member_emails": ["user@domain.com"],
      "snake_url": "http://localhost:7000/"
    }
  ]
}
```

### PUT /api/teams/current/members/&lt;email&gt;

Add a member to the team that's currently signed in.

##### URL Parameters
* **email** - The email of the user to add

##### Response
* **data** - The updated list of member emails on the current team

```json
{
  "data": ["user@email.com", "user2@email.com"]
}
```

### POST /api/teams/

Create a new team.

##### Parameters
* **snake_url** - Full URL to the team's current snake AI, or null if not set
* **teamname** - Team name - *Not currently updateable*
* **password** - The team's new password - *Not currently updateable*

```json
{
  "teamname": "TEAM2",
  "password": "SECRET",
  "snake_url": "http://localhost:8000/"
}
```

##### Response
* **data** - The new team object
  * **teamname** - Team name
  * **member_emails** - List of emails for members of this team
  * **snake_url** - Full URL to the team's current snake AI, or null if not set

```json
{
  "data": [
    {
      "teamname": "TEAM2",
      "member_emails": [],
      "snake_url": "http://localhost:7000/"
    }
  ]
}
```
