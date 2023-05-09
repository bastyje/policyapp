## Opis problemu

PolicyApp jest aplikacją w formie usługi sieciowej (ang. webservice), w stylu RESTopodobnym, służącą do wykonywania różnych operacji 
na polisach komunikacyjnych. Jest to rozwiązanie dla wszelkich brokerów ubezpieczeniowych posiadających swoje systemy
informatyczne, jednak bez modułu polisowego. PolicyApp można łatwo zintegrować albo bezpośrednio już z interfejsem
użytkownika albo z backendem aplikacji i korzystając z możliwości własnego systemu i PolicyApp przeprowadzać konkretne
procesy biznesowe świata polisowego.

## Analiza funkcjonalna

### Rejestracja

```http request
POST http://localhost:8005/brokers
```
```json
{
    "name": "Broker Name"
}
```

Operacją, którą każdy użytkownić usługi musi wykonać na samym początku to rejestracja w systemie. Broker
ubezpieczeniowy tworzy swoje konto, które jest powiązane jest z konkretnym kluczem do API, który niezbędny jest do
przeprowadzania wszelkich operacji w webserwisie.

### Dodanie ubezpieczyciela

```http request
POST http://localhost:8005/insurers?api_key=api_key
```
```json
{
    "name": "InsurerName S.A.",
    "krs": "0000009831",
    "taxId": "5260251049"
}
```

Nazwa akcji właściwie opisuje cału jej sens. Polega ona na dodaniu encji ubezpieczyciela (Insurer), która niezbędna
będzie do zawarcia polisy, bądź do wykonania niektórych raportów.

### Dodanie szablonu oferty

```http request
POST http://localhost:8005/policies/offer-template?api_key=api_key
```
```json
{
    "name": "TPL for cars older than 2010",
    "insurerId": 1,
    "quotationAlgorithm": "import datetime\nfrom _decimal import Decimal\n\nfrom data_access.entities.dict.currency import CurrencyEnum\nfrom data_access.entities.dict.risk import RiskEnum\n\n\nif vehicle.ProductionYear < 2010:\n    risk = PolicyRisk()\n    risk.CurrencyId = CurrencyEnum.EUR.value\n    risk.RiskId = RiskEnum.TPL.value\n    risk.CreationDate = datetime.date.today()\n    risk.StartDate = datetime.date.today()\n    risk.EndDate = datetime.date.today() + datetime.timedelta(days=2)\n    risk.Premium = Decimal(100.0)\n    policy_risks.append(risk)\n\n    risk1 = PolicyRisk()\n    risk1.CurrencyId = CurrencyEnum.EUR.value\n    risk1.RiskId = RiskEnum.TPL.value\n    risk1.CreationDate = datetime.date.today()\n    risk1.StartDate = datetime.date.today()\n    risk1.EndDate = datetime.date.today() + datetime.timedelta(days=2)\n    risk1.Premium = Decimal(200.0)\n    policy_risks.append(risk1)",
    "validFrom": "2022-02-02",
    "validTo": "2024-02-02"
}
```

Szablon oferty jest obiektem, z którego na podstawie jego pól można utworzyć ofertę polisy (oferta od polisy różni się
tym, że oferta nie jest zawartą polisą, a jedynie jej symulacją/podglądem dla klienta). Obiekt szablonu oferty składa
się z ubezpieczyciela (ponieważ on ustala sposób wyliczania składek), zakresu dat obowiązywania oraz algorytmu
liczącego. Algorytm liczący służy do przeliczenia ryzyk powiązanych z polisą dla danego pojazdu na podstawie
parametrów pojazdu. Algorytm jest kodem napisanym w języku Python, wykonywanym dynamicznie w tracie procesu tworzenia
oferty.

### Stworzenie oferty dla danego pojazdu i szablonu oferty

