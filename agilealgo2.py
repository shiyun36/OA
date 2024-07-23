from neo4j import GraphDatabase
import pandas as pd

uri =  "neo4j+s://d224636a.databases.neo4j.io" #
username = "neo4j"
password = "r9kfOnjnCIW8SJ3qTOP-orcp1n15SR6NHW1Uz_JshZY"

# Create the driver instance
driver = GraphDatabase.driver(uri, auth=(username, password))

'''
CREATE (P:Person {name: "PersonName"}) #
CREATE (Ap:Approver {name: "ApproverName"})
CREATE (D:Department {name: "DepartmentName"})
CREATE (C:Case {name: "CaseName"})
CREATE (A:Action {name: "ActionName"})

CREATE (P)-[:seekApproval]->(Ap)
CREATE (P)-[:belongtoDept]->(D)
CREATE (P)-[:hasCase]->(C)
CREATE (C)-[:hasAction]->(A)

RETURN P, Ap, D, C, A

'''


'''
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

MATCH (p1:Person {name: "Gerard"}), (d1:Department {name: "HR"})
CREATE (p1)-[:belongtoDept]->(d1)
WITH p1, d1

MATCH (p2:Person {name: "Rachel"}), (d1:Department {name: "HR"})
CREATE (p2)-[:belongtoDept]->(d1)
WITH p2, d1

MATCH (p3:Person {name: "Lee"}), (d1:Department {name: "HR"})
CREATE (p3)-[:belongtoDept]->(d1)
WITH p3, d1

MATCH (p4:Person {name: "Jocelyn"}), (d2:Department {name: "FIN"})
CREATE (p4)-[:belongtoDept]->(d2)
WITH p4, d2

MATCH (p5:Person {name: "Dorothy"}), (d3:Department {name: "LOB"})
CREATE (p5)-[:belongtoDept]->(d3)
WITH p5, d3

MATCH (p6:Person {name: "Albert"}), (d3:Department {name: "LOB"})
CREATE (p6)-[:belongtoDept]->(d3)
WITH p6, d3

MATCH (p1:Person {name: "Gerard"}), (a1:Approver {name: "Ken"})
CREATE (p1)-[:seekApproval]->(a1)
WITH p1, a1

MATCH (p3:Person {name: "Lee"}), (a2:Approver {name: "Gerard"})
CREATE (p3)-[:seekApproval]->(a2)
WITH p3, a2

MATCH (p4:Person {name: "Jocelyn"}), (a1:Approver {name: "Ken"})
CREATE (p4)-[:seekApproval]->(a1)
WITH p4, a1

MATCH (p5:Person {name: "Dorothy"}), (a3:Approver {name: "Keith"})
CREATE (p5)-[:seekApproval]->(a3)
WITH p5, a3

MATCH (p6:Person {name: "Albert"}), (a3:Approver {name: "Keith"})
CREATE (p6)-[:seekApproval]->(a3)
WITH p6, a3

MATCH (p1:Person {name: "Gerard"}), (c1:Case {id: 1})
CREATE (p1)-[:hasCase]->(c1)
WITH p1, c1

MATCH (p4:Person {name: "Jocelyn"}), (c2:Case {id: 2})
CREATE (p4)-[:hasCase]->(c2)
WITH p4, c2

MATCH (p5:Person {name: "Dorothy"}), (c3:Case {id: 3})
CREATE (p5)-[:hasCase]->(c3)
WITH p5, c3

MATCH (p2:Person {name: "Rachel"}), (c4:Case {id: 4})
CREATE (p2)-[:hasCase]->(c4)
WITH p2, c4

MATCH (p1:Person {name: "Gerard"}), (c5:Case {id: 5})
CREATE (p1)-[:hasCase]->(c5)
WITH p1, c5

MATCH (c1:Case {id: 1}), (ac1:Action {name: "Find Resource"})
CREATE (c1)-[:hasAction]->(ac1)
WITH c1, ac1

MATCH (c2:Case {id: 2}), (ac2:Action {name: "Sell Project"})
CREATE (c2)-[:hasAction]->(ac2)
WITH c2, ac2

MATCH (c3:Case {id: 3}), (ac3:Action {name: "Train Resource"})
CREATE (c3)-[:hasAction]->(ac3)
WITH c3, ac3

MATCH (c4:Case {id: 4}), (ac4:Action {name: "Find Resource"})
CREATE (c4)-[:hasAction]->(ac4)
WITH c4, ac4

MATCH (c5:Case {id: 5}), (ac5:Action {name: "Brand Marketing"})
CREATE (c5)-[:hasAction]->(ac5)
WITH c5, ac5

MATCH (p:Person)-[:seekApproval]->(a:Approver),
      (p)-[:belongtoDept]->(d:Department),
      (p)-[:hasCase]->(c:Case),
      (c)-[:hasAction]->(ac:Action)
RETURN p, a, d, c, ac;

'''