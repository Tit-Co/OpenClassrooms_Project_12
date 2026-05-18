import os

USERNAME = os.getenv("DB_USERNAME")
PASSWORD = os.getenv("DB_PASSWORD")
DATABASE = os.getenv("DATABASE")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")

SENTRY_KEY = os.getenv("SENTRY_KEY")

PERMISSIONS = {
    "MANAGER": ["display:manager", "display:commercial", "display:technician", "create:collaborator",
                "update:collaborator", "delete:collaborator", "display:contract", "display:client", "display:event",
                "create:contract", "update:contract", "delete:contract", "update:event", "delete:event",
                "filter:event", "filter:client", "filter:manager", "filter:commercial", "filter:technician"],

    "COMMERCIAL": ["display:manager", "display:commercial", "display:technician", "display:contract", "display:client",
                   "display:event", "create:client", "update:client", "delete:client", "update:contract",
                   "filter:contract", "create:event", "filter:client", "filter:manager", "filter:commercial",
                   "filter:technician"],

    "TECHNICIAN": ["display:manager", "display:commercial", "display:technician", "display:contract", "display:client",
                   "display:event", "update:event", "filter:event", "filter:client", "filter:collaborator",
                   "filter:manager", "filter:commercial", "filter:technician"]
}