```http request
POST http://127.0.0.1:8005/policies/offer?api_key=api_key&policy_offer_template_id=1
```
```json
{
    "person": {
        "name": "Janusz",
        "lastName": "Kowalski",
        "birthDate": "2000-01-01",
        "pesel": "01210187654",
        "email": "janusz.kowalski@gmail.com",
        "phoneNumber": "509876543"
    },
    "vehicle": {
        "make": "Alfa Romeo",
        "model": "Julia",
        "registrationNumber": "WE1234",
        "vin": "12345678901234567",
        "productionYear": 2009,
        "registrationDate": "2020-12-12",
        "ownerCount": 1
    }
}
```

Podczas tej akcji dzieje się kilka rzeczy:
- tworzony jest pojazd (jeżeli nie istnieje drugi o takim samym numerze VIN)
- tworzona jest osoba (jeżeli nie istnieje druga o takim samum numerze PESEL)
- obliczane są ryzyka dla oferty
- tworzona jest oferta

### Zawarcie polisy na podstawie oferty

```http request
POST http://127.0.0.1:8005/policies/4/issue?api_key=api_key
```

Akcja tworzy na podstawie oferty odpowiadającą jej polisę.

### Pobranie raportów na temat polis

```http request
GET http://127.0.0.1:8005/policies?api_key=aki_key
```

Za pomocą tej metody HTTP można uzyskać wiele różnych rodzajów raportów na temat bazy polis.
Wybór rodzaju raportu sterowany jest za pomocą `query parameters` podanych po URI.

#### Pobranie polis per broker

Zwraca listę ryzyk wraz z danymi na temat poliy, pojazdu, osoby i ubezpieczyciela dla brokera
o danym id.
Wymagane `query parameters` do uruchomienia tego raportu to:
- broker_id: int

#### Pobranie polis per ubezpieczyciel

Zwraca listę ryzyk wraz z danymi na temat poliy, pojazdu, osoby i brokera dla ubezpieczyciela
o danym id.
Wymagane `query parameters` do uruchomienia tego raportu to:
- insurer_id: int

#### Pobranie podsumowania polis per ubezpieczyciel

Zwraca zsumowane składki dla wszystkich polis dla ubezpieczyciela o danym id.
Wymagane `query parameters` do uruchomienia tego raportu to:
- insurer_id: int
- is_summary: bool = True

#### Pobranie polis per pojazd

Zwraca listę ryzyk wraz z danymi na temat poliy, osoby, ubezpieczyciela i brokera dla pojazdu
o danym id.
Wymagane `query parameters` do uruchomienia tego raportu to:
- vehicle_id: int

#### Pobranie polis per osoba

Zwraca listę ryzyk wraz z danymi na temat poliy, pojazdu, ubezpieczyciela i brokera dla pojazdu
o danym id.
Wymagane `query parameters` do uruchomienia tego raportu to:
- person_id: int

## Schemat bazy

