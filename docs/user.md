<h1>User manual</h1>

## Introduction

Voor je ligt de handleiding voor de nieuwe achterkant van de JD-site. Een website kent een voorkant (front end) en een achterkant (back end). De 'front end' is datgene wat de bezoekers van een site zien. Deze handleiding dient als uitleg voor de 'back end' van de site. Het is de bedoeling dat je via de achterkant aanpassingen doet aan site.

- toegang specificeren, hoe geraak je als AS op de achterkant van de site. 

Het is overigens niet de bedoeling dat je via de nieuwe achterkant allerlei bestanden gaat opslaan, de Wolk blijft voor massaopslag het primaire middel. 



### 1 Pages

1.1 Menustructuur

Via de admin-pagina, onder Content > Pages, is het mogelijk de menustructuur van de site aan te passen. Door met de cursor op het logo van de 'pijltjes omhoog/omlaag' te klikken kan je met het balkje slepen. Je kan het balkje ook laten inspringen zodat er submenu onstaat. Het systeem laat 2 menulagen toe - een hoofdmenu en een submenu - een sub-submenu is dus niet zichtbaar op de site. Een menu verwijderen kan door simpelweg op het kruisje te klikken. 

1.1.1 Homepage

De bovenste regel 'Home' kan je niet verwijderen. Dit is de homepage van je site en staat vast in structuur. Wanneer je op 'Home' klikt, kan je de inhoud van de pagina veranderen. Indien je dit doet zul je onder het content-venster een indeling zien van de kolommen op de homepage. 
Met 'Left column widgets' en 'Right column widgets' kun je een indeling maken met éen of twee kolommen en x-aantal rijen. Dit kan je naar eigen inzicht indelen. Als AS heb je de keuze tussen vaste categorieën die de uiteindelijke kopjes op de Homepage zullen zijn.
Deze categorieën staan vast, wil je een andere titel voor je kopje dan kan je het ICT-team hiervoor mailen. Onder 'horizontal position' kan je bepalen of je de Kopjes links of rechts op de site wilt zien.


1.1.2 Nieuw menu aanmaken

- Ga naar: Content > Pages > Add... > Rich text page
- Title: Naam van het menu
- Status: 'Published' is automatisch aangevinkt. Hierdoor zullen veranderingen aan de site na opslaan meteen zichtbaar op de site.  Wanneer je je veranderingen nog niet aan de buitenwereld wilt tonen kun je ervoor kiezen om bovenaan 'Draft' aan te vinken. De veranderingen zullen dan alleen zichtbaar zijn voor de admin.  
- Published from/Expires on: Hier kan je aangeven wanneer het formulier zichtbaar moet zijn op de website. Klik bij 'Published from' op 'today' en daarnaast bij 'Time' op 'now'. Als je wilt aangeven tot wanneer de content zichtbaar moet zijn op de site kan je een uiterste datum aangeven bij 'Expires on'. Dit is niet noodzakelijk.
- Content: hier zie je een tekstverwerker waar naar believen tekst, afbeeldingen en video invoeren. Zie 2.1 voor uitleg over de tekstverwerker. 
- Klik op 'Save' om de veranderingen door te voeren. 

### 2 Managing Content

De tekstverwerker, het venster waar je inhoud kunt wijzingen zul je vaak gebruiken. Deze heeft verschillende opties die hieronder staan beschreven. 

<strong>2.1 Taakbalk teksverwerker</strong>

Van links naar rechts zie je in de tekstverwerksbalk staan: 


B: <strong>Vetgedrukt</strong>

I: <em>Cursief</em>

Geschakelde ketting: Hyperlink invoegen/veranderen

Gebroken ketting: Hyperlink verwijderen

Scherm met plusje: Afbeeldingen invoegen/veranderen

Filmband: Video invoegen/veranderen (embedden)

Omega: Speciale tekens/symbolen invoegen

HTML: laat de ingevoerde content in HTML-code zien

Tabel: Tabel invoegen

Bulletpoints invoegen

Nummering invoegen

Ongedaan maken (ctrl-z)

Herstellen (ctrl-y)

Drop-down menu: bewerken format van de alinea's

Verrekijker: Zoekfunctie

Venster: Fullscreen


<strong>2.2 Hyperlink invoegen</strong>

Het invoegen van een hyperlink kan als volgt: selecteer de tekst waarvan je een link wilt maken, klik vervolgens op de het icoontje van de kettingschakel in de tekstverwerkersbalk. Vul de URL Link in bij 'General Properties' en  klik op Update. Wil je de link weer verwijderen kan dit door op 'Unlink' te klikken.

