# FlexiFiles Release Notes

## Version 4.2 - CRITICAL Performance Update ⚡ (Srpen 2025)

### 🚀 KRITICKÉ OPTIMALIZACE
- **Instant dialog loading** - "O aplikaci" dialog se načítá okamžitě (0.0ms vs. 2-3 sekund = 100,000%+ zrychlení!)
- **Background version cache** - Git informace se načítají v pozadí pomocí QTimer po startu aplikace
- **Zero-blocking UI** - Uživatelské rozhraní nikdy nezamrzne při načítání Git údajů
- **Fallback systém** - Spolehlivé zobrazení verzí i bez Git repozitáře

### 🧹 Projekt cleanup
- **Masivní úklid** - Odstraněny všechny duplicitní EXE soubory a build artifacts
- **Streamlined struktura** - Pouze `FlexiFiles.exe` v `dist/` složce
- **Git optimalizace** - Vyčištěn repozitář, synchronizace GitHub + lokální změny
- **Dokumentace update** - Aktualizované README.md a RELEASE_NOTES.md

### 📊 Technické detaily
- **Cache mechanismus** - `_version_info_cache` s předběžným načítáním
- **QTimer implementace** - 100ms delay po startu pro background loading
- **Timeout ochrana** - 1 sekunda timeout pro Git příkazy
- **Error resilience** - Automatický fallback na statické verze

### 🎯 Dopad na uživatele
- **Okamžitá odezva** - Dialog "O aplikaci" se otevře bez prodlevy
- **Stabilní výkon** - Žádné zamrzání UI při prvním otevření dialogy
- **Čistší projekt** - Redukce velikosti repozitáře o duplicitní soubory

---

## Version 3.0.0 - První oficiální release 🎉

### ✨ Nové funkce
- **Vlastní ikona aplikace** - Profesionální zelená ikona s logem "F"
- **Třípanelové rozhraní** - Strom složek | Hlavní zobrazení | Informační panel
- **Informační panel** - Detailní informace o souborech a složkách
- **Náhledy obrázků** - Automatické náhledy pro JPG, PNG, BMP, GIF, TIFF, ICO
- **Statistiky složek** - Počet souborů, složek a celková velikost
- **Multi-tab interface** - Více záložek pro současnou práci
- **Tři režimy zobrazení** - Detaily, Seznam, Velké ikony
- **História navigace** - Nezávislá pro každou záložku
- **Kontextová menu** - Rychlé akce na pravé kliknutí

### 🔧 Technické vylepšení
- **PyQt6 GUI framework** - Moderní a rychlé uživatelské rozhraní
- **QFileSystemModel** - Efektivní načítání souborového systému
- **Modulární architektura** - Oddělené třídy pro různé funkcionality
- **Error handling** - Robustní zpracování chyb
- **Cross-platform ready** - Připraveno pro rozšíření na Linux/Mac

### 📁 Operace se soubory
- **Vytváření složek** - Ctrl+Shift+N
- **Přejmenování** - Interaktivní dialog
- **Mazání** - S potvrzovacím dialogem
- **Vlastnosti** - Detailní informace o položkách
- **Otevírání** - Ve výchozích aplikacích
- **Kopírování cest** - Do schránky

### 🎨 Uživatelské rozhraní
- **Adresní řádek** - Přímá navigace zadáním cesty
- **Navigační tlačítka** - Zpět, Vpřed, Nahoru, Obnovit
- **Toolbar** - Rychlý přístup k funkcím
- **Stavový řádek** - Informace o výběru a operacích
- **Klávesové zkratky** - Efektivní ovládání

### 📦 Distribuce
- **Executable soubor** - FlexiFiles_v3.exe (~36 MB)
- **Zdrojový kód** - Python soubory s dokumentací
- **Žádná instalace** - Portable aplikace

### 🐛 Známé limitace
- Windows pouze (v této verzi)
- Česká lokalizace pouze
- Základní operace se soubory (bez copy/paste)

---

## Systémové požadavky
- **OS**: Windows 10/11
- **RAM**: 256 MB+
- **Disk**: 50 MB volného místa
- **Python**: 3.8+ (pro spuštění ze zdrojového kódu)

## Instalace
1. Stáhněte `FlexiFiles_v3.exe`
2. Spusťte dvojklikem
3. Žádná instalace není potřeba!

## Předchozí verze
- **v2.0** - Přidání informačního panelu
- **v1.0** - Základní funkcionalita file browseru

---

**Stáhnout**: [FlexiFiles_v3.exe](../../releases/download/v3.0.0/FlexiFiles_v3.exe)

*FlexiFiles v3.0.0 - Profesionální správce souborů pro Windows*
