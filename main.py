from graph import build_graph
from schemas.state import AgentState
import uuid

#graph visualization
def save_graph_visualization(graph):
    png_bytes = graph.get_graph().draw_mermaid_png()
    with open("workflow.png", "wb") as f:
        f.write(png_bytes)

app = build_graph()

save_graph_visualization(app)

print("🤖 CorpAssist AI (LangGraph)")
print("Type 'exit' to quit\n")

while True:
    query = input("Employee: ")

    if query.lower() == "exit":
        break

    state = AgentState(user_id=str(uuid.uuid4()),user_query=query)
    result = app.invoke(state)

    print("\nBot:", result.get("response", "Sorry for the inconvenience.\n"))
