// Création des utilisateurs métiers à la première initialisation
db = db.getSiblingDB('datasolutech');

db.createUser({
  user: "admin_datasolutech",
  pwd: "mdp_admin_datasolutech",
  roles: [{ role: "dbOwner", db: "datasolutech" }]
});

db.createUser({
  user: "app_migration",
  pwd: "mdp_app_migration",
  roles: [{ role: "readWrite", db: "datasolutech" },{ role: "dbAdmin", db: "datasolutech" }]
});

db.createUser({
  user: "analyste_lecture",
  pwd: "mdp_analyste_lecture",
  roles: [{ role: "read", db: "datasolutech" }]
});



// Source: https://www.mongodb.com/docs/manual/reference/method/db.createUser/
// Source: https://www.mongodb.com/docs/manual/reference/method/db.getSiblingDB/
// La fonction getSiblingDB permet de se positionner explicitement sur la base cible avant de créer les utilisateurs. Sans cela, MongoDB utiliserait la base par défaut test, ce qui provoquerait des erreurs d’authentification.