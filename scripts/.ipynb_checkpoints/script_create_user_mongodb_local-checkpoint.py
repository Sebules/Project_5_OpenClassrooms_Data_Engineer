from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/admin")

db = client["datasolutech"]

users = [
    {
        "user": "admin_datasolutech",
        "pwd": "mdp_admin_datasolutech",
        "roles": [{"role": "dbOwner", "db": "datasolutech"}]
    },
    {
        "user": "app_migration",
        "pwd": "mdp_app_migration",
        "roles": [
            {"role": "readWrite", "db": "datasolutech"},
            {"role": "dbAdmin", "db": "datasolutech"}
        ]
    },
    {
        "user": "analyste_lecture",
        "pwd": "mdp_analyste_lecture",
        "roles": [{"role": "read", "db": "datasolutech"}]
    }
]

for u in users:
    db.command("createUser", u["user"], pwd=u["pwd"], roles=u["roles"])
    print(f" User créé : {u['user']}")