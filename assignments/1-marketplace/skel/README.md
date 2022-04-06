331CB - Stoica Vlad Marian

#Tema 1-Marketplace

##Organizare
Pentru rezolvarea temei, in clasa de marketplace, am 
folosit 2 lock-uri (lock_consumer, lock_producer) pentru
a acoperi sectiunile critice ale marketplace-ului.
Aceste sctiuni critice apar in momentul in care un produs
este adaugat sau eliminat dintr-un cos de cumparaturi, sau
cand un producator publica un nou produs. Pentru a elimina
functiile de acquire si release, s-a folosit keyword-ul "with".
In marketplace, exista o lista de producatori, fiecare avand
o lista cu produsele publicate, si o lista de cart-uri, cu
produsele adaugate.*
Un caz nespecificat in enunt si care nu apare in teste este
trimiterea unui parametru gresit la functiile de "publish",
"add_to_cart", "remove_from_cart". Daca id-ul cart-ului sau
al producatorului nu exista, ar trebui intoarsa o eroare.
Clasele de producer si consumer apeleaza metode din referinta
clasei marketplace pentru a realiza operatii pe produse.

##Implementare
Tema a fost implementata integral, inclusiv testele unitare
si loggerul. Ca nivel de dificultate, consider ca este usoara
spre mediu, singurele "obstacole" fiind intelegerea testelor si
a modului in care datele de intrare sunt organizate si cand 
un cart ar trebui sa apeleze metoda "place_order". Elementele
de threading sunt clare si usor de inteles (thx lab 3 ASC).

##Resurse utilizate
https://ocw.cs.pub.ro/courses/asc/laboratoare/03
https://ocw.cs.pub.ro/courses/asc/laboratoare/02
https://stackoverflow.com/questions/40088496/how-to-use-pythons-rotatingfilehandler
https://www.youtube.com/watch?v=jxmzY9soFXg
https://stackoverflow.com/questions/10525185/python-threading-how-do-i-lock-a-thread

##Git
https://github.com/StoicaVlad/ASC---Marketplace.git
