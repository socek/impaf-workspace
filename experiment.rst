1. Testing and mocking
======================

Próba mockowania  Jinja2Application poprzez dziedziczenie po Jinja2Application zakończona porażką.
Trzeba dziedziczyć po rodzicu Jinja2Application, aby dobrze to zmockować.

2. Settings
===========

Podział settingsów na "project / envoritment / dynamic"

3. Ruby -> result as jinja2 or json or xml
==========================================

Tutaj zamiast "return as html" można po prostu można odpowiednio dziedziczyć.

4. super jako dekorator
=======================

Tutaj niestety pomysł się nie sprawdził, gdyż super() dla rodzica z użytym dekoratorem
zwróci nam dekorator, a nie konkretną metodę.

5. Konstruktor kopiujący
========================

Czyli jak zrobić konstruktor kopiujący z pomocą .__dict__

6. Konfiguracja == wysoki próg wejścia
======================================

Aby skonfigurować całość, trzeba wiedzieć jak to działa od początku do końca.
Example hello world?
