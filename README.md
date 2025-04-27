# epic_event

the_admin
secret2025!
role: admin

secret
secret1234
role: manager

the_manager
secret2025!
role: manager

the_sailor
secret2025!
role: sailor

test_create_sailor
test1234
role: sailor

the_support
secret2025!
role: support

Scénario de test:

tous les roles peuvent read les infos

equipe gestion : créé 2 sailors, créé 2 support
sailor 1 : créé 2 clients (peut modifier)
sailor 2 : mettre à jour 1 client dont il n'est pas responsable --> pas le droit normalement

équipe gestion créé 2 contrats (peut modif)

sailor 1 : update contrats de ses clients, créé un evenement pour un client qui a signé, ne peut pas pour un client qui n'a pas signé
sailor 2 : mettre à jour 1 contrat d'un client dont il n'est pas responsable --> pas le droit normalement

equipe gestion : update 1 un evenement pour associer un support

supp 1: maj seulement les event dont il est resp
supp 2 : essaye de maj l'event --> pas le droit normalement
