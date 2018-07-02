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
    constituency = election |> constituency |> label |> _value
    label = election |> label |> _value

    about_link = election |> _about
    details = FETCH about_link
    candidates = details |> result |> primaryTopic |> candidate
    turnout = details |> result |> primaryTopic |> 
turnout

    for candidate_url in candidates:
        candidate = FETCH candidate_url
        vote_change_percentage = candidate |> result |> primaryTopic |> voteChangePercentage
        votes = candidate |> result |> primaryTopic |>
numberOfVotes
        full_name = candidate |> result |> primaryTopic |> fullName |>
_value
        party = candidate |> result |> primaryTopic |> party |> _value
```
