# Election results

## REST API query design

First, send a request to
`http://lda.data.parliament.uk/electionresults.json` which is the top
level endpoint.


```
# Root request, returns election result meta-objects
elections = FETCH http://lda.data.parliament.uk/electionresults.json |> result |>
totalResults

for election in elections:
    # Extract constituency info
    {
        constituency_url = election |> constituency |> _about
        constituency_info = FETCH constituency_url

        constituency_type = constituency_info |> result |> primaryTopic |> constituencyType
        constituency_name = constituency_info |> result |> primaryTopic |> label |> _value
        constituency_os_name = constituency_info |> result |> primaryTopic |> osName
    }

    # Extract election info
    {
        election_url = election |> _about
        election_info = FETCH election_url

        election_type = election_info |> result |> primaryTopic |> electionType
        election_label = election_info |> result |> primaryTopic |> label |> _value
        candidates = election_info |> result |> primaryTopic |> candidate
        turnout = election_info |> result |> primaryTopic |> turnout

        for candidate_url in candidates:
            candidate = FETCH candidate_url
            vote_change_percentage = candidate |> result |> primaryTopic |> voteChangePercentage
            votes = candidate |> result |> primaryTopic |> numberOfVotes
            full_name = candidate |> result |> primaryTopic |> fullName |> _value
            party = candidate |> result |> primaryTopic |> party |> _value
    }
```

## Models

```
candidate:
    id integer primary key
    full_name string

constituency:
    id integer primary key
    type string
    name string
    os_name string

election:
    id integer primary key
    type string
    label string

turnout:
    id integer primary key
    election_id integer foreign_key(election.id)
    constituency_id integer foreign_key(constituency.id)
    turnout integer
    
votes:
    id integer primary key
    candidate_id integer foreign_key(candidate.id)
    constituency_id integer foreign_key(constituency.id)
    election_id integer foreign_key(election.id)
    votes integer
    vote_change_percentage real
    party string
```

vim: tw=0:nowrap