<strong>2.3 Afbeelding</strong>

Een afbeelding op nemen in de tekst kan op twee manieren: 

1. Een afbeelding kopiëren/plakken (vanaf een andere site) in het tekstvak. Deze methode is makkelijk en snel, wanneer echter de locatie van de afbeelding op de originele site verandert, is de afbeelding niet meer beschikbaar. 

2. Om te zorgen dat je afbeelding in de toekomst wel beschikbaar blijft kan je de afbeelding uploaden naar de Media Library (en dus onze eigen server). Wanneer dit is gedaan kan je via Insert/Edit Image (icoontje in de tekstverwerkersbalk) een plaatje uploaden vanuit de Media Library. Naast het veld van Image URL zit de 'browse' knop om naar de Media Library te gaan.

<strong>2.4 PDF bestanden</strong>

PDF bestanden zoals het HR en Statuten kan je als volgt insluiten (embedden) op een pagina.

1. Upload het PDF-bestand in de Media Library
2. Open in de backend de pagina waar je het PDF wilt insluiten
3. Ga naar het venster 'Content' en klik in de taakbalk op het HTML icoon (zevende van links)
4. Voer in het HTML venster de onderstaande objectcode in:

```<object data="/static/media/path/bestandsnaam.pdf" width="100%" height=600 type="application/pdf">Oeps, foutje. Hier hoort een document te staan</object>```

5. Waar in de bovenstaande code nu "/static/media/path/bestandsnaam.pdf" staat dien je de locatiecode (tag) van het pdf-bestand te plaatsen. Dit doe je als volgt: 
	a. ga terug naar Media Library
	b. klik op de bestandsnaam van het desbetreffende pdf-bestand
	c. Het pdf-bestand wordt nu geopend in een nieuw venster, in de adresbalk zie je nu de locatiecode van het pdf-bestand staan.
	d. Kopieer deze locatiecode, let wel, de code begint met /static/media/ en eindigt met .pdf . Alles wat hiervoor of achter staat is niet noodzakelijk.
6. Plak de locatiecode op de plek waar nu /static/media/path/bestandsnaam.pdf staat. Zorg dat de code tussen de aanhalingstekens blijft staan.


Dit is een vrij geavanceerd proces. Ga niet zomaar rommelen aan de code. Wanneer je de locatiecode niet correct invoegt komt de volgende melding op de site te staan: 'Oeps, foutje. Hier hoort een document te staan'.


<strong>2.5 Headers</strong>

Op de HomePage and elke RichTextPage kunnen één of meerdere headers worden geplaatst. 

Een header image kan je wijzigen via Admin-pagina > Content > Pages 

Onderaan aan de pagina kan je bij 'Header Images' een afbeelding invoegen. 
Header Images > klik op het diagonale pijltje (linkericoon) de afbeelding aan die je als header wilt.
Let wel: Een header image dient 610 x 290 pixels als vereiste te hebben. Is dit niet het geval kan je de afbeelding niet invoeren.

Onder 'Header image type' kun je aangeven welk type header je wilt. 

'Parent header' --> de header die het hoogst in de hierarchie (HomePage) staat wordt hier weergegeven
'No header' -- > de header wordt niet afgebeeld op de pagina
'Single image' -- > de bovenste ingevoerde image wordt als header aangegeven
'Random image' --> indien je meerdere header images hebt, kun je deze laten rouleren

De Header image verwijderen --> klik op het kruisje (plaatje verdwijnt niet automatisch)

Klik op save om je wijzigen definitief te maken. 


<strong>2.6 Video's</strong>

Filmpjes uploaden via Youtube (maar ook via andere sites) is geen probleem. 

