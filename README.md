nous creerons une platform qui gere et fournir des coffre-fort au client. le platform permet d'ajouter des nouveau client et alerter les client s'il ya une detection de forçage de coffre ou mot de passe erroné

le coffre fort est composer de esp32 et keypad 4*3, capteur vibration, le coffre n'est pas censé ouvrir offline seulement online,le donner sont centraliser  sur le platform

premierement, le coffre lit le mot de passe et le vibration en permanence, il a une menu principal pour se conecter au wifi ou changer de mot de passe ou reinitialiser le mot de passe a partir du platform par un mot de passe temporaire envoyer par le platform est confirmer par le proprietaire.le coffre doit rester connecter au serveur pour suivre le log du coffre , s'il n'est pas connecter le coffre ne s'ouvre pas a moins que le mot de passe temporaire est envoyée par le serveur au client par facebook,et il enregistre les tentative offline et nregistre dans un base et synchroniser au moment de connection au serbveur.il envoye aussi toute log ver le serveur pour la journalisation.

pour la reinitialisation du mot de passe, le client selectione le menu reinitialisation puis valider et l'esp envoye une demande de reinitialisation et il change le mot de passse du coffre en ligne et envoye le mot de passe au client.

au niveau de base de donné, client, coffre, log, command,

sur le front-end, une interface administration pour enregistrer une client au coffre , et crud pour la modification de donner ou suppresion,visualisation de box non connecté en peranence et alerter le proprietaire si le box est offline durant 3h, une interface aussi pour le client pour qu'il peuve voir lhistorique de son box
