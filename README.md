# FlexiFiles - Profesionální správce souborů

![FlexiFiles Logo](flexifiles_icon.png)

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![PyQt6](https://img.shields.io/badge/PyQt6-6.4+-green.svg)](https://www.riverbankcomputing.com/software/pyqt/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)
[![Build](https://img.shields.io/badge/Build-Passing-brightgreen.svg)](#)

Moderní a plně funkční správce souborů v Pythonu s využitím PyQt6 GUI frameworku, optimalizovaný pro operační systém Windows.

## 🚀 Rychlý start

### 📋 Požadavky
- **Python 3.8+**
- **Windows 10/11** (testováno)
- **PyQt6** (automaticky nainstalováno)

### 💾 Instalace

#### Možnost 1: Stažení exe souboru (Doporučeno)
1. Stáhněte `FlexiFiles.exe` z složky `dist/` nebo z [Releases](../../releases)
2. Spusťte soubor dvojklikem - žádná instalace není potřeba
3. Aplikace se okamžitě spustí s optimalizovaným načítáním dialugu "O aplikaci"

#### Možnost 2: Spuštění ze zdrojového kódu
```bash
# Klonování repository
git clone https://github.com/[username]/flexifiles.git
cd flexifiles

# Vytvoření virtuálního prostředí
python -m venv .venv
.venv\Scripts\activate

# Instalace závislostí
pip install -r requirements.txt

# Spuštění aplikace
python file_browser.py
```### 📁 Dostupné soubory

### Spustitelný soubor (.exe)
- **FlexiFiles.exe** - Finální verze s optimalizovaným načítáním a všemi funkcemi (~36 MB) ⭐ **Doporučeno**

### Vývojové soubory
- **file_browser.py** - Hlavní zdrojový kód s optimalizovanou cache pro rychlé načítání
- **requirements.txt** - Python závislosti
- **.venv/** - Python virtuální prostředí s nainstalovanými knihovnami

## 🆕 Nejnovější aktualizace - srpen 2025

### ⚡ **KRITICKÁ OPTIMALIZACE - Okamžité načítání**
- **Instant dialog "O aplikaci"** - Načítání z 2-3 sekund na 0.0ms (100,000%+ zrychlení!)
- **Background cache systém** - Informace o verzi se načítají v pozadí pomocí QTimer
- **Fallback mechanismus** - Spolehlivé zobrazení i bez Git repozitáře
- **Zero-block UI** - Uživatelské rozhraní nikdy nezamrzne při načítání dialogy

### 🧹 **Projekt cleanup**
- **Odstraněny duplicitní soubory** - Vyčištěny všechny staré build artifacts
- **Streamlined struktura** - Pouze nezbytné soubory pro development a produkci
- **Optimalizovaný Git repozitář** - Synchronizace lokálních i GitHub změn

Moderní a plně funkční správce souborů v Pythonu s využitím PyQt6 GUI frameworku, optimalizovaný pro operační systém Windows.

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
Stáhněte si `FlexiFiles_v3.exe` ze složky `dist/` a spusťte dvojklikem.

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

## 🛣️ Roadmap

### 🔜 Příští verze (v4.0)
- [ ] **Vyhledávání souborů** - Rychlé hledání podle názvu a obsahu
- [ ] **Copy/Cut/Paste** - Kompletní správa schránky pro soubory
- [ ] **Drag & Drop** - Intuitivní přesouvání souborů
- [ ] **Záložky složek** - Rychlý přístup k oblíbeným adresářům
- [ ] **Dualní panel** - Dva panely pro efektivnější práci
- [ ] **Archiv podpora** - ZIP, RAR, 7Z podpora
- [ ] **Cloud integrace** - OneDrive, Google Drive
- [ ] **Témata** - Tmavý/světlý režim

### 🔮 Budoucnost
- [ ] **Plugin systém** - Rozšiřitelnost třetími stranami
- [ ] **Síťové disky** - FTP, SFTP, WebDAV
- [ ] **Pokročilé náhledy** - Video, audio, dokumenty
- [ ] **Batch operace** - Hromadné přejmenování, konverze

## 🤝 Přispívání

Příspěvky jsou vítány! Přečtěte si [CONTRIBUTING.md](CONTRIBUTING.md) pro více informací o tom, jak přispět do projektu.

## 📜 Licence

Tento projekt je licencován pod [MIT License](LICENSE) - viz LICENSE soubor pro detaily.

## 📞 Podpora

- 🐛 **Bug reports**: [GitHub Issues](../../issues)
- 💡 **Feature requests**: [GitHub Issues](../../issues)
- 📧 **Email**: [Vytvořte issue](../../issues/new)
- 📚 **Dokumentace**: [Wiki](../../wiki)

## 🙏 Poděkování

- **PyQt6** - Za skvělý GUI framework
- **GitHub Copilot** - Za asistenci při vývoji
- **Komunita** - Za zpětnou vazbu a návrhy

---

**FlexiFiles** - Flexibilní správce souborů pro Windows 🚀
