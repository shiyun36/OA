from neo4j import GraphDatabase
import pandas as pd

uri =  "neo4j+s://d224636a.databases.neo4j.io" 
username = "neo4j"
password = "r9kfOnjnCIW8SJ3qTOP-orcp1n15SR6NHW1Uz_JshZY"

# Create the driver instance
driver = GraphDatabase.driver(uri, auth=(username, password))

### Delete everything first, if not it will cause duplicates.
def reset(tx):
    tx.run('''
    MATCH (n)
    DETACH DELETE n
    '''
    )

# Creating graphs
def create_graph(tx):
    tx.run('''
    CREATE (p1:Person {name: "Gerard", role: "Head"})
    CREATE (p2:Person {name: "Rachel", role: "Team Member"})
    CREATE (p3:Person {name: "Lee", role: "Team Member"})
    CREATE (p4:Person {name: "Jocelyn", role: "Head"})
    CREATE (p5:Person {name: "Dorothy", role: "Team Member"})
    CREATE (p6:Person {name: "Albert", role: "Team Member"})

    CREATE (a1:Approver {name: "Ken"})
    CREATE (a2:Approver {name: "Gerard"})
    CREATE (a3:Approver {name: "Keith"})

    CREATE (d1:Department {name: "HR"})
    CREATE (d2:Department {name: "FIN"})
    CREATE (d3:Department {name: "LOB"})

    CREATE (c1:Case {id: 1, description: "Lack of Resource"})
    CREATE (c2:Case {id: 2, description: "Lack of Fund"})
    CREATE (c3:Case {id: 3, description: "Poor Delivery Quality"})
    CREATE (c4:Case {id: 4, description: "Need more room"})
    CREATE (c5:Case {id: 5, description: "Need to create more awareness"})

    CREATE (ac1:Action {name: "Find Resource", status: "Not Started"})
    CREATE (ac2:Action {name: "Sell Project", status: "In Progress"})
    CREATE (ac3:Action {name: "Train Resource", status: "Close"})
    CREATE (ac4:Action {name: "Find Resource", status: "In Progress"})
    CREATE (ac5:Action {name: "Brand Marketing", status: "In Progress"})

    WITH p1, p2, p3, p4, p5, p6, a1, a2, a3, d1, d2, d3, c1, c2, c3, c4, c5, ac1, ac2, ac3, ac4, ac5

    CREATE (p1)-[:belongtoDept]->(d1)
    CREATE (p2)-[:belongtoDept]->(d1)
    CREATE (p3)-[:belongtoDept]->(d1)
    CREATE (p4)-[:belongtoDept]->(d2)
    CREATE (p5)-[:belongtoDept]->(d3)
    CREATE (p6)-[:belongtoDept]->(d3)

    WITH p1, p2, p3, p4, p5, p6, a1, a2, a3, c1, c2, c3, c4, c5, ac1, ac2, ac3, ac4, ac5, d1, d2, d3

    CREATE (p1)-[:seekApproval]->(a1)
    CREATE (p3)-[:seekApproval]->(a2)
    CREATE (p4)-[:seekApproval]->(a1)
    CREATE (p5)-[:seekApproval]->(a3)
    CREATE (p6)-[:seekApproval]->(a3)

    WITH p1, p2, p3, p4, p5, p6, c1, c2, c3, c4, c5, ac1, ac2, ac3, ac4, ac5, d1, d2, d3, a1, a2, a3

    CREATE (p1)-[:hasCase]->(c1)
    CREATE (p4)-[:hasCase]->(c2)
    CREATE (p5)-[:hasCase]->(c3)
    CREATE (p2)-[:hasCase]->(c4)
    CREATE (p1)-[:hasCase]->(c5)

    WITH p1, p2, p3, p4, p5, p6, c1, c2, c3, c4, c5, ac1, ac2, ac3, ac4, ac5, d1, d2, d3, a1, a2, a3

    CREATE (c1)-[:hasAction]->(ac1)
    CREATE (c2)-[:hasAction]->(ac2)
    CREATE (c3)-[:hasAction]->(ac3)
    CREATE (c4)-[:hasAction]->(ac4)
    CREATE (c5)-[:hasAction]->(ac5)

    WITH p1, p2, p3, p4, p5, p6, c1, c2, c3, c4, c5, ac1, ac2, ac3, ac4, ac5, d1, d2, d3, a1, a2, a3


    MATCH (p1:Person {name: "Gerard"}), (d1:Department {name: "HR"})
    CREATE (p1)-[:belongtoDept]->(d1)

    WITH p1, p2, p3, p4, p5, p6, d1, d2, d3, a1, a2, a3, c1, c2, c3, c4, c5, ac1, ac2, ac3, ac4, ac5
    MATCH (p2:Person {name: "Rachel"}), (d1:Department {name: "HR"})
    CREATE (p2)-[:belongtoDept]->(d1)

    WITH p1, p2, p3, p4, p5, p6, d1, d2, d3, a1, a2, a3, c1, c2, c3, c4, c5, ac1, ac2, ac3, ac4, ac5
    MATCH (p3:Person {name: "Lee"}), (d1:Department {name: "HR"})
    CREATE (p3)-[:belongtoDept]->(d1)

    WITH p1, p2, p3, p4, p5, p6, d1, d2, d3, a1, a2, a3, c1, c2, c3, c4, c5, ac1, ac2, ac3, ac4, ac5
    MATCH (p4:Person {name: "Jocelyn"}), (d2:Department {name: "FIN"})
    CREATE (p4)-[:belongtoDept]->(d2)

    WITH p1, p2, p3, p4, p5, p6, d1, d2, d3, a1, a2, a3, c1, c2, c3, c4, c5, ac1, ac2, ac3, ac4, ac5
    MATCH (p5:Person {name: "Dorothy"}), (d3:Department {name: "LOB"})
    CREATE (p5)-[:belongtoDept]->(d3)

    WITH p1, p2, p3, p4, p5, p6, d1, d2, d3, a1, a2, a3, c1, c2, c3, c4, c5, ac1, ac2, ac3, ac4, ac5
    MATCH (p6:Person {name: "Albert"}), (d3:Department {name: "LOB"})
    CREATE (p6)-[:belongtoDept]->(d3)

    WITH p1, p2, p3, p4, p5, p6, d1, d2, d3, a1, a2, a3, c1, c2, c3, c4, c5, ac1, ac2, ac3, ac4, ac5

    // Relationships between Person and Approver
    MATCH (p1:Person {name: "Gerard"}), (a1:Approver {name: "Ken"})
    CREATE (p1)-[:seekApproval]->(a1)

    WITH p1, p2, p3, p4, p5, p6, d1, d2, d3, a1, a2, a3, c1, c2, c3, c4, c5, ac1, ac2, ac3, ac4, ac5
    MATCH (p3:Person {name: "Lee"}), (a2:Approver {name: "Gerard"})
    CREATE (p3)-[:seekApproval]->(a2)

    WITH p1, p2, p3, p4, p5, p6, d1, d2, d3, a1, a2, a3, c1, c2, c3, c4, c5, ac1, ac2, ac3, ac4, ac5
    MATCH (p4:Person {name: "Jocelyn"}), (a1:Approver {name: "Ken"})
    CREATE (p4)-[:seekApproval]->(a1)

    WITH p1, p2, p3, p4, p5, p6, d1, d2, d3, a1, a2, a3, c1, c2, c3, c4, c5, ac1, ac2, ac3, ac4, ac5
    MATCH (p5:Person {name: "Dorothy"}), (a3:Approver {name: "Keith"})
    CREATE (p5)-[:seekApproval]->(a3)

    WITH p1, p2, p3, p4, p5, p6, d1, d2, d3, a1, a2, a3, c1, c2, c3, c4, c5, ac1, ac2, ac3, ac4, ac5
    MATCH (p6:Person {name: "Albert"}), (a3:Approver {name: "Keith"})
    CREATE (p6)-[:seekApproval]->(a3)

    WITH p1, p2, p3, p4, p5, p6, d1, d2, d3, a1, a2, a3, c1, c2, c3, c4, c5, ac1, ac2, ac3, ac4, ac5

    MATCH (p1:Person {name: "Gerard"}), (c1:Case {id: 1})
    CREATE (p1)-[:hasCase]->(c1)

    WITH p1, p2, p3, p4, p5, p6, d1, d2, d3, a1, a2, a3, c1, c2, c3, c4, c5, ac1, ac2, ac3, ac4, ac5
    MATCH (p4:Person {name: "Jocelyn"}), (c2:Case {id: 2})
    CREATE (p4)-[:hasCase]->(c2)

    WITH p1, p2, p3, p4, p5, p6, d1, d2, d3, a1, a2, a3, c1, c2, c3, c4, c5, ac1, ac2, ac3, ac4, ac5
    MATCH (p5:Person {name: "Dorothy"}), (c3:Case {id: 3})
    CREATE (p5)-[:hasCase]->(c3)

    WITH p1, p2, p3, p4, p5, p6, d1, d2, d3, a1, a2, a3, c1, c2, c3, c4, c5, ac1, ac2, ac3, ac4, ac5
    MATCH (p2:Person {name: "Rachel"}), (c4:Case {id: 4})
    CREATE (p2)-[:hasCase]->(c4)

    WITH p1, p2, p3, p4, p5, p6, d1, d2, d3, a1, a2, a3, c1, c2, c3, c4, c5, ac1, ac2, ac3, ac4, ac5
    MATCH (p1:Person {name: "Gerard"}), (c5:Case {id: 5})
    CREATE (p1)-[:hasCase]->(c5)

    WITH p1, p2, p3, p4, p5, p6, d1, d2, d3, a1, a2, a3, c1, c2, c3, c4, c5, ac1, ac2, ac3, ac4, ac5

    // Relationships between Case and Action
    MATCH (c1:Case {id: 1}), (ac1:Action {name: "Find Resource"})
    CREATE (c1)-[:hasAction]->(ac1)

    WITH p1, p2, p3, p4, p5, p6, d1, d2, d3, a1, a2, a3, c1, c2, c3, c4, c5, ac1, ac2, ac3, ac4, ac5
    MATCH (c2:Case {id: 2}), (ac2:Action {name: "Sell Project"})
    CREATE (c2)-[:hasAction]->(ac2)

    WITH p1, p2, p3, p4, p5, p6, d1, d2, d3, a1, a2, a3, c1, c2, c3, c4, c5, ac1, ac2, ac3, ac4, ac5
    MATCH (c3:Case {id: 3}), (ac3:Action {name: "Train Resource"})
    CREATE (c3)-[:hasAction]->(ac3)

    WITH p1, p2, p3, p4, p5, p6, d1, d2, d3, a1, a2, a3, c1, c2, c3, c4, c5, ac1, ac2, ac3, ac4, ac5
    MATCH (c4:Case {id: 4}), (ac4:Action {name: "Find Resource"})
    CREATE (c4)-[:hasAction]->(ac4)

    WITH p1, p2, p3, p4, p5, p6, d1, d2, d3, a1, a2, a3, c1, c2, c3, c4, c5, ac1, ac2, ac3, ac4, ac5
    MATCH (c5:Case {id: 5}), (ac5:Action {name: "Brand Marketing"})
    CREATE (c5)-[:hasAction]->(ac5)

    RETURN *
    ''')

