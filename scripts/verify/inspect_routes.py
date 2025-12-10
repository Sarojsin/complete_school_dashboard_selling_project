from main import app
from fastapi.routing import APIRoute

def inspect_routes():
    with open("routes.txt", "w") as f:
        f.write("Inspecting routes...\n")
        for route in app.routes:
            if isinstance(route, APIRoute):
                if "authority" in route.path and "fee" in route.path:
                    f.write(f"Path: {route.path}, Methods: {route.methods}, Name: {route.name}\n")

if __name__ == "__main__":
    inspect_routes()
