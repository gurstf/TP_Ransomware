Q1: L'algorithme c'est le XOR dans la fonction xorcrypt, il est robuste, ça veux dire que il est previsible et simple, parce que l'operation c'est juste un xor entre données.

Q2: Non hacher le sel et la clef directement il complique le déchiffrement en générant toujours un hachage unique et ne peut pas être rétrocalibré en évitant brute force,  de sorte que les mêmes mots de passe ne produisent pas la même valeur de hachage.
Avec le HMAC, une couche de protection supplémentaire peut être générée et le rétrocalcul peut être difficile.

Q3: Il est préférable de vérifier s’il existe déjà un jeton.bin et la création d’un dossier du même nom peut entraîner des conflits de noms et des pertes de données, ce qui permet également d’économiser de l’espace et d’éviter les erreurs de programmation.

Q4:La vérification de la clé dépend si elle est utilisée pour chiffrer ou déchiffrer, nous pouvons vérifier si la clé est bonne en l’utilisant pour déchiffrer un message déjà crypté, dans le cas où notre projet n’est pas une méthode viable pour l’attaquant et la victime, Donc, en tant que pirate informatique, une méthode de vérification serait de recevoir l’entrée de la victime et de la comparer avec la clé générée par le programme.

YANO, Gustavo Akio
