# USOS Grade Fetcher

## Opis
USOS Grade Fetcher to skrypt do pobierania ocen z systemu USOS. Skrypt automatycznie loguje się na konto studenta i pobiera oceny z wybranego semestru. Wartości są wyświetlane w formie tabeli w konsoli.

## Wymagania
* Przed uruchomieniem skryptu należy zainstalować wszystkie wymagane pakiety. Wymagane jest posiadanie środowiska z zainstalowanym Pythonem oraz bibliotekami.
* Przeglądarka: Skrypt używa przeglądarki (np. Chrome), więc musisz mieć zainstalowaną przeglądarkę.

### Instalacja zależności
Zainstaluj wymagane pakiety z pliku `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Uruchomienie skryptu

Aby uruchomić skrypt, podaj login i hasło jako argumenty w linii poleceń.

### Przykład uruchomienia
```bash
python UsosGrades.py <login> <hasło>
```

Gdzie:

* \<username> — Twój login do USOS (identyfikator indeksu lub PESEL).
* \<hasło> — Twoje hasło do USOS.

### Przykład
```bash
python UsosGrades.py 000000 supertajnehaslo123
```

Po uruchomieniu skrypt automatycznie zaloguje się na Twoje konto USOS i pobierze oceny z wybranego semestru. Oceny zostaną wyświetlone w konsoli w formie tabeli.