- Ga naar Youtube en zoek de betreffende video. 
- Klik onder de video op 'Delen/Share', daarna op 'Insluiten/Embed'.
- Kopieer de code (deze HTML code lijkt hierop: ```<iframe width="560" height="315" src="//www.youtube.com/embed/BcsfftwLUf0" frameborder="0" allowfullscreen></iframe>``` 
- Plaats in het tekstvak de cursor op de plek waar je de video wilt plaatsen en klik op het film-icoontje in de tekstverwerkersbalk. 
- Open in het nieuwe venster de 'Source' tab en kopieer de link in het zwarte veld. 
- Klik op 'Insert'

Wanneer je dit hebt gedaan zul je de video niet in het tekstvak zien, schrik hier niet van, dit hoort zo. Wil je toch zien waar de video staat in tekstvak kan je de gehele tekst selecteren (ctrl-a).
De video kan je na het invoegen nog verslepen in het tekstvak, dit doe je door op het de video te klikken en met de cursor te verslepen naar de gewenste plek. Wil je de video weer verwijderen uit het tekstvak dan kan je dat met delete of backspace doen. 

Als je klaar bent met het bewerken van de pagina, klik je op save. De veranderingen zullen dan zichtbaar zijn op de site. Wanneer je je veranderingen nog niet aan de buitenwereld wilt tonen kun je ervoor kiezen om bovenaan 'Draft' aan te vinken. De veranderingen zullen dan alleen zichtbaar zijn voor de admin. 

<strong>2.7 In-line editing</strong>

Een website kent een voorkant (front end) en een achterkant (back end). De 'front end' is datgene wat de bezoekers van een site zien. Deze User Manual dient als uitleg voor de 'back end' van de site. Het is de bedoeling dat je via de achterkant aanpassingen doet aan site. Wanneer je als admin bent ingelogd is het ook mogelijk om via de voorkant kleinere aanpassingen te doen (in-line editing) aan de de titel en een blog post. Login bij de admin-omgeving > ga terug naar de site. Je ziet linksboven een klein gele tab met een pijltje, klap deze uit en je ziet waar wijzigingen kan aanbrengen met 'Edit'. 

### 3 Formulier opstellen

Wil je een formulier opstellen, zodat leden zich voor een activiteit kunnen aanmelden, dan kan dat met de nieuwe backend. Overigens kan je met dit formulier geen betalingen invoeren of verwerken.

Ga naar: Content > Pages > Add Form > Change Form
- Title: Naam van het submenu
- Status: 'Published' is automatisch aangevinkt. Hierdoor zullen veranderingen aan de site na opslaan meteen zichtbaar op de site.  Wanneer je je veranderingen nog niet aan de buitenwereld wilt tonen kun je ervoor kiezen om bovenaan 'Draft' aan te vinken. De veranderingen zullen dan alleen zichtbaar zijn voor de admin. 
- Published from/Expires on: Hier kan je aangeven wanneer het formulier zichtbaar moet zijn op de website. Klik bij 'Published from' op 'today' en daarnaast bij 'Time' op 'now'. Als je wilt aangeven tot wanneer de content zichtbaar moet zijn op de site kan je een uiterste datum aangeven bij 'Expires on'. Dit is niet noodzakelijk.
- Content: hier zie je een tekstverwerker waar naar believen tekst, afbeeldingen en video invoeren. Zie 2.1 voor uitleg over de tekstverwerker.
 
- Button text: staat standaard op 'Submit', dit is de text van de button waarmee je het formulier verstuurd. 
- Response: Nadat het formulier is verstuurd, zullen gebruikers de content zien die je hier plaatst. 

Vervolgens kan je gebruiker een bevestigingsmail toesturen (optioneel), vul hiervoor de  benodigde velden in. 

Uiteindelijk kan je onderaan het formulier indelen via 'fields', dit kun je naar eigen inzicht doen. 

- Klik op 'Save' om de veranderingen door te voeren. 


##### Add Link

Via deze optie is het mogelijk om van een menu een link te maken naar een andere URL. 
Content > Pages > Add Link

### 4 Blogposts

Als AS heb je de mogelijkheid om blogs aan te maken, aan te passen en te verwijderen. 

<strong>Blog aanmaken</strong>

Een blog kan je aan maken door bij de admin-pagina naar Content > Blog posts te gaan.
Klik rechtsboven op 'Add blog posts' 
Vul vervolgens in:
- Title: Naam van het submenu
- Categories: Vink hier de categorie aan waar je Blog bij hoort>>
- Status: 'Published' is automatisch aangevinkt
- Indien je dit wilt kun je bij 'Published from/Expires on' de data aangeven wanneer de blog zichtbaar moet zijn op de site. Laat je 'Expires on' leeg, zal de blog niet verdwijnen van de hoofdsite. Besluit je 'Expires on' wel in te stellen, dan zal de blog na deze datum van de site verdwijnen. Als admin van de site kan je wel nog steeds de blog zien, deze zal niet aan de achterkant verdwijnen.
- Content: hier zie je een tekstverwerker waar naar believen tekst, afbeeldingen en video invoeren. Zie 2.1 voor uitleg over de tekstverwerker.

Onder de tab 'Other posts' is het mogelijk om links van gerelateerde berichten te plaatsen onder de blog. Dit is optioneel. 
Onder de tab 'Meta data' is het mogelijk om nog tags toe te voegen onder de blog. Tevens is het hier mogelijk om de URL en  beschrijving aan te passen.

'allow comments' is automatisch aangevinkt. Echter laat de JD-site het niet toe om comments onder een blog te plaatsen. Je kan er dus voor kiezen om 'allow comments' niet aan te vinken, dit kan je naar eigen inzicht bepalen. Als je besluit dit te doen zal in het overzicht van de blogs op de site de dode link naar '0 comments' verdwijnen. (deze functie zal verdwijnen) 
Tot slot, klik op 'Save'

<strong>Blog bewerken/verwijderen</strong>

Nadat een blog is ingevoerd kan je het als AS nog bewerken. Dit doe je door onder Content > Blog posts in het overzicht op de desbetreffende blog te klikken. Je komt nu weer in het specificatie venster wat je ook zag toen je de blog aanmaakte. Je kan hier veranderingen doorvoeren. Klik vervolgens wel op 'Save'. 

Een blog kan je verwijderen uit het overzicht door er een vinkje voor te zetten en in het drop-down-menu erboven (waar nu nog ------ staat) op 'delete selected Blog posts' te klikken. 

### 5 Events

Via de admin-pagina, onder Events > events, is het mogelijk om evenement aan te maken. 
Klik rechtsboven op 'Add event', vul vervolgens in:

- Title: Naam van het evenement
- Status: 'Published' is automatisch aangevinkt
- Published from/Expires on: Hier kan je aangeven wanneer het evenement zichtbaar moet zijn op de website. 
- Content: Tekst over het evenement
 
Onderaan staat 'Occurrences', hier vul je de datum, aanvangstijd (start time) en datum, sluitingstijd (end time) in. Datumnotatie is jjjj-mm-dd. Gebruik de kekke agenda- en klokicoontjes om datum en tijd in te voeren. Onder Description (optioneel) kan je een beschrijving geven van het evenement voor je eigen administratie. Deze beschrijving is niet zichtbaar op de frontend. 

### 6 Newsletters

Coming soon

### 7 Images and Documents

<strong>7.1 Media Library</strong>

Je kan verschillende bestanden (zoals documenten en afbeeldingen) opslaan bij de Media Library. Deze bestanden kan je uploaden onder Content > Media Library. Klik rechtsboven op de knop 'Upload', klik vervolgens op de knop 'Select'. Je kan meerdere bestanden in één keer selecteren en uploaden. 

Onder de tab help staat welke verschillende bestandsformaten je kan uploaden. Een bestand groter dan 10mb kan niet worden geüpload. Wel kan je meerdere bestanden die samen groter zijn dan 10mb uploaden.

Om een ellenlange lijst met bestanden te voorkomen kun je de Media Library naar eigen inzicht onderverdelen in mappen. Daarnaast kan je bestanden sorteren op alfabetische volgorde, grootte en datum. Tevens kan je bestanden filteren op datum en type. Met de zoekfunctie kan je door je de Media Library doorzoeken.

Gebruik de Media Library om documenten op te slaan die je op de site wilt plaatsen. Documenten die je voor intern gebruik nodig hebt kun je opslaan op de Wolk. 


<strong>7.2 Documenten toevoegen</strong>

Het is mogelijk om documenten (bv. HR, Statuten) zelf te plaatsen op de website.
Ga naar Content > Pages > Add Document Listing
Vul vervolgens in:
Title: Naam van het submenu
Status: 'Published' is automatisch aangevinkt
Content: Plaats hier de tekst van de pagina
Meta Data: Onder deze tab is het mogelijk om nog tags toe te voegen bij de Documenten. Tevens is het hier mogelijk om de URL en  beschrijving aan te passen.

Onderaan bij 'Documents' kun je documenten uploaden. Klik hiervoor op het icoontje onder 'Document'. Bestanden die nog niet in de Media Library staan kan je alsnog direct uploaden via de knop rechtsboven. Tekstbestanden die al in de Media Library staan kan je hier selecteren via 'Select' (het blauwe icoontje met pijltje, links vooraan). Op dit moment zie je nog geen verandering; het bestand is echter wél geüpload. Enkele vereiste is nog dat je een beschrijving van het bestand invult bij 'Description'. Deze beschrijving is uiteindelijk ook te zien op de site.

Wanneer je andere bestanden wilt uploaden, klik dan op 'Add another' wat helemaal onderaan staat.

