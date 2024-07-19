from neo4j import GraphDatabase
import pandas as pd

#docker pull neo4j
#Q1 numbers keep changing, Q2 getting connection error

uri =   "neo4j+s://27779763.databases.neo4j.io" #neo4j+s://74146678.databases.neo4j.io"  # or bolt://localhost:7687 for local 
username = "neo4j"
password = "TOCv55tlTImLlACrhOEm9o_zph13D6LkpsaAOnTjnW4"

# Create the driver instance
driver = GraphDatabase.driver(uri, auth=(username, password))

belongtoDept_data = {
    "Department": ["HR", "HR", "HR", "FIN", "LOB", "LOB"],
    "Person": ["Gerard", "Rachel", "Lee", "Jocelyn", "Dorothy", "Albert"],
    "Role": ["Head", "Team Member", "Team Member", "Head", "Team Member", "Team Member"]
}

seekApproval_data = {
    "Approver": ["Ken", "Gerard", "Ken", "Keith", "Keith"],
    "Person": ["Gerard", "Lee", "Jocelyn", "Dorothy", "Albert"]
}

hasCase_data = {
    "Person": ["Gerard", "Jocelyn", "Dorothy", "Rachel", "Gerard"],
    "CaseID": [1, 2, 3, 4, 5],
    "CaseDescription": [
        "Lack of Resource", "Lack of Fund", "Poor Delivery Quality",
        "Need more room", "Need to create more awareness"
    ]
}

hasAction_data = {
    "CaseID": [1, 2, 3, 4, 5],
    "Action": ["Find Resource", "Sell Project", "Train Resource", "Find Resource", "Brand Marketing"],
    "Status": ["Not Started", "In Progress", "Close", "In Progress", "In Progress"]
}

# Create DataFrames
belongtoDept = pd.DataFrame(belongtoDept_data)
seekApproval = pd.DataFrame(seekApproval_data)
hasCase = pd.DataFrame(hasCase_data)
hasAction = pd.DataFrame(hasAction_data)
# print(belongtoDept)
# print(seekApproval)
# print(hasCase)
# print(hasAction)

# Create nodes and relationships
def create_graph(tx):
    for index, row in belongtoDept.iterrows():
        tx.run("""
            MATCH (p:Person {name: $person})
            MATCH (d:Department {name: $dept})
            MERGE (p)-[:belongtoDept]->(d)
            """, person=row['Person'], dept=row['Department'])

        # tx.run("CREATE (:Person {name: $name, department: $department, role: $role})",
        #        name=row['Person'], department=row['Department'], role=row['Role'])
    
    for index, row in seekApproval.iterrows():
        tx.run("""
            MATCH (a:Person {name: $approver})
            MATCH (p:Person {name: $person})
            CREATE (p)-[:seekApproval]->(a)
            """, approver=row['Approver'], person=row['Person'])
    
    for index, row in hasCase.iterrows():
        tx.run("""
            MATCH (p:Person {name: $person})
            CREATE (c:Case {id: $case_id, description: $description})
            CREATE (p)-[:hasCase]->(c)
            """, person=row['Person'], case_id=row['CaseID'], description=row['CaseDescription'])
    
    for index, row in hasAction.iterrows():
        tx.run("""
            MATCH (c:Case {id: $case_id})
            CREATE (c)-[:hasAction {status: $status}]->(:Action {name: $action})
            """, case_id=row['CaseID'], action=row['Action'], status=row['Status'])

#1a) How many people are in the LOB department?
def get_lob_count(tx):
    result = tx.run("MATCH (p:Person {department: 'LOB'}) RETURN count(p) AS count")
    return result.single()["count"]

#1b)How many case loads are there for the HR department?
def get_hr_cases(tx):
    result = tx.run("""
        MATCH (p:Person {department: 'HR'})-[:HAS_CASE]->(c:Case)
        RETURN count(c) AS case_count
    """)
    return result.single()["case_count"]

with driver.session() as session:
    session.execute_write(create_graph)
    lob_count = session.execute_read(get_lob_count)
    print(f"Number of people in LOB department: {lob_count}")
    hr_case_count = session.execute_read(get_hr_cases)
    print(f"Number of cases in HR department: {hr_case_count}")

#2a) 
def link_prediction(tx):
    query = """
    CALL gds.nodeSimilarity.write({
        nodeProjection: 'Person',
        relationshipProjection: {
            SEEKS_APPROVAL_FROM: {
                type: 'SEEKS_APPROVAL_FROM',
                orientation: 'UNDIRECTED'
            }
        },
        similarityCutoff: 0.5,
        writeRelationshipType: 'SIMILAR',
        writeProperty: 'score'
    })
    YIELD nodesCompared, relationshipsWritten, similarityDistribution
    """
    tx.run(query)
    
    # Now infer if Rachel's approving officer can be Gerard
    prediction_query = """
    MATCH (r:Person {name: 'Rachel'})-[:SIMILAR]-(g:Person {name: 'Gerard'})
    RETURN g.name AS name, g.score AS score
    """
    result = tx.run(prediction_query)
    return result.single()

with driver.session() as session:
    session.execute_write(link_prediction)
    prediction = session.execute_read(link_prediction)
    if prediction:
        print(f"Rachel's predicted approving officer is: {prediction['name']} with similarity score: {prediction['score']}")
    else:
        print("No prediction available for Rachel and Gerard.")


#2b)

driver.close()

