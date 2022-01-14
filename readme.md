Gabriel Zabielski
--
Grupa: Z707

Link do projektu: 
(https://jachty.gzabielski.click/)

#### Użyty AWS:
1. Cognito:
   1. Dostarcza wszystkie funkcje związane z zarządzaniem użytkownikami - rejestracja, logowanie i autoryzacja
   2. Generuje `access_token`
2. API Gateway:
   1. Integracja innych serwisów:
      1. (S3) serwuje statyczny kontent, 
      2. (Lambda Functions) proxy + mapowanie parametrów
      3. (Cognito) Kontrola dostępu - weryfikacja `access_token`
   2. Wystawienie zintegrowanych serisów (jako endpointy) do publicznego internetu
3. S3 - przechowywanie statycznego kontentu
4. Lambda Functions:
   1. Wykonywanie kodu python'owego
   2. Komunikacja z DynamoDB
5. DynamoDB - nosql Amazona
6. Route 53 - DNS

#### Niektóre endpointy wymagają autoryzacji - Jak działa autoryzacja:
1. `Authorization` header z przypisanym mu `access_token` musi znaleźć się w zapytaniu 
2. API Gateway sprawdza podany `access_token` w Cognito

#### Diagram
[Link](https://s3.eu-central-1.amazonaws.com/jachty.gzabielski.click/jachty.html)

#### Swagger documentation
[Swagger](jachty-any-swagger-apigateway.yaml)