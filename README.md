# FlexiFiles - Profesionální správce souborů

Moderní a plně funkční správce soubo### 📁 Dostupné soubory

### Spustitelné soubory (.exe)
- **FlexiFiles.exe** - Nejnovější verze s všemi funkcemi (~36 MB) ⭐ **Doporučeno**
- **File Browser.exe** - Starší verze (~35 MB)
- **File Browser v2.exe** - Starší verze s informačním panelem (~36 MB)

### Vývojové soubory
- **file_browser.py** - Hlavní zdrojový kód
- **requirements.txt** - Python závislosti
- **FlexiFiles.spec** / **FlexiFiles v2.spec** - PyInstaller konfiguracený v Pythonu s využitím PyQt6 GUI frameworku, optimalizovaný pro operační systém Windows.

## ✨ Nové funkce - verze 2.0

### 📊 **Informační panel**
- **Detailní informace** - Zobrazuje podrobnosti o vybraných souborech a složkách
- **Náhledy obrázků** - Automatické náhledy pro běžné obrazové formáty (JPG, PNG, BMP, GIF, TIFF, ICO)
- **Statistiky složek** - Počet souborů, složek a celková velikost
- **Více vybraných položek** - Souhrnné informace při výběru více položek
- **Přepínání viditelnosti** - F1 nebo tlačítko v toolbaru

### 🎨 **Vylepšené uživatelské rozhraní**
- **Třípanelové rozložení** - Stromové zobrazení | Hlavní zobrazení | Informační panel
- **Škálovatelné panely** - Možnost přizpůsobení šířky jednotlivých panelů
- **Čisté formátování** - Elegantní zobrazení velikostí souborů (B, KB, MB, GB, TB)
- **Vizuální indikátory** - Progress bar pro výpočty velikostí složek

### 🔧 **Technická vylepšení**
- **Optimalizovaný výkon** - Efektivnější zpracování složek s mnoha soubory
- **Lepší error handling** - Robustnější zpracování chyb při přístupu k souborům
- **Vylepšená architektura** - Modulární design s odděleným informačním panelem

## Funkce

### 🎯 Hlavní vlastnosti
- **Moderní GUI** - Čisté a intuitivní uživatelské rozhraní s PyQt6
- **Tabované rozhraní** - Více záložek pro současnou práci s více adresáři
- **Tři režimy zobrazení** - Detaily (tabulka), Seznam, Velké ikony
- **Plná navigace** - Adresní řádek, tlačítka Zpět/Vpřed/Nahoru/Obnovit
- **Historie navigace** - Nezávislá historie pro každou záložku
- **Kontextová menu** - Pravé kliknutí pro rychlé akce
- **Stavový řádek** - Informace o vybraných položkách a velikosti

### 📁 Operace se soubory
- **Vytváření složek** - Rychlé vytvoření nových adresářů
- **Přejmenování** - Interaktivní přejmenování souborů a složek
- **Mazání** - Bezpečné mazání s potvrzovacím dialogem
- **Otevírání** - Spouštění souborů ve výchozích aplikacích
- **Kopírování cest** - Rychlé kopírování cest do schránky
- **Vlastnosti** - Zobrazení detailních informací o souborech

### 🔧 Technické vlastnosti
- **Výkonnost** - Optimalizováno pro velké adresáře
- **Thread-safe** - Bezpečné operace v multithreading prostředí
- **Správa paměti** - Efektivní využití paměti při procházení
- **Error handling** - Robustní zpracování chyb
- **Windows native** - Nativní vzhled a chování pro Windows

## Instalace

### Požadavky
- Python 3.7+
- PyQt6

### Instalace závislostí
```bash
pip install PyQt6
```

## Spuštění

### Možnost 1: Python skript
```bash
python file_browser.py
```

### Možnost 2: Batch soubor
```bash
start_flexifiles.bat
```

### Možnost 3: Executable soubor
Stáhněte si `FlexiFiles.exe` ze složky `dist/` a spusťte dvojklikem.

## Ovládání

### Klávesové zkratky
- **Ctrl+T**: Nová záložka
- **Ctrl+Shift+N**: Nová složka
- **F1**: Přepnout informační panel
- **Delete**: Smazat vybranou položku
- **F5**: Obnovit zobrazení
- **Enter**: Otevřít soubor/složku
- **Backspace**: Přejít do nadřazeného adresáře

### Mouse operace
- **Levé kliknutí**: Výběr položky
- **Dvojité kliknutí**: Otevření souboru/přechod do složky
- **Pravé kliknutí**: Kontextové menu
- **Kolečko myši**: Scrollování

## 📁 Dostupné soubory

### Spustitelné soubory (.exe)
- **File Browser.exe** - Původní verze (~35 MB)
- **File Browser v2.exe** - Verze s informačním panelem (~36 MB)

### Vývojové soubory
- **file_browser.py** - Hlavní zdrojový kód
- **requirements.txt** - Python závislosti
- **File Browser.spec** / **File Browser v2.spec** - PyInstaller konfigurace
- **Zpět/Vpřed**: Procházení historie navigace
- **Nahoru**: Přechod do nadřazeného adresáře
- **Obnovit**: Aktualizace zobrazení

### Operace se soubory
- **Dvojité kliknutí**: Otevření souboru nebo přechod do složky
- **Pravé kliknutí**: Kontextové menu s akcemi
- **Ctrl+Shift+N**: Vytvoření nové složky

### Kontextové menu
**Na soubor/složku:**
- Otevřít
- Spustit (jen soubory)
- Přejmenovat
- Smazat
- Zkopírovat cestu
- Vlastnosti

**Na prázdnou plochu:**
- Vytvořit novou složku
- Vložit (placeholder)
- Obnovit

## Struktura kódu

### Hlavní třídy
- `FileBrowserMainWindow` - Hlavní okno aplikace
- `NavigationHistory` - Správa historie navigace
- `FileOperations` - Operace se soubory a složkami

### Klíčové komponenty
- **QFileSystemModel** - Efektivní načítání souborového systému
- **QTreeView** - Stromové zobrazení adresářů
- **QTableView** - Tabulkové zobrazení s detaily
- **QLineEdit** - Adresní řádek pro navigaci
- **QStatusBar** - Zobrazení stavových informací

## Rozšíření

Aplikace je navržena modulárně a lze ji snadno rozšířit o:
- Vyhledávání souborů
- Kopírování/vyjímání/vkládání
- Drag & drop operace
- Náhledy souborů
- Bookmarks/oblíbené složky
- Více panelové zobrazení
- Integraci s cloud úložišti

## Licence

Tento projekt je open source a může být volně používán a modifikován.

## Autor

Vytvořeno s využitím GitHub Copilot pro demonstraci moderních Python GUI aplikací.