def create_named_graph(tx):
    tx.run('''
    CALL gds.graph.project(
        'myGraph',
        ['Person', 'Approver', 'Department', 'Case', 'Action'],
        {
            belongtoDept: {
                type: 'belongtoDept',
                orientation: 'UNDIRECTED'
            },
            seekApproval: {
                type: 'seekApproval',
                orientation: 'UNDIRECTED'
            },
            hasCase: {
                type: 'hasCase',
                orientation: 'UNDIRECTED'
            },
            hasAction: {
                type: 'hasAction',
                orientation: 'UNDIRECTED'
            }
        }
    )
    ''')


#Q1a
def get_lob_count(tx):
    tx.run('''
    MATCH (p:Person)-[:belongtoDept]->(d:Department {name: "LOB"})
    RETURN count(DISTINCT p) as NumberOfPeopleInLOB;
    ''')

#Q1b
def get_hr_cases(tx):
    tx.run('''
    MATCH (d:Department {name: "HR"})<-[:belongtoDept]-(p:Person)-[:hasCase]->(c:Case)
    WITH DISTINCT d, p, c
    RETURN count(*) AS HRCaseLoad
    ''')


#2
## CHECK: Since Rachel is a team member in the HR department and Gerard is the Head of the HR department,
## and Lee, who is a team member of the HR Department has Gerard as his/her Approver, it is logical 
## to conclude that Gerard is Rachel's approver as well.
### NOTE: Once the code has been executed once, it will return nothing because the r/s is already established, and will no longer return NULL.
def run_link_prediction(tx):
    tx.run("""
    CALL gds.graph.project(
        'myGraph',
        ['Person', 'Approver'],
        {
            seekApproval: {
                type: 'seekApproval',
                orientation: 'UNDIRECTED'
            }
        }
    )
    """)
    result = tx.run('''
    CALL gds.beta.linkprediction.adamicAdar.stream({
        nodeProjection: ['Person', 'Approver'],
        relationshipProjection: {
            SEEK_APPROVAL: {
                type: 'seekApproval',
                orientation: 'UNDIRECTED'
            }
        },
        topK: 1
    })
    YIELD node1, node2, score
    RETURN gds.util.asNode(node1).name AS Person, gds.util.asNode(node2).name AS Approver, score
    ORDER BY score DESC
    ''')
    return [{"Person": record["Person"], "Approver": record["Approver"], "Score": record["score"]} for record in result]


with driver.session() as session:
    session.execute_write(reset)
    session.execute_write(create_graph)
    session.execute_write(create_named_graph)
    lob_count = session.execute_read(get_lob_count)
    print(f"Number of people in LOB department: {lob_count}")
    hr_case_count = session.execute_read(get_hr_cases)
    print(f"Number of cases in HR department: {hr_case_count}")
    predictions = session.execute_write(run_link_prediction)
    rachel_approver = [pred for pred in predictions if pred["Person"] == "Rachel"]
    print(f"Rachel's approver is : {rachel_approver}")
    