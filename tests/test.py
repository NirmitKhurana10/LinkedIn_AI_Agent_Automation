import sys, os
sys.path.insert(0, os.getcwd())

from src.database.db_manager import DatabaseManager

db = DatabaseManager()
db.init_database()

# print(os.path.exists(db.db_path))


# ----------------------- Test add project -----------------------

# project_id = db.add_project(
#     title="Ikea Operational Waste Mitigation and Demand Forecasting Engine",
#     description="""The Operational Waste Mitigation & Demand Forecasting Engine is an enterprise-grade automation system designed to eliminate operational inefficiencies in food service operations. Built for IKEA's disposable management operations, this system transforms raw sales data into actionable insights while maintaining real-time inventory control.

#                     The Problem:
#                     Manual tracking of disposable item usage leads to stockouts and over-ordering
#                     No correlation between food sales and disposable consumption
#                     Reactive inventory management resulting in operational waste
#                     Time-consuming manual data entry and reconciliation
#                     The Solution: This engine automates the entire workflow from data ingestion to inventory optimization:
#                     Automated Data Processing: Ingests daily sales reports and transforms them into structured data
#                     Real-time Inventory Tracking: Automatically updates stock levels based on actual usage
#                     Demand Forecasting: Analyzes consumption patterns to predict future needs
#                     Zero Manual Intervention: Fully automated GitHub Actions pipelines running on schedule
#                     Waste Reduction: Data-driven ordering prevents both stockouts and excess inventory. """,
#     tech_stack="Python, PostgreSQL, Github Actions, PowerBI, Excel, Sharepoint, JIRA",
#     github_url="https://github.com/NirmitKhurana10/Operational-Waste-Mitigation-Demand-Forecasting-Engine",
#     key_learnings="Learnt to auomate CI/CD Pipelines, build Data Visualizations, clean data through python cripts, agile methodology followed during the project."
# )

# print(f"Returned ID: {project_id}")


# ----------------------- Test get project -----------------------


# projects = db.get_projects()
# print(f"Total projects: {len(projects)}")
# for p in projects:
#         print(f"\nProject Id: {p['id']} \nTitle: {p['title']} \nTech Stack: {p['tech_stack']}")



# ----------------------- Get Least Recent Posted Project -----------------------

least_recent_project = db.get_least_recent_posted_project()
print(f"\nLeast recent posted project: ")
print(f"\nProject Id: {least_recent_project['id']} \nTitle: {least_recent_project['title']} \nTech Stack: {least_recent_project['tech_stack']}")