![Database diagram](https://github.com/bastyje/policyapp/blob/main/docs/database_diagram.png?raw=true)

[Skrypt inicjalizujący bazę danych](https://github.com/bastyje/policyapp/blob/main/database/scripts/V1.0.20230405.0.1__create_base_structure.sql)

## Opis realizacji

### Wykorzystane technologie

Zbiór technologii w których został wykonany projekt:
- [Microsoft SQL Server](https://learn.microsoft.com/en-us/sql/?view=sql-server-ver16) - baza danych
- [Python3.10](https://www.python.org/) - aplikacja
  - [fastapi](https://fastapi.tiangolo.com/lo/) + [uvicorn](https://www.uvicorn.org/) - serwer http
  - [dependency_injector](https://python-dependency-injector.ets-labs.org/) - zarządzanie zależnościami zgodnie ze wzorcem [Dependency injection](https://en.wikipedia.org/wiki/Dependency_injection)
  - [pymssql](https://www.pymssql.org/) + [SQLAlchemy](https://www.sqlalchemy.org/) - połączenie z bazą danych i mapowanie obiektowo-relacyjne
  - [pydantic](https://docs.pydantic.dev/latest/) - obsługa anotacji typów
- [flyway](https://flywaydb.org/) - zarządzanie wersjami bazy danych i migracjami danych
- [docker](https://www.docker.com/) - kontreneryzacja środowiska

### Realizacja bazy danych

Wszelkie operacje na bazie danych (między innymi tworzenie i edycja tabel) zapisywane są w
odpowiednio nazwanych plikach w katalogu [`database/scripts`](https://github.com/bastyje/policyapp/tree/main/database/scripts).
W zależności od tego, czy ma być to jednorazowa migracja, czy skrypt ma się wykonywać przy każdorazowym uruchomieniu
narzędzia `flyway` umieszczony jest w odpowiednim katalogu i nazwany według odpowiedniej konwencji.

W pierwszym pliku jednorazowej migracji tworzona jest pierwotna forma bazy danych. W plikach wykonywanych powtarzalnie
uzupełniane danymi są tabele ze schemy `dict`, czyli słowniki oraz aktualizowane są funkcje SQL.

W schemie `dbo` znajdują się wszelkie tabele gromadzące dane operacyjne bądź archiwalne. W schemie `conf` znajdują
się dane konfiguracyjne. Zaś w schemie `security` przechowywane są dane o krytycznym znaczeniu dla bezpieczeństwa
aplikacji i użytkowników.

W sytuacji potencjalnej rozbudowy bazy danych o kolejne tabele, wykonanie zmian może zostać wprowadzone bezboleśnie
za pomocą kolejnego skryptu wykonywanego przez `flyway`. O ile skrypt będzie zgodny ze składnią `TSQL` i nie będzie
naruszał integralności danych w bazie, to powinien się wykonać, a wersja bazy danych powinna zostać podniesiona.

### Realizacja aplikacji webowej

#### Architektura

Aplikacja w języku Python napisana została zgodnie z architekturą warstwową, patrząc od strony przychodzących
żądań HTTP:
- warstwa controllerów - obsługująca na poziomie technicznym żądania HTTP i przekazująca je do niższej warstwy;
kod dla tej warstwy znajduje się w katalogu `src/webapi`
- warstwa serwisów - serwisy realizują zadania logiki aplikacji; kod dla tej warstwy znajduje się w katalogu
`src/services`
- warstwa repozytoriów - warstwa dostępu do danych; abstracja modelu obiektowego reprezentująca relacyjną bazę danych;
kod dla tej warstwy znajduje się w katalogu `src/data_access`

#### Konfiguracja

Konfiguracja aplikacji, czyli dane zmienne, takie jak np. hasło do bazy danych przechowywane są w pliku
`src/config/appsettings.json`. Następnie JSON jest deserializowany do obiektu reprezentującego konfigurację
aplikacji i ten obiekt przekazywany jest do kontenera DI odpowiedzialnego za mechanizm Dependency Injection

#### Dependency Injection

Mechanizm Dependency Injection zrealizowany jest z pomocą bibioteki `dependency_injector`. W pliku `src/di_container.py`
w kontenerze DI rejestrowane są wszystkie klasy świadczące pewne usługi w aplikacji. Później te klasy, na podstawie
konfiguracji w wyżej wymienionym pliku, wstrzykiwane są innym usługom przez wcześniej wspomniany kontener. Takie
rozwiązanie problemu zależności między klasami w projekcie likwiduje tzw. 'architektoniczne spaghetti', w którym klasy
posiadają bardzo skomplikowane zależności. `dependency_injector` pozwala tym bardzo łatwo zarządzać.

#### Połączenie z bazą danych

Połączenie z bazą danych realizowane jest dzięki bibliotece `pymssql`, która zajmuje się takimi aspektami jak
utrzymywanie połączenia z bazą. Mimo tej ważnej roli, w tym projekcie dużo odwołań do wspomnianej biblioteki nie widać,
ponieważ wszystkie te operacje 'pod spodem' realizuje `SQLAlcchemy` - ORM, czyli biblioteka służąca do mapowania
relacyjno-obiektowego. Krótko mówiąc, jestem w stanie w kodzie w Pythonie zdefiniować sobie klasy, które reprezentują
encje w bazie danych i za pomocą tych encji wykonywać operacje bazodanowe. Możliwości `SQLAlchemy` są na tyle
rozbudowane, że właściwie nie trzeba wcześniej tworzyć struktury bazy danych skryptami SQL-owymi, tylko ORM jest za nas
w stanie to zrobić.

## Dokumentacja działania

### Wprowadzanie danych

Pierwszą operacją jest rejestracja brokera:
![add broker](https://github.com/bastyje/policyapp/blob/main/docs/create_broker.png?raw=true)

Operacja zwraca `api_key`, za pomocą którego broker będzie mógł się uwierzytelniać.

Następnie tworzonych jest dwóch ubezpieczycieli:
![add insurer 1](https://github.com/bastyje/policyapp/blob/main/docs/add_insurer_1.png?raw=true)
![add insurer 2](https://github.com/bastyje/policyapp/blob/main/docs/add_insurer_2.png?raw=true)

Operacje zwracają `id` utworzonego ubezpieczyciela.

Następnie tworzone są szablony ofert i przypisane są do kolejnych ubezpieczycieli:
![add offer template 2](https://github.com/bastyje/policyapp/blob/main/docs/add_offer_template_for_insurer_2.png?raw=true)
![add offer template 1](https://github.com/bastyje/policyapp/blob/main/docs/add_offer_template_for_insurer_1.png?raw=true)

Tak jak w przypadku poprzednich akcji, rezultatem żądania są identyfikatory szablonów ofert.

Z obecnie znajdującymi się w bazie danymi można już utworzyć ofertę ubezpieczenia dla pojazdu:
![create offer 1](https://github.com/bastyje/policyapp/blob/main/docs/create_offer_from_template_1_1.png?raw=true)
![create offer 2](https://github.com/bastyje/policyapp/blob/main/docs/create_offer_from_template_2_1.png?raw=true)
![create offer 3](https://github.com/bastyje/policyapp/blob/main/docs/create_offer_from_template_2_2.png?raw=true)

Każda z akcji zwraca `id` oferty utworzonej w rezultacie przeliczenia ryzyk z użyciem 
algorytmu liczącego zapisanego w polu `PolicyOfferTemplate.QuotationAlgorithm`.

Gdy oferty spodobają się klientowi, można na ich podstawie stworzyć polisę:
![issue policy 1](https://github.com/bastyje/policyapp/blob/main/docs/issue_policy_from_offer_1.png?raw=true)
![issue policy 2](https://github.com/bastyje/policyapp/blob/main/docs/issue_policy_from_offer_2.png?raw=true)
![issue policy 3](https://github.com/bastyje/policyapp/blob/main/docs/issue_policy_from_offer_3.png?raw=true)

Zawarte `Polisy` znajdują się w tej samej tabeli co `Oferty` ze względu na identyczny model encji.
Domenowo różnią się tym, że Oferta jest niezawartą Polisą.

### Raporty

W celu lepszej wizualizacji wyglądu raportów wprowadzonych zostało trochę dodatkowych danych.

#### Podsumowanie składek za polisy danego ubezpieczyciela
![premium summary](https://github.com/bastyje/policyapp/blob/main/docs/summary.png?raw=true)

#### Płaski model polis dla danego brokera
![by broker](https://github.com/bastyje/policyapp/blob/main/docs/by_broker.png?raw=true)

#### Płaski model polis zawartych przez daną osobę
![by person](https://github.com/bastyje/policyapp/blob/main/docs/by_person.png?raw=true)

#### Płaski model polis zawartych na dany pojazd
![by vehicle](https://github.com/bastyje/policyapp/blob/main/docs/vy_vehicle.png?raw=true)
