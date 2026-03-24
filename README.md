# 1. Praktiskais darbs tēmā Mākslīgajais intelekts
## Lai palaistu spēli nepieciešams palaist start.py
## :bangbang: Pirms spēles palaišanas pārliecinieties vai ir instalēta PyQt6 bibliotēka <br> To var izdarīt ar komandu `pip install PyQt6`
**start.py** -> sākuma GUI logs, kurā tiek iegūta informācija par to, kurš sāk spēli, cik gara būs skaitļu virkne un kāds algoritms tiks izmantots.<br>
Pēc tam tiek atvērts **game.py** logs, kurā notiek pati spēle - tur tiek izmantotas metodes no **engine.py**, atjaunināti punkti un mērīts datora gājiena laiks<br>
**engine.py** -> šajā failā ir aprakstīti visi spēles algoritmi, un tur arī tiek aprēķināts algoritma virsotņu skaits, kas vēlāk tiek izmantots statistikas aprēķināšanai.<br>
**stats.py** -> statistikas logs, kurā visa informācija tiek saglabāta CSV failā.

