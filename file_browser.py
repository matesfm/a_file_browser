"""
FlexiFiles - Profesionální správce souborů v Pythonu s PyQt6
============================================================

Tento soubor obsahuje kompletní implementaci moderního správce souborů
optimalizovaného pro Windows s využitím knihovny PyQt6.

Instalace potřebných knihoven:
pip install PyQt6

Pro spuštění aplikace:
python file_browser.py
"""

import sys
import os
import shutil
import subprocess
import os
import sys
import shutil
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional, List
from enum import Enum

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QTreeView, QTableView, QLineEdit, QPushButton, QSplitter,
    QStatusBar, QMenu, QMessageBox, QInputDialog, QHeaderView,
    QAbstractItemView, QToolBar, QFileDialog, QListView, QTabWidget, QStyleFactory,
    QLabel, QScrollArea, QFrame, QGridLayout, QProgressBar, QStyle
)
from PyQt6.QtCore import (
    Qt, QDir, QModelIndex, QTimer,
    pyqtSignal, QThread, QObject, QUrl, QSize
)
from PyQt6.QtGui import (
    QIcon, QDesktopServices, QClipboard, QAction,
    QKeySequence, QPixmap, QStandardItemModel, QFileSystemModel
)


class ViewMode(Enum):
    """Enum pro různé režimy zobrazení"""
    DETAILS = "details"      # Detailní tabulkové zobrazení
    LIST = "list"           # Jednoduchý seznam
    LARGE_ICONS = "icons"   # Velké ikony


