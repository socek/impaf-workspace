Temat: Jak działa super?
Jest jedna funkcjonalność Pythona, której wszyscy używają bardzo szczątkowo, gdyż panuje opinia iż nadużywanie jej może doprowadzić do nieokreślonego działania aplikacji. Tą funkcjonalnością jest wielodziedziczenie. Postaram się w kilku słowach pokazać jak działa "Method Resolution Order" w Pythonie (wybaczcie, nie znalazłem dobrego tłumaczenia tej nazwy). Postaram się wam pokazać jak można użyć "super", aby zamockować i przetestować przykładową klasę.
Zacznijmy jednak od teorii. W programowaniu panuje przekonanie, że wielodziedziczenie jest złe, gdyż może występować "the diamond problem", czyli sytuacja, w której klasa dziedziczy po dwóch klasach, a te dwie klasy dziedziczą po jednej i tej samej. Gdybyś my w takiej sytuacji (powiedzmy w C++) we wszystkich klasach zaimplementowali taką samą metodę, to język nie wiedziałby którą metodę wywołać najpierw.  W Pythonie ten problem nie występuje, dzięki MRO, który to jest implementacją algorytmu "C3 linearization"*. Wprowadzono go w wersji 2.3 (new style classes) oraz w Perl 5 i Parrot. Niestety nie są znane mi inne języki, które by implementowały ten algorytm.
Dodatkowym atutem Pythona jest fakt, iż wywołanie metody rodzica, jest jawne w metodzie potomka. Dzięki temu, można kod rodzica uruchomić nie tylko przed wywołaniem własnej metody, ale na przykład w środku. Daje nam to naprawdę duże pole do manewru.



* https://en.wikipedia.org/wiki/C3_linearization
