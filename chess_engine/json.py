#Sending format
model = {
     choices: [
        {
            name: "Pd2",
            id: "d2",
            choices: [
                {
                    name: "d3", 
                    id: "d3",
                    choices: []
                },
                {
                    name: "d4", 
                    id: "d4",
                    choices: []
                }
            ]
        },
        {
            name: "Kb2",
            id: "b2",
            choices: [
                {
                    name: "a3", 
                    id: "a3",
                    choices: []
                },
                {
                    name: "c3", 
                    id: "c3",
                    choices: []
                }
            ]
        }
    ],
    display: "board string"
}


# return format
[id1, id2]