class FileInfoPanel(QWidget):
    """Informační panel pro zobrazení detailů o vybraných souborech"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.file_model = None
        self.setup_ui()
    
    def setup_ui(self):
        """Vytvoří UI pro informační panel"""
        self.setMaximumWidth(300)
        self.setMinimumWidth(250)
        
        # Hlavní layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Nadpis panelu
        title = QLabel("Informace o souboru")
        title.setStyleSheet("font-weight: bold; font-size: 14px; color: #2c3e50;")
        layout.addWidget(title)
        
        # Scrollovací oblast pro obsah
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameStyle(QFrame.Shape.NoFrame)
        
        # Widget pro obsah
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(5)
        
        # Základní informace
        self.info_frame = QFrame()
        self.info_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        info_layout = QGridLayout(self.info_frame)
        info_layout.setContentsMargins(10, 10, 10, 10)
        info_layout.setSpacing(5)
        
        # Labels pro informace
        self.name_label = QLabel("Žádný soubor nevybrán")
        self.name_label.setWordWrap(True)
        self.name_label.setStyleSheet("font-weight: bold;")
        
        self.type_label = QLabel("")
        self.size_label = QLabel("")
        self.modified_label = QLabel("")
        self.created_label = QLabel("")
        self.path_label = QLabel("")
        self.path_label.setWordWrap(True)
        self.path_label.setStyleSheet("font-size: 10px; color: #7f8c8d;")
        
        # Přidání do grid layoutu
        info_layout.addWidget(QLabel("Název:"), 0, 0)
        info_layout.addWidget(self.name_label, 0, 1)
        info_layout.addWidget(QLabel("Typ:"), 1, 0)
        info_layout.addWidget(self.type_label, 1, 1)
        info_layout.addWidget(QLabel("Velikost:"), 2, 0)
        info_layout.addWidget(self.size_label, 2, 1)
        info_layout.addWidget(QLabel("Změněno:"), 3, 0)
        info_layout.addWidget(self.modified_label, 3, 1)
        info_layout.addWidget(QLabel("Vytvořeno:"), 4, 0)
        info_layout.addWidget(self.created_label, 4, 1)
        info_layout.addWidget(QLabel("Cesta:"), 5, 0, 1, 2)
        info_layout.addWidget(self.path_label, 6, 0, 1, 2)
        
        self.content_layout.addWidget(self.info_frame)
        
        # Statistiky složky (pouze pro složky)
        self.folder_stats_frame = QFrame()
        self.folder_stats_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        self.folder_stats_frame.hide()
        
        stats_layout = QVBoxLayout(self.folder_stats_frame)
        stats_layout.setContentsMargins(10, 10, 10, 10)
        
        stats_title = QLabel("Statistiky složky")
        stats_title.setStyleSheet("font-weight: bold; color: #2c3e50;")
        stats_layout.addWidget(stats_title)
        
        self.folder_items_label = QLabel("")
        self.folder_files_label = QLabel("")
        self.folder_folders_label = QLabel("")
        self.folder_size_label = QLabel("")
        
        stats_layout.addWidget(self.folder_items_label)
        stats_layout.addWidget(self.folder_files_label)
        stats_layout.addWidget(self.folder_folders_label)
        stats_layout.addWidget(self.folder_size_label)
        
        # Progress bar pro výpočet velikosti složky
        self.size_progress = QProgressBar()
        self.size_progress.setVisible(False)
        self.size_progress.setMaximum(0)  # Neurčitý progress
        stats_layout.addWidget(self.size_progress)
        
        self.content_layout.addWidget(self.folder_stats_frame)
        
        # Náhled (pro budoucí implementaci)
        self.preview_frame = QFrame()
        self.preview_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        self.preview_frame.hide()
        
        preview_layout = QVBoxLayout(self.preview_frame)
        preview_layout.setContentsMargins(10, 10, 10, 10)
        
        preview_title = QLabel("Náhled")
        preview_title.setStyleSheet("font-weight: bold; color: #2c3e50;")
        preview_layout.addWidget(preview_title)
        
        self.preview_label = QLabel("Náhled není k dispozici")
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setMinimumHeight(100)
        self.preview_label.setStyleSheet("border: 1px dashed #bdc3c7; color: #7f8c8d;")
        preview_layout.addWidget(self.preview_label)
        
        self.content_layout.addWidget(self.preview_frame)
        
        # Elastic space
        self.content_layout.addStretch()
        
        scroll_area.setWidget(self.content_widget)
        layout.addWidget(scroll_area)
    
    def set_file_model(self, model):
        """Nastaví file model pro získávání informací"""
        self.file_model = model
    
    def update_info(self, file_path: str):
        """Aktualizuje informace o souboru/složce"""
        if not file_path or not os.path.exists(file_path):
            self.clear_info()
            return
        
        try:
            # Základní informace
            file_name = os.path.basename(file_path)
            self.name_label.setText(file_name)
            self.path_label.setText(file_path)
            
            # Získání statistik souboru
            stat_info = os.stat(file_path)
            
            # Datum změny a vytvoření
            modified_time = datetime.fromtimestamp(stat_info.st_mtime)
            self.modified_label.setText(modified_time.strftime("%d.%m.%Y %H:%M:%S"))
            
            created_time = datetime.fromtimestamp(stat_info.st_ctime)
            self.created_label.setText(created_time.strftime("%d.%m.%Y %H:%M:%S"))
            
            if os.path.isfile(file_path):
                # Soubor
                self.type_label.setText("Soubor")
                size = stat_info.st_size
                self.size_label.setText(self.format_size(size))
                
                # Skryj statistiky složky
                self.folder_stats_frame.hide()
                
                # Zkus zobrazit náhled pro obrázky
                self.update_preview(file_path)
                
            elif os.path.isdir(file_path):
                # Složka
                self.type_label.setText("Složka")
                self.size_label.setText("Počítám...")
                
                # Zobraz statistiky složky
                self.update_folder_stats(file_path)
                self.folder_stats_frame.show()
                
                # Skryj náhled
                self.preview_frame.hide()
                
        except Exception as e:
            self.clear_info()
            self.name_label.setText(f"Chyba: {str(e)}")
    
    def update_folder_stats(self, folder_path: str):
        """Aktualizuje statistiky složky"""
        try:
            items = os.listdir(folder_path)
            total_items = len(items)
            
            files_count = 0
            folders_count = 0
            total_size = 0
            
            for item in items:
                item_path = os.path.join(folder_path, item)
                if os.path.isfile(item_path):
                    files_count += 1
                    try:
                        total_size += os.path.getsize(item_path)
                    except (OSError, PermissionError):
                        pass
                elif os.path.isdir(item_path):
                    folders_count += 1
            
            self.folder_items_label.setText(f"Celkem položek: {total_items}")
            self.folder_files_label.setText(f"Soubory: {files_count}")
            self.folder_folders_label.setText(f"Složky: {folders_count}")
            self.folder_size_label.setText(f"Velikost: {self.format_size(total_size)}")
            
        except PermissionError:
            self.folder_items_label.setText("Nedostatečná oprávnění")
            self.folder_files_label.setText("")
            self.folder_folders_label.setText("")
            self.folder_size_label.setText("")
        except Exception as e:
            self.folder_items_label.setText(f"Chyba: {str(e)}")
            self.folder_files_label.setText("")
            self.folder_folders_label.setText("")
            self.folder_size_label.setText("")
    
    def update_preview(self, file_path: str):
        """Aktualizuje náhled souboru"""
        # Získej příponu souboru
        _, ext = os.path.splitext(file_path.lower())
        
        # Seznam podporovaných obrazových formátů
        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.ico'}
        
        if ext in image_extensions:
            try:
                # Zkus načíst obrázek
                pixmap = QPixmap(file_path)
                if not pixmap.isNull():
                    # Změň velikost pro náhled
                    scaled_pixmap = pixmap.scaled(200, 150, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                    self.preview_label.setPixmap(scaled_pixmap)
                    self.preview_label.setText("")
                    self.preview_frame.show()
                    return
            except Exception:
                pass
        
        # Skryj náhled pro nepodporované formáty
        self.preview_frame.hide()
    
    def format_size(self, size: int) -> str:
        """Formátuje velikost souboru do čitelné podoby"""
        if size < 1024:
            return f"{size} B"
        elif size < 1024 * 1024:
            return f"{size / 1024:.1f} KB"
        elif size < 1024 * 1024 * 1024:
            return f"{size / (1024 * 1024):.1f} MB"
        elif size < 1024 * 1024 * 1024 * 1024:
            return f"{size / (1024 * 1024 * 1024):.1f} GB"
        else:
            return f"{size / (1024 * 1024 * 1024 * 1024):.1f} TB"
    
    def clear_info(self):
        """Vymaže všechny informace"""
        self.name_label.setText("Žádný soubor nevybrán")
        self.type_label.setText("")
        self.size_label.setText("")
        self.modified_label.setText("")
        self.created_label.setText("")
        self.path_label.setText("")
        self.folder_stats_frame.hide()
        self.preview_frame.hide()
    
    def update_selection(self, selected_paths: List[str]):
        """Aktualizuje panel na základě výběru více položek"""
        if not selected_paths:
            self.clear_info()
            return
        
        if len(selected_paths) == 1:
            # Jedna vybraná položka
            self.update_info(selected_paths[0])
        else:
            # Více vybraných položek
            self.show_multiple_selection_info(selected_paths)
    
    def show_multiple_selection_info(self, paths: List[str]):
        """Zobrazí informace o více vybraných položkách"""
        files_count = 0
        folders_count = 0
        total_size = 0
        
        for path in paths:
            if os.path.isfile(path):
                files_count += 1
                try:
                    total_size += os.path.getsize(path)
                except (OSError, PermissionError):
                    pass
            elif os.path.isdir(path):
                folders_count += 1
        
        self.name_label.setText(f"Vybráno {len(paths)} položek")
        self.type_label.setText("Více položek")
        self.size_label.setText(self.format_size(total_size))
        self.modified_label.setText("")
        self.created_label.setText("")
        self.path_label.setText(f"Soubory: {files_count}, Složky: {folders_count}")
        
        self.folder_stats_frame.hide()
        self.preview_frame.hide()


class NavigationHistory:
    """Třída pro správu historie navigace"""
    
    def __init__(self):
        self.history: List[str] = []
        self.current_index: int = -1
    
    def add_path(self, path: str) -> None:
        """Přidá cestu do historie"""
        # Odstraní všechny cesty za aktuální pozicí
        self.history = self.history[:self.current_index + 1]
        self.history.append(path)
        self.current_index = len(self.history) - 1
    
    def can_go_back(self) -> bool:
        """Kontroluje, zda je možné jít zpět"""
        return self.current_index > 0
    
    def can_go_forward(self) -> bool:
        """Kontroluje, zda je možné jít vpřed"""
        return self.current_index < len(self.history) - 1
    
    def go_back(self) -> Optional[str]:
        """Vrací předchozí cestu"""
        if self.can_go_back():
            self.current_index -= 1
            return self.history[self.current_index]
        return None
    
    def go_forward(self) -> Optional[str]:
        """Vrací následující cestu"""
        if self.can_go_forward():
            self.current_index += 1
            return self.history[self.current_index]
        return None


class FileOperations(QObject):
    """Třída pro operace se soubory a složkami"""
    
    operation_completed = pyqtSignal(str)  # Signál po dokončení operace
    operation_failed = pyqtSignal(str)     # Signál při chybě
    
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def create_folder(self, parent_path: str, folder_name: str) -> bool:
        """Vytvoří novou složku"""
        try:
            new_path = os.path.join(parent_path, folder_name)
            os.makedirs(new_path, exist_ok=False)
            self.operation_completed.emit(f"Složka '{folder_name}' byla vytvořena")
            return True
        except FileExistsError:
            self.operation_failed.emit(f"Složka '{folder_name}' již existuje")
        except Exception as e:
            self.operation_failed.emit(f"Chyba při vytváření složky: {str(e)}")
        return False
    
    def delete_item(self, path: str) -> bool:
        """Smaže soubor nebo složku"""
        try:
            if os.path.isfile(path):
                os.remove(path)
                self.operation_completed.emit(f"Soubor byl smazán")
            elif os.path.isdir(path):
                shutil.rmtree(path)
                self.operation_completed.emit(f"Složka byla smazána")
            return True
        except Exception as e:
            self.operation_failed.emit(f"Chyba při mazání: {str(e)}")
        return False
    
    def rename_item(self, old_path: str, new_name: str) -> bool:
        """Přejmenuje soubor nebo složku"""
        try:
            parent_dir = os.path.dirname(old_path)
            new_path = os.path.join(parent_dir, new_name)
            os.rename(old_path, new_path)
            self.operation_completed.emit(f"Položka byla přejmenována na '{new_name}'")
            return True
        except Exception as e:
            self.operation_failed.emit(f"Chyba při přejmenování: {str(e)}")
        return False


class FileBrowserMainWindow(QMainWindow):
    """Hlavní okno file browseru"""
    
    def __init__(self):
        super().__init__()
        self.current_path = QDir.homePath()
        self.navigation_history = NavigationHistory()
        self.file_operations = FileOperations(self)
        self.current_view_mode = ViewMode.DETAILS  # Výchozí režim zobrazení
        self.tab_data = {}  # Slovník pro ukládání dat záložek
        
        # Nastavení oken
        self.setWindowTitle("FlexiFiles - Profesionální správce souborů")
        self.setGeometry(100, 100, 1200, 800)
        
        # Nastavení ikony aplikace
        self.set_application_icon()
        
        # Vytvoření file system modelu
        self.file_model = QFileSystemModel()
        self.file_model.setRootPath(QDir.rootPath())
        
        # Vytvoření GUI komponent
        self.setup_ui()
        
        # Načtení výchozí cesty už se děje v create_new_tab
        # self.navigate_to_path(self.current_path)
    
    def get_version_info(self):
        """Získá informace o verzi z Git repozitáře"""
        try:
            # Získání počtu commitů
            result = subprocess.run(['git', 'rev-list', '--count', 'HEAD'], 
                                  capture_output=True, text=True, cwd=os.path.dirname(__file__))
            if result.returncode == 0:
                commit_count = int(result.stdout.strip())
                major = commit_count // 10  # Každých 10 commitů = nová major verze
                minor = commit_count % 10   # Zbytek = minor verze
                
                # Získání hash posledního commitu
                hash_result = subprocess.run(['git', 'rev-parse', '--short', 'HEAD'], 
                                           capture_output=True, text=True, cwd=os.path.dirname(__file__))
                git_hash = hash_result.stdout.strip() if hash_result.returncode == 0 else "unknown"
                
                # Získání data posledního commitu
                date_result = subprocess.run(['git', 'log', '-1', '--format=%cd', '--date=short'], 
                                           capture_output=True, text=True, cwd=os.path.dirname(__file__))
                commit_date = date_result.stdout.strip() if date_result.returncode == 0 else "unknown"
                
                # Kontrola, zda jsou nějaké změny
                status_result = subprocess.run(['git', 'status', '--porcelain'], 
                                             capture_output=True, text=True, cwd=os.path.dirname(__file__))
                has_changes = bool(status_result.stdout.strip()) if status_result.returncode == 0 else False
                
                version = f"{major}.{minor}"
                if has_changes:
                    version += "-dev"
                    
                return {
                    'version': version,
                    'git_hash': git_hash,
                    'commit_date': commit_date,
                    'commit_count': commit_count,
                    'has_changes': has_changes
                }
            else:
                return self.get_fallback_version()
                
        except Exception as e:
            print(f"Chyba při získávání Git informací: {e}")
            return self.get_fallback_version()
    
    def get_fallback_version(self):
        """Náhradní verze pokud Git není dostupný"""
        return {
            'version': '4.1-standalone',
            'git_hash': 'unknown',
            'commit_date': 'unknown',
            'commit_count': 0,
            'has_changes': False
        }
    
    def set_application_icon(self):
        """Nastaví ikonu aplikace"""
        try:
            # Cesta k vlastní ikoně (pokud existuje)
            icon_paths = [
                os.path.join(os.path.dirname(__file__), 'flexifiles_icon.png'),
                os.path.join(os.path.dirname(__file__), 'flexifiles_icon.ico')
            ]
            
            app_icon = None
            for icon_path in icon_paths:
                if os.path.exists(icon_path):
                    app_icon = QIcon(icon_path)
                    break
            
            if app_icon is None:
                # Použít standardní ikonu složky jako náhradní řešení
                app_icon = self.style().standardIcon(QStyle.StandardPixmap.SP_DirIcon)
            
            # Nastavit ikonu pro okno
            self.setWindowIcon(app_icon)
            
        except Exception as e:
            print(f"Nepodařilo se nastavit ikonu aplikace: {e}")
    
    def setup_ui(self):
        """Vytvoří uživatelské rozhraní"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Hlavní layout
        main_layout = QVBoxLayout(central_widget)
        
        # Menu bar
        self.create_menu_bar()
        
        # Toolbar s navigačními tlačítky
        self.create_toolbar()
        
        # Navigační panel s adresním řádkem
        nav_layout = QHBoxLayout()
        
        # Navigační tlačítka
        self.back_button = QPushButton("◀ Zpět")
        self.back_button.setEnabled(False)
        self.forward_button = QPushButton("Vpřed ▶")
        self.forward_button.setEnabled(False)
        self.up_button = QPushButton("↑ Nahoru")
        self.refresh_button = QPushButton("🔄 Obnovit")
        
        # Adresní řádek
        self.address_bar = QLineEdit()
        self.address_bar.setPlaceholderText("Zadejte cestu...")
        
        nav_layout.addWidget(self.back_button)
        nav_layout.addWidget(self.forward_button)
        nav_layout.addWidget(self.up_button)
        nav_layout.addWidget(self.refresh_button)
        nav_layout.addWidget(self.address_bar)
        
        main_layout.addLayout(nav_layout)
        
        # Tab widget pro záložky
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.currentChanged.connect(self.tab_changed)
        
        # Vytvoření první záložky
        self.create_new_tab(QDir.homePath(), "Domů")
        
        main_layout.addWidget(self.tab_widget)
        
        # Propojení signálů pro navigační tlačítka
        self.back_button.clicked.connect(self.go_back)
        self.forward_button.clicked.connect(self.go_forward)
        self.up_button.clicked.connect(self.go_up)
        self.refresh_button.clicked.connect(self.refresh_current_view)
        self.address_bar.returnPressed.connect(self.navigate_from_address_bar)
        
        # Propojení file operations
        self.file_operations.operation_completed.connect(self.show_status_message)
        self.file_operations.operation_failed.connect(self.show_error_message)
        
        # Stavový řádek
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Připraven")
        
    def create_new_tab(self, path: str, title: Optional[str] = None) -> int:
        """Vytvoří novou záložku s file browserem"""
        if not title:
            title = os.path.basename(path) or path
        
        # Widget pro záložku
        tab_widget = QWidget()
        tab_layout = QVBoxLayout(tab_widget)
        tab_layout.setContentsMargins(0, 0, 0, 0)
        
        # Splitter pro rozdělení zobrazení
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Stromové zobrazení (levý panel)
        tree_view = QTreeView()
        tree_view.setHeaderHidden(True)
        tree_view.setMaximumWidth(300)
        
        # Střední panel s file view
        middle_widget = QWidget()
        middle_layout = QVBoxLayout(middle_widget)
        middle_layout.setContentsMargins(0, 0, 0, 0)
        
        # Tabulkové zobrazení s upravenými řádky
        table_view = QTableView()
        table_view.setSortingEnabled(True)
        table_view.setAlternatingRowColors(True)
        table_view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        
        # Úprava tloušťky řádků
        table_view.verticalHeader().setDefaultSectionSize(20)  # Tenčí řádky
        table_view.verticalHeader().setMinimumSectionSize(18)
        table_view.setShowGrid(False)  # Skrytí mřížky pro čistší vzhled
        
        # Seznamové zobrazení
        list_view = QListView()
        list_view.setViewMode(QListView.ViewMode.ListMode)
        list_view.setResizeMode(QListView.ResizeMode.Adjust)
        list_view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        
        # Ikonové zobrazení
        icon_view = QListView()
        icon_view.setViewMode(QListView.ViewMode.IconMode)
        icon_view.setResizeMode(QListView.ResizeMode.Adjust)
        icon_view.setGridSize(QSize(100, 100))
        icon_view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        
        # Kontejner pro různé režimy zobrazení
        view_container = QWidget()
        view_layout = QVBoxLayout(view_container)
        view_layout.setContentsMargins(0, 0, 0, 0)
        
        # Přidám pouze table_view na začátku
        view_layout.addWidget(table_view)
        list_view.hide()
        icon_view.hide()
        
        middle_layout.addWidget(view_container)
        
        # Informační panel (pravý panel)
        info_panel = FileInfoPanel()
        info_panel.set_file_model(self.file_model)
        
        splitter.addWidget(tree_view)
        splitter.addWidget(middle_widget)
        splitter.addWidget(info_panel)
        splitter.setStretchFactor(0, 0)  # Pevná šířka pro tree view
        splitter.setStretchFactor(1, 1)  # Rozšiřitelná šířka pro view
        splitter.setStretchFactor(2, 0)  # Pevná šířka pro info panel
        
        tab_layout.addWidget(splitter)
        
        # Přidání záložky
        tab_index = self.tab_widget.addTab(tab_widget, title)
        
        # Uložení referencí na view komponenty pro tuto záložku
        tab_data = {
            'path': path,
            'tree_view': tree_view,
            'table_view': table_view,
            'list_view': list_view,
            'icon_view': icon_view,
            'view_container': view_container,
            'view_layout': view_layout,
            'current_view_mode': ViewMode.DETAILS,
            'splitter': splitter,
            'navigation_history': NavigationHistory(),  # Každá záložka má svou historii
            'info_panel': info_panel,  # Informační panel
            'middle_widget': middle_widget
        }
        
        # Nastavení modelu pro tuto záložku
        tree_view.setModel(self.file_model)
        for i in range(1, self.file_model.columnCount()):
            tree_view.hideColumn(i)
        
        table_view.setModel(self.file_model)
        list_view.setModel(self.file_model)
        icon_view.setModel(self.file_model)
        
        # Nastavení hlaviček tabulky
        header = table_view.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        
        # Propojení signálů
        tree_view.clicked.connect(lambda index, tab_idx=tab_index: self.tree_item_clicked(index, tab_idx))
        table_view.doubleClicked.connect(lambda index, tab_idx=tab_index: self.table_item_double_clicked(index, tab_idx))
        list_view.doubleClicked.connect(lambda index, tab_idx=tab_index: self.table_item_double_clicked(index, tab_idx))
        icon_view.doubleClicked.connect(lambda index, tab_idx=tab_index: self.table_item_double_clicked(index, tab_idx))
        
        # Signály pro aktualizaci informačního panelu při výběru
        table_view.clicked.connect(lambda index, tab_idx=tab_index: self.update_info_panel(index, tab_idx))
        list_view.clicked.connect(lambda index, tab_idx=tab_index: self.update_info_panel(index, tab_idx))
        icon_view.clicked.connect(lambda index, tab_idx=tab_index: self.update_info_panel(index, tab_idx))
        
        # Signály pro výběr více položek
        table_view.selectionModel().selectionChanged.connect(lambda selected, deselected, tab_idx=tab_index: self.update_info_panel_selection(tab_idx))
        list_view.selectionModel().selectionChanged.connect(lambda selected, deselected, tab_idx=tab_index: self.update_info_panel_selection(tab_idx))
        icon_view.selectionModel().selectionChanged.connect(lambda selected, deselected, tab_idx=tab_index: self.update_info_panel_selection(tab_idx))
        
        # Kontextová menu
        table_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        table_view.customContextMenuRequested.connect(lambda pos, tab_idx=tab_index: self.show_context_menu(pos, tab_idx))
        list_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        list_view.customContextMenuRequested.connect(lambda pos, tab_idx=tab_index: self.show_context_menu(pos, tab_idx))
        icon_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        icon_view.customContextMenuRequested.connect(lambda pos, tab_idx=tab_index: self.show_context_menu(pos, tab_idx))
        tree_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        tree_view.customContextMenuRequested.connect(lambda pos, tab_idx=tab_index: self.show_tree_context_menu(pos, tab_idx))
        
        # Uložení dat záložky
        self.tab_data[tab_index] = tab_data
        
        # Nastavení aktuální záložky
        self.tab_widget.setCurrentIndex(tab_index)
        
        # Navigace na cestu
        self.navigate_to_path_in_tab(path, tab_index)
        
        return tab_index
    
    def close_tab(self, index: int):
        """Zavře záložku"""
        if self.tab_widget.count() > 1:  # Nechá alespoň jednu záložku
            # Odstraň data záložky
            if index in self.tab_data:
                del self.tab_data[index]
            # Přenumeruj zbývající záložky
            new_tab_data = {}
            for i, data in self.tab_data.items():
                if i > index:
                    new_tab_data[i-1] = data
                elif i < index:
                    new_tab_data[i] = data
            self.tab_data = new_tab_data
            self.tab_widget.removeTab(index)
        
    def tab_changed(self, index: int):
        """Zpracuje změnu aktivní záložky"""
        if index >= 0:
            tab_data = self.get_current_tab_data()
            if tab_data:
                self.current_path = tab_data['path']
                self.address_bar.setText(self.current_path)
                self.update_navigation_buttons()
    
    def get_current_tab_data(self):
        """Vrací data aktuální záložky"""
        current_index = self.tab_widget.currentIndex()
        if current_index >= 0 and current_index in self.tab_data:
            return self.tab_data[current_index]
        return None
    
    def create_new_tab_current_path(self):
        """Vytvoří novou záložku s aktuální cestou"""
        self.create_new_tab(self.current_path)
    
    def navigate_to_path_in_tab(self, path: str, tab_index: int):
        """Naviguje na cestu v konkrétní záložce"""
        if tab_index not in self.tab_data or not os.path.exists(path) or not os.path.isdir(path):
            return
            
        tab_data = self.tab_data[tab_index]
        
        # Přidej cestu do historie této záložky
        tab_data['navigation_history'].add_path(path)
        tab_data['path'] = path
        
        # Aktualizace zobrazení v záložce
        index = self.file_model.index(path)
        tab_data['tree_view'].setCurrentIndex(index)
        tab_data['tree_view'].scrollTo(index)
        
        # Nastavení root indexu pro aktuální zobrazení v záložce
        current_view = self.get_current_view_for_tab(tab_data)
        current_view.setRootIndex(index)
        
        # Aktualizace UI pouze pokud je to aktuální záložka
        if tab_index == self.tab_widget.currentIndex():
            self.current_path = path
            self.address_bar.setText(path)
            self.update_navigation_buttons()
        
        # Aktualizace názvu záložky
        folder_name = os.path.basename(path) or path
        self.tab_widget.setTabText(tab_index, folder_name)
    
    def _navigate_to_path_in_tab_without_history(self, path: str, tab_index: int):
        """Naviguje na cestu v konkrétní záložce bez přidání do historie (pro zpět/vpřed)"""
        if tab_index not in self.tab_data or not os.path.exists(path) or not os.path.isdir(path):
            return
            
        tab_data = self.tab_data[tab_index]
        tab_data['path'] = path
        
        # Aktualizace zobrazení v záložce
        index = self.file_model.index(path)
        tab_data['tree_view'].setCurrentIndex(index)
        tab_data['tree_view'].scrollTo(index)
        
        # Nastavení root indexu pro aktuální zobrazení v záložce
        current_view = self.get_current_view_for_tab(tab_data)
        current_view.setRootIndex(index)
        
        # Aktualizace UI pouze pokud je to aktuální záložka
        if tab_index == self.tab_widget.currentIndex():
            self.current_path = path
            self.address_bar.setText(path)
            self.update_navigation_buttons()
        
        # Aktualizace názvu záložky
        folder_name = os.path.basename(path) or path
        self.tab_widget.setTabText(tab_index, folder_name)
    
    def get_current_view_for_tab(self, tab_data):
        """Vrací aktuální aktivní zobrazení pro záložku"""
        if tab_data['current_view_mode'] == ViewMode.DETAILS:
            return tab_data['table_view']
        elif tab_data['current_view_mode'] == ViewMode.LIST:
            return tab_data['list_view']
        else:
            return tab_data['icon_view']
    
    def create_menu_bar(self):
        """Vytvoří menu bar s nápovědou"""
        menubar = self.menuBar()
        
        # Menu Nápověda
        help_menu = menubar.addMenu('&Nápověda')
        
        # Akce Nápověda
        help_action = QAction('&Nápověda', self)
        help_action.setShortcut(QKeySequence('F1'))
        help_action.setStatusTip('Zobrazí nápovědu k aplikaci')
        help_action.triggered.connect(self.show_help)
        help_menu.addAction(help_action)
        
        help_menu.addSeparator()
        
        # Akce O aplikaci
        about_action = QAction('&O aplikaci', self)
        about_action.setStatusTip('Informace o aplikaci FlexiFiles')
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def create_toolbar(self):
        """Vytvoří toolbar s akcemi"""
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        
        # Akce pro novou složku
        new_folder_action = QAction("📁 Nová složka", self)
        new_folder_action.setShortcut(QKeySequence("Ctrl+Shift+N"))
        new_folder_action.triggered.connect(self.create_new_folder)
        toolbar.addAction(new_folder_action)
        
        # Akce pro novou záložku
        new_tab_action = QAction("🔖 Nová záložka", self)
        new_tab_action.setShortcut(QKeySequence("Ctrl+T"))
        new_tab_action.triggered.connect(self.create_new_tab_current_path)
        toolbar.addAction(new_tab_action)
        
        toolbar.addSeparator()
        
        # Přepínání zobrazení
        view_action = QAction("🔄 Přepnout zobrazení", self)
        view_action.triggered.connect(self.toggle_view_mode)
        toolbar.addAction(view_action)
        
        # Přepínání informačního panelu
        info_panel_action = QAction("ℹ️ Informační panel", self)
        info_panel_action.setShortcut(QKeySequence("Ctrl+I"))
        info_panel_action.triggered.connect(self.toggle_info_panel)
        toolbar.addAction(info_panel_action)
    
    def navigate_to_path(self, path: str):
        """Naviguje na zadanou cestu v aktuální záložce"""
        current_tab = self.tab_widget.currentIndex()
        self.navigate_to_path_in_tab(path, current_tab)
    
    def update_navigation_buttons(self):
        """Aktualizuje stav navigačních tlačítek"""
        tab_data = self.get_current_tab_data()
        if tab_data:
            nav_history = tab_data['navigation_history']
            self.back_button.setEnabled(nav_history.can_go_back())
            self.forward_button.setEnabled(nav_history.can_go_forward())
            self.up_button.setEnabled(os.path.dirname(self.current_path) != self.current_path)
        else:
            self.back_button.setEnabled(False)
            self.forward_button.setEnabled(False)
            self.up_button.setEnabled(False)
    
    def go_back(self):
        """Jde na předchozí cestu v historii aktuální záložky"""
        tab_data = self.get_current_tab_data()
        if not tab_data:
            return
            
        nav_history = tab_data['navigation_history']
        path = nav_history.go_back()
        if path:
            current_tab = self.tab_widget.currentIndex()
            # Navigace bez přidání do historie (protože už tam je)
            self._navigate_to_path_in_tab_without_history(path, current_tab)
    
    def go_forward(self):
        """Jde na následující cestu v historii aktuální záložky"""
        tab_data = self.get_current_tab_data()
        if not tab_data:
            return
            
        nav_history = tab_data['navigation_history']
        path = nav_history.go_forward()
        if path:
            current_tab = self.tab_widget.currentIndex()
            # Navigace bez přidání do historie (protože už tam je)
            self._navigate_to_path_in_tab_without_history(path, current_tab)
    
    def go_up(self):
        """Jde do nadřazeného adresáře"""
        parent_path = os.path.dirname(self.current_path)
        if parent_path != self.current_path:
            self.navigate_to_path(parent_path)
    
    def refresh_current_view(self):
        """Obnoví aktuální zobrazení"""
        tab_data = self.get_current_tab_data()
        if tab_data:
            path = tab_data['path']
            index = self.file_model.index(path)
            current_view = self.get_current_view_for_tab(tab_data)
            if current_view:
                current_view.setRootIndex(index)
            tab_data['tree_view'].setCurrentIndex(index)
            self.status_bar.showMessage("Zobrazení obnoveno", 2000)
    
    def navigate_from_address_bar(self):
        """Naviguje na cestu z adresního řádku"""
        path = self.address_bar.text().strip()
        if path:
            self.navigate_to_path(path)
        else:
            self.address_bar.setText(self.current_path)
    
    def tree_item_clicked(self, index: QModelIndex, tab_index: Optional[int] = None):
        """Zpracuje kliknutí na položku ve stromovém zobrazení"""
        path = self.file_model.filePath(index)
        if os.path.isdir(path):
            if tab_index is not None:
                self.navigate_to_path_in_tab(path, tab_index)
            else:
                # Fallback pro případ, kdy není specifikovaný tab_index
                current_tab = self.tab_widget.currentIndex()
                self.navigate_to_path_in_tab(path, current_tab)
    
    def table_item_double_clicked(self, index: QModelIndex, tab_index: Optional[int] = None):
        """Zpracuje dvojité kliknutí na položku v tabulce"""
        path = self.file_model.filePath(index)
        
        if os.path.isdir(path):
            # Navigace do složky
            if tab_index is not None:
                self.navigate_to_path_in_tab(path, tab_index)
            else:
                current_tab = self.tab_widget.currentIndex()
                self.navigate_to_path_in_tab(path, current_tab)
        elif os.path.isfile(path):
            # Otevření souboru
            self.open_file(path)
    
    def open_file(self, file_path: str):
        """Otevře soubor ve výchozí aplikaci"""
        try:
            if sys.platform.startswith('win'):
                os.startfile(file_path)
            else:
                QDesktopServices.openUrl(QUrl.fromLocalFile(file_path))
            self.status_bar.showMessage(f"Otevírám: {os.path.basename(file_path)}", 2000)
        except Exception as e:
            self.show_error_message(f"Nepodařilo se otevřít soubor: {str(e)}")
    
    def show_context_menu(self, position, tab_index: Optional[int] = None):
        """Zobrazí kontextové menu pro aktuální view"""
        if tab_index is None:
            tab_index = self.tab_widget.currentIndex()
            
        tab_data = self.tab_data.get(tab_index)
        if not tab_data:
            return
            
        # Určí, které view poslalo signál
        sender = self.sender()
        current_view = None
        
        if sender == tab_data['table_view']:
            current_view = tab_data['table_view']
        elif sender == tab_data['list_view']:
            current_view = tab_data['list_view']
        elif sender == tab_data['icon_view']:
            current_view = tab_data['icon_view']
        
        if not current_view:
            return
            
        index = current_view.indexAt(position)
        menu = QMenu()
        if index.isValid():
            # Menu pro vybranou položku
            file_path = self.file_model.filePath(index)
            file_name = os.path.basename(file_path)
            
            open_action = menu.addAction(f"🔓 Otevřít '{file_name}'")
            open_action.triggered.connect(lambda: self.open_file(file_path))
            
            if os.path.isfile(file_path):
                run_action = menu.addAction(f"▶️ Spustit '{file_name}'")
                run_action.triggered.connect(lambda: self.run_file(file_path))
            
            menu.addSeparator()
            
            rename_action = menu.addAction(f"✏️ Přejmenovat '{file_name}'")
            rename_action.triggered.connect(lambda: self.rename_item(file_path))
            
            delete_action = menu.addAction(f"🗑️ Smazat '{file_name}'")
            delete_action.triggered.connect(lambda: self.delete_item(file_path))
            
            menu.addSeparator()
            
            copy_path_action = menu.addAction("📋 Zkopírovat cestu")
            copy_path_action.triggered.connect(lambda: self.copy_path_to_clipboard(file_path))
            
            properties_action = menu.addAction(f"ℹ️ Vlastnosti '{file_name}'")
            properties_action.triggered.connect(lambda: self.show_properties(file_path))
        else:
            # Menu pro prázdnou plochu
            new_folder_action = menu.addAction("📁 Vytvořit novou složku")
            new_folder_action.triggered.connect(self.create_new_folder)
            
            menu.addSeparator()
            
            paste_action = menu.addAction("📄 Vložit")
            paste_action.setEnabled(False)  # Funkce vložení není implementována
            
            refresh_action = menu.addAction("🔄 Obnovit")
            refresh_action.triggered.connect(self.refresh_current_view)
        
        menu.exec(current_view.mapToGlobal(position))
    
    def show_tree_context_menu(self, position, tab_index: Optional[int] = None):
        """Zobrazí kontextové menu pro tree view"""
        if tab_index is None:
            tab_index = self.tab_widget.currentIndex()
            
        tab_data = self.tab_data.get(tab_index)
        if not tab_data:
            return
            
        tree_view = tab_data['tree_view']
        index = tree_view.indexAt(position)
        if index.isValid():
            menu = QMenu()
            file_path = self.file_model.filePath(index)
            file_name = os.path.basename(file_path)
            
            navigate_action = menu.addAction(f"📂 Přejít do '{file_name}'")
            navigate_action.triggered.connect(lambda: self.navigate_to_path_in_tab(file_path, tab_index))
            
            menu.exec(tree_view.mapToGlobal(position))
    
    def create_new_folder(self):
        """Vytvoří novou složku v aktuálním adresáři"""
        tab_data = self.get_current_tab_data()
        if not tab_data:
            return
            
        current_path = tab_data['path']
        folder_name, ok = QInputDialog.getText(
            self, "Nová složka", "Zadejte název složky:"
        )
        
        if ok and folder_name.strip():
            self.file_operations.create_folder(current_path, folder_name.strip())
    
    def rename_item(self, file_path: str):
        """Přejmenuje vybranou položku"""
        old_name = os.path.basename(file_path)
        new_name, ok = QInputDialog.getText(
            self, "Přejmenovat", f"Nový název pro '{old_name}':", text=old_name
        )
        
        if ok and new_name.strip() and new_name != old_name:
            self.file_operations.rename_item(file_path, new_name.strip())
    
    def delete_item(self, file_path: str):
        """Smaže vybranou položku s potvrzením"""
        file_name = os.path.basename(file_path)
        item_type = "složku" if os.path.isdir(file_path) else "soubor"
        
        reply = QMessageBox.question(
            self, "Potvrdit smazání",
            f"Opravdu chcete smazat {item_type} '{file_name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.file_operations.delete_item(file_path)
    
    def run_file(self, file_path: str):
        """Spustí spustitelný soubor"""
        try:
            if sys.platform.startswith('win'):
                subprocess.Popen(file_path, shell=True)
            else:
                subprocess.Popen([file_path])
            self.status_bar.showMessage(f"Spouštím: {os.path.basename(file_path)}", 2000)
        except Exception as e:
            self.show_error_message(f"Nepodařilo se spustit soubor: {str(e)}")
    
    def copy_path_to_clipboard(self, file_path: str):
        """Zkopíruje cestu do schránky"""
        clipboard = QApplication.clipboard()
        if clipboard:
            clipboard.setText(file_path)
            self.status_bar.showMessage("Cesta zkopírována do schránky", 2000)
    
    def show_properties(self, file_path: str):
        """Zobrazí vlastnosti souboru/složky"""
        try:
            stat = os.stat(file_path)
            size = stat.st_size
            modified = datetime.fromtimestamp(stat.st_mtime).strftime("%d.%m.%Y %H:%M:%S")
            
            if os.path.isdir(file_path):
                # Počet položek ve složce
                try:
                    items_count = len(os.listdir(file_path))
                    size_text = f"{items_count} položek"
                except PermissionError:
                    size_text = "Nedostupné (oprávnění)"
            else:
                # Velikost souboru
                if size < 1024:
                    size_text = f"{size} B"
                elif size < 1024 * 1024:
                    size_text = f"{size / 1024:.1f} KB"
                elif size < 1024 * 1024 * 1024:
                    size_text = f"{size / (1024 * 1024):.1f} MB"
                else:
                    size_text = f"{size / (1024 * 1024 * 1024):.1f} GB"
            
            properties_text = f"""Název: {os.path.basename(file_path)}
Cesta: {file_path}
Typ: {"Složka" if os.path.isdir(file_path) else "Soubor"}
Velikost: {size_text}
Změněno: {modified}"""
            
            QMessageBox.information(self, "Vlastnosti", properties_text)
            
        except Exception as e:
            self.show_error_message(f"Nepodařilo se načíst vlastnosti: {str(e)}")
    
    def update_status_bar(self):
        """Aktualizuje stavový řádek"""
        try:
            # Získej data aktuální záložky
            tab_data = self.get_current_tab_data()
            if not tab_data:
                self.status_bar.showMessage("Připraven")
                return
                
            # Počet vybraných položek z aktuálního zobrazení
            current_view = self.get_current_view_for_tab(tab_data)
            if not current_view:
                self.status_bar.showMessage("Připraven")
                return
                
            selection_model = current_view.selectionModel()
            if not selection_model:
                self.status_bar.showMessage("Připraven")
                return
                
            selection = selection_model.selectedRows()
            selected_count = len(selection)
            
            if selected_count > 0:
                # Výpočet celkové velikosti vybraných položek
                total_size = 0
                for index in selection:
                    file_path = self.file_model.filePath(index)
                    if os.path.isfile(file_path):
                        total_size += os.path.getsize(file_path)
                
                if total_size > 0:
                    if total_size < 1024:
                        size_text = f"{total_size} B"
                    elif total_size < 1024 * 1024:
                        size_text = f"{total_size / 1024:.1f} KB"
                    elif total_size < 1024 * 1024 * 1024:
                        size_text = f"{total_size / (1024 * 1024):.1f} MB"
                    else:
                        size_text = f"{total_size / (1024 * 1024 * 1024):.1f} GB"
                    
                    message = f"Vybráno: {selected_count} položek ({size_text})"
                else:
                    message = f"Vybráno: {selected_count} položek"
            else:
                # Počet všech položek v aktuálním adresáři
                try:
                    current_path = tab_data['path']
                    items_count = len(os.listdir(current_path))
                    message = f"Položek celkem: {items_count}"
                except PermissionError:
                    message = "Nedostatečná oprávnění"
                except Exception:
                    message = "Připraven"
            
            self.status_bar.showMessage(message)
            
        except Exception:
            self.status_bar.showMessage("Připraven")
    
    def toggle_view_mode(self):
        """Přepne mezi různými režimy zobrazení pro aktuální záložku"""
        tab_data = self.get_current_tab_data()
        if not tab_data:
            return
            
        current_mode = tab_data['current_view_mode']
        
        # Cyklické přepínání mezi režimy
        if current_mode == ViewMode.DETAILS:
            self.set_view_mode_for_tab(ViewMode.LIST)
        elif current_mode == ViewMode.LIST:
            self.set_view_mode_for_tab(ViewMode.LARGE_ICONS)
        else:
            self.set_view_mode_for_tab(ViewMode.DETAILS)
    
    def set_view_mode_for_tab(self, mode: ViewMode, tab_index: Optional[int] = None):
        """Nastaví konkrétní režim zobrazení pro záložku"""
        if tab_index is None:
            tab_index = self.tab_widget.currentIndex()
            
        tab_data = self.tab_data.get(tab_index)
        if not tab_data or mode == tab_data['current_view_mode']:
            return
        
        # Skryj všechna zobrazení
        tab_data['table_view'].hide()
        tab_data['list_view'].hide()
        tab_data['icon_view'].hide()
        
        # Odstraň všechna zobrazení z layoutu
        view_layout = tab_data['view_layout']
        for i in reversed(range(view_layout.count())):
            item = view_layout.itemAt(i)
            if item and item.widget():
                item.widget().setParent(None)
        
        # Získej aktuální root index
        current_view = self.get_current_view_for_tab(tab_data)
        current_index = current_view.rootIndex() if current_view else None
        
        # Nastav nový režim
        tab_data['current_view_mode'] = mode
        
        if mode == ViewMode.DETAILS:
            view_layout.addWidget(tab_data['table_view'])
            tab_data['table_view'].show()
            if current_index and current_index.isValid():
                tab_data['table_view'].setRootIndex(current_index)
            self.status_bar.showMessage("Režim zobrazení: Podrobnosti", 2000)
            
        elif mode == ViewMode.LIST:
            view_layout.addWidget(tab_data['list_view'])
            tab_data['list_view'].show()
            if current_index and current_index.isValid():
                tab_data['list_view'].setRootIndex(current_index)
            self.status_bar.showMessage("Režim zobrazení: Seznam", 2000)
            
        elif mode == ViewMode.LARGE_ICONS:
            view_layout.addWidget(tab_data['icon_view'])
            tab_data['icon_view'].show()
            if current_index and current_index.isValid():
                tab_data['icon_view'].setRootIndex(current_index)
            self.status_bar.showMessage("Režim zobrazení: Velké ikony", 2000)
    
    def get_current_view(self):
        """Vrací aktuální aktivní zobrazení pro aktuální záložku"""
        tab_data = self.get_current_tab_data()
        if tab_data:
            return self.get_current_view_for_tab(tab_data)
        return None
    
    def show_status_message(self, message: str):
        """Zobrazí zprávu ve stavovém řádku"""
        self.status_bar.showMessage(message, 3000)
        self.refresh_current_view()
    
    def show_error_message(self, message: str):
        """Zobrazí chybovou zprávu"""
        QMessageBox.warning(self, "Chyba", message)
    
    def update_info_panel(self, index: QModelIndex, tab_index: int):
        """Aktualizuje informační panel při kliknutí na soubor"""
        if tab_index not in self.tab_data:
            return
            
        tab_data = self.tab_data[tab_index]
        info_panel = tab_data['info_panel']
        
        if index.isValid():
            file_path = self.file_model.filePath(index)
            info_panel.update_info(file_path)
        else:
            info_panel.clear_info()
    
    def update_info_panel_selection(self, tab_index: int):
        """Aktualizuje informační panel při změně výběru"""
        if tab_index not in self.tab_data:
            return
            
        tab_data = self.tab_data[tab_index]
        info_panel = tab_data['info_panel']
        current_view = self.get_current_view_for_tab(tab_data)
        
        if current_view and current_view.selectionModel():
            selected_indexes = current_view.selectionModel().selectedRows()
            selected_paths = []
            
            for index in selected_indexes:
                if index.isValid():
                    file_path = self.file_model.filePath(index)
                    selected_paths.append(file_path)
            
            info_panel.update_selection(selected_paths)
        else:
            info_panel.clear_info()
    
    def toggle_info_panel(self):
        """Přepne viditelnost informačního panelu"""
        tab_data = self.get_current_tab_data()
        if not tab_data:
            return
            
        info_panel = tab_data['info_panel']
        if info_panel.isVisible():
            info_panel.hide()
        else:
            info_panel.show()
    
    def show_help(self):
        """Zobrazí nápovědu k aplikaci"""
        help_text = """
<h2>FlexiFiles - Nápověda</h2>

<h3>🔧 Základní ovládání</h3>
<ul>
<li><b>Navigace:</b> Klikněte na složku pro otevření, nebo použijte adresní řádek</li>
<li><b>Zpět/Vpřed:</b> Tlačítka ◀ ▶ nebo Alt+← Alt+→</li>
<li><b>Nahoru:</b> Tlačítko ↑ nebo Alt+↑</li>
<li><b>Obnovit:</b> Tlačítko 🔄 nebo F5</li>
</ul>

<h3>📁 Operace se soubory</h3>
<ul>
<li><b>Otevřít:</b> Dvojité kliknutí na soubor</li>
<li><b>Přejmenovat:</b> Pravé tlačítko → Přejmenovat</li>
<li><b>Smazat:</b> Pravé tlačítko → Smazat nebo klávesa Delete</li>
<li><b>Nová složka:</b> Ctrl+Shift+N</li>
<li><b>Vlastnosti:</b> Pravé tlačítko → Vlastnosti</li>
</ul>

<h3>🔖 Záložky</h3>
<ul>
<li><b>Nová záložka:</b> Ctrl+T</li>
<li><b>Zavřít záložku:</b> Kliknutí na ×</li>
<li><b>Přepínat záložky:</b> Ctrl+Tab</li>
</ul>

<h3>👁️ Zobrazení</h3>
<ul>
<li><b>Přepínání režimů:</b> Tlačítko 🔄 Přepnout zobrazení</li>
<li><b>Informační panel:</b> Ctrl+I nebo tlačítko ℹ️</li>
<li><b>Skrytí/zobrazení panelů:</b> Přetahování hranic</li>
</ul>

<h3>⌨️ Klávesové zkratky</h3>
<ul>
<li><b>F1:</b> Nápověda</li>
<li><b>F5:</b> Obnovit</li>
<li><b>Ctrl+T:</b> Nová záložka</li>
<li><b>Ctrl+Shift+N:</b> Nová složka</li>
<li><b>Ctrl+I:</b> Informační panel</li>
<li><b>Delete:</b> Smazat vybranou položku</li>
<li><b>Enter:</b> Otevřít vybranou položku</li>
</ul>
        """
        
        help_dialog = QMessageBox(self)
        help_dialog.setWindowTitle("FlexiFiles - Nápověda")
        help_dialog.setTextFormat(Qt.TextFormat.RichText)
        help_dialog.setText(help_text)
        help_dialog.setIcon(QMessageBox.Icon.Information)
        help_dialog.exec()
    
    def show_about(self):
        """Zobrazí informace o aplikaci"""
        version_info = self.get_version_info()
        
        # Sestavení detailních informací o verzi
        version_details = f"Verze: {version_info['version']}"
        if version_info['git_hash'] != 'unknown':
            version_details += f" (git: {version_info['git_hash']})"
        if version_info['has_changes']:
            version_details += " - obsahuje neuložené změny"
            
        build_date = version_info['commit_date'] if version_info['commit_date'] != 'unknown' else datetime.now().strftime("%Y-%m-%d")
        
        about_text = f"""
<h2>FlexiFiles</h2>
<h3>Profesionální správce souborů</h3>

<p><b>{version_details}</b></p>
<p><b>Datum buildu:</b> {build_date}</p>
<p><b>Počet commitů:</b> {version_info['commit_count']}</p>

<h4>🌟 Funkce:</h4>
<ul>
<li>Moderní uživatelské rozhraní s PyQt6</li>
<li>Podpora záložek pro efektivní práci</li>
<li>Tři režimy zobrazení (Podrobnosti, Seznam, Ikony)</li>
<li>Informační panel s detaily souborů</li>
<li>Náhledy obrázků</li>
<li>Statistiky složek</li>
<li>Klávesové zkratky</li>
<li>Kontextová menu</li>
</ul>

<h4>🛠️ Technologie:</h4>
<ul>
<li><b>Python:</b> Programovací jazyk</li>
<li><b>PyQt6:</b> GUI framework</li>
<li><b>Windows:</b> Optimalizováno pro Windows</li>
</ul>

<h4>📄 Licence:</h4>
<p>MIT License - Open Source software</p>

<h4>👨‍💻 Autor:</h4>
<p>Vytvořeno pomocí GitHub Copilot</p>

<p><i>FlexiFiles je moderní, rychlý a intuitivní správce souborů<br>
navržený pro zvýšení produktivity při práci se soubory.</i></p>
        """
        
        about_dialog = QMessageBox(self)
        about_dialog.setWindowTitle("O aplikaci FlexiFiles")
        about_dialog.setTextFormat(Qt.TextFormat.RichText)
        about_dialog.setText(about_text)
        about_dialog.setIcon(QMessageBox.Icon.Information)
        
        # Nastavení ikony aplikace v dialogu
        try:
            icon_path = os.path.join(os.path.dirname(__file__), 'flexifiles_icon.png')
            if os.path.exists(icon_path):
                about_dialog.setWindowIcon(QIcon(icon_path))
        except Exception:
            pass
            
        about_dialog.exec()


def main():
    """Hlavní funkce aplikace"""
    app = QApplication(sys.argv)
    
    # Nastavení stylu aplikace pro Windows
    app.setStyle('WindowsVista')
    
    # Vytvoření a zobrazení hlavního okna
    window = FileBrowserMainWindow()
    window.show()
    
    # Spuštění aplikace
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
