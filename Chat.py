import sys
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets, QtGui
import ctypes
from ctypes import wintypes
import os
import json


GWL_EXSTYLE = -20
WS_EX_LAYERED = 0x00080000
WS_EX_TRANSPARENT = 0x00000020
WS_EX_TOOLWINDOW = 0x00000080
WS_EX_NOACTIVATE = 0x08000000

VK_CONTROL = 0x11  


user32 = ctypes.windll.user32
SetWindowLong = user32.SetWindowLongW
GetWindowLong = user32.GetWindowLongW
SetLayeredWindowAttributes = user32.SetLayeredWindowAttributes
GetAsyncKeyState = user32.GetAsyncKeyState


SetWindowLong.argtypes = [wintypes.HWND, ctypes.c_int, wintypes.LONG]
SetWindowLong.restype = wintypes.LONG

GetWindowLong.argtypes = [wintypes.HWND, ctypes.c_int]
GetWindowLong.restype = wintypes.LONG

SetLayeredWindowAttributes.argtypes = [wintypes.HWND, wintypes.COLORREF, ctypes.c_byte, wintypes.DWORD]
SetLayeredWindowAttributes.restype = wintypes.BOOL


# Classe para configuração do sistema
class ConfigManager:
    """
    Gerencia a configuração do aplicativo, incluindo carregamento,
    salvamento e fornecimento de valores padrão.
    """
    DEFAULT_CONFIG = {
        "url": "https://streamlabs.com/widgets/chat-box/v1/4485FA70F1938B583520",
        "width": 300,
        "height": 600,
        "opacity": 40,  # 0-100
        "position_x": 100,
        "position_y": 100,
        "enable_sound": True,
        "sound_url": "https://uploads.twitchalerts.com/000/186/728/273/%5BZELDA%5D%20NAVI%20-%20HEY%20LISTEN%20%21%20Sound%20Effect%20%5BFree%20Ringtones%20Download%5D.ogg",
        "hotkey": VK_CONTROL,
        "hotkey_name": "Control"
    }
    
    def __init__(self, config_file="chat_overlay_config.json"):
        self.config_file = config_file
        self.config = self.load_config()
    
    def load_config(self):
        """Carrega a configuração do arquivo ou usa valores padrão"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    # Mescla com os padrões para garantir que todos os campos existam
                    config = self.DEFAULT_CONFIG.copy()
                    config.update(loaded_config)
                    return config
        except Exception as e:
            print(f"Erro ao carregar configuração: {e}")
        
        return self.DEFAULT_CONFIG.copy()
    
    def save_config(self, config=None):
        """Salva a configuração atual no arquivo"""
        if config:
            self.config = config
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Erro ao salvar configuração: {e}")
            return False
    
    def get(self, key, default=None):
        """Obtém um valor de configuração específico"""
        return self.config.get(key, default)
    
    def set(self, key, value):
        """Define um valor de configuração específico"""
        self.config[key] = value
    
    def update(self, new_config):
        """Atualiza várias configurações de uma vez"""
        self.config.update(new_config)


class ConfigDialog(QtWidgets.QDialog):
    """
    Diálogo para configurar as preferências do Chat Overlay
    """
    def __init__(self, config_manager, parent=None):
        super().__init__(parent)
        self.config = config_manager
        self.setWindowTitle("Configurações do Chat Overlay")
        self.setMinimumWidth(400)
        
        # Adicione esta linha para definir a cor de fundo
        self.setStyleSheet("background-color: white;")  # Defina uma cor de fundo visível
        
        layout = QtWidgets.QVBoxLayout()
        
        # URL do chat
        url_layout = QtWidgets.QHBoxLayout()
        url_layout.addWidget(QtWidgets.QLabel("URL do Chat:"))
        self.url_input = QtWidgets.QLineEdit(self.config.get("url"))
        url_layout.addWidget(self.url_input)
        layout.addLayout(url_layout)
        
        # Dimensões
        dim_layout = QtWidgets.QHBoxLayout()
        dim_layout.addWidget(QtWidgets.QLabel("Largura:"))
        self.width_input = QtWidgets.QSpinBox()
        self.width_input.setRange(100, 1000)
        self.width_input.setValue(self.config.get("width"))
        dim_layout.addWidget(self.width_input)
        
        dim_layout.addWidget(QtWidgets.QLabel("Altura:"))
        self.height_input = QtWidgets.QSpinBox()
        self.height_input.setRange(100, 1000)
        self.height_input.setValue(self.config.get("height"))
        dim_layout.addWidget(self.height_input)
        layout.addLayout(dim_layout)
        
        # Transparência
        opacity_layout = QtWidgets.QHBoxLayout()
        opacity_layout.addWidget(QtWidgets.QLabel("Transparência:"))
        self.opacity_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.opacity_slider.setRange(0, 100)
        self.opacity_slider.setValue(self.config.get("opacity"))
        self.opacity_value = QtWidgets.QLabel(f"{self.config.get('opacity')}%")
        self.opacity_slider.valueChanged.connect(
            lambda v: self.opacity_value.setText(f"{v}%")
        )
        opacity_layout.addWidget(self.opacity_slider)
        opacity_layout.addWidget(self.opacity_value)
        layout.addLayout(opacity_layout)
        
        # Som de notificação
        sound_layout = QtWidgets.QVBoxLayout()
        
        sound_enable_layout = QtWidgets.QHBoxLayout()
        self.sound_checkbox = QtWidgets.QCheckBox("Habilitar Som de Notificação")
        self.sound_checkbox.setChecked(self.config.get("enable_sound"))
        sound_enable_layout.addWidget(self.sound_checkbox)
        sound_layout.addLayout(sound_enable_layout)
        
        sound_url_layout = QtWidgets.QHBoxLayout()
        sound_url_layout.addWidget(QtWidgets.QLabel("URL do Som:"))
        self.sound_url_input = QtWidgets.QLineEdit(self.config.get("sound_url"))
        sound_url_layout.addWidget(self.sound_url_input)
        sound_layout.addLayout(sound_url_layout)
        
        layout.addLayout(sound_layout)
        
        # Tecla de atalho para edição
        hotkey_layout = QtWidgets.QHBoxLayout()
        hotkey_layout.addWidget(QtWidgets.QLabel("Tecla para alternar modo:"))
        
        self.hotkey_combo = QtWidgets.QComboBox()
        self.hotkeys = {
            "Control": VK_CONTROL,
            "Shift": 0x10,
            "Alt": 0x12,
            "F1": 0x70,
            "F2": 0x71,
            "F3": 0x72,
            "F4": 0x73
        }
        
        for key_name in self.hotkeys:
            self.hotkey_combo.addItem(key_name)
        
        current_hotkey_name = self.config.get("hotkey_name", "Control")
        current_index = self.hotkey_combo.findText(current_hotkey_name)
        if current_index >= 0:
            self.hotkey_combo.setCurrentIndex(current_index)
        
        hotkey_layout.addWidget(self.hotkey_combo)
        layout.addLayout(hotkey_layout)
        
        # Botões
        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
        self.setLayout(layout)
    
    def accept(self):
        # Salvar configurações
        self.config.update({
            "url": self.url_input.text(),
            "width": self.width_input.value(),
            "height": self.height_input.value(),
            "opacity": self.opacity_slider.value(),
            "enable_sound": self.sound_checkbox.isChecked(),
            "sound_url": self.sound_url_input.text(),
            "hotkey_name": self.hotkey_combo.currentText(),
            "hotkey": self.hotkeys[self.hotkey_combo.currentText()]
        })
        
        # Adicione um log para verificar se as configurações estão corretas
        print("Salvando configurações:", self.config.config)

        if self.config.save_config():
            super().accept()  # Fecha o diálogo se a configuração for salva com sucesso
        else:
            QtWidgets.QMessageBox.warning(self, "Erro", "Não foi possível salvar as configurações.")


class ChatOverlay(QtWidgets.QMainWindow):
    """
    Janela de sobreposição que exibe o chat do Streamlabs.
    
    Permite alternar entre o modo de edição (para reposicionamento da janela)
    e o modo overlay (janela transparente e sem interação com o mouse) ao pressionar a tecla configurada.
    """
    def __init__(self, config_manager):
        super().__init__()
        
        self.config = config_manager
        self.edit_mode = False
        
        # Carregar configurações
        self.load_configurations()
        
        # Configurar ícone da aplicação na bandeja do sistema
        self.setup_tray()
        
        # Configurar a janela
        self.setup_window()
        
        # Mostrar a janela e aplicar propriedades extras
        self.show()
        self.set_window_extras()
        
        # Configurar timer para verificar a tecla de atalho
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.check_hotkey)
        self.timer.start(100)
        
        # Conectar eventos
        self.browser.page().loadFinished.connect(self.on_load_finished)
        
        # Para arrastar a janela
        self.offset = None
        
        # Carregar o HTML com o chat incorporado
        self.load_embedded_html()
    
    def load_configurations(self):
        self.url = self.config.get("url")
        self.width = self.config.get("width")
        self.height = self.config.get("height")
        self.opacity = self.config.get("opacity") / 100
        self.position_x = self.config.get("position_x")
        self.position_y = self.config.get("position_y")
        self.enable_sound = self.config.get("enable_sound")
        self.sound_url = self.config.get("sound_url")
        self.hotkey = self.config.get("hotkey")
    
    def setup_window(self):
        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.Tool
        )
        
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)  # Mantenha a transparência
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground, True)
        
        self.resize(self.width, self.height)
        self.move(self.position_x, self.position_y)
        
        self.setWindowOpacity(self.opacity)  # Aplique a opacidade
        self.setStyleSheet("background-color: transparent;")  # Mantenha a cor de fundo transparente
        
        # Configurar o navegador
        self.browser = QtWebEngineWidgets.QWebEngineView(self)
        self.browser.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.browser.setStyleSheet("background:transparent;")
        self.browser.page().setBackgroundColor(QtCore.Qt.transparent)
        
        self.setCentralWidget(self.browser)
        
        # Remover fundo
        self.setStyleSheet("background-color: transparent;")
    
    def setup_tray(self):
        """Configura o ícone na bandeja do sistema e seu menu"""
        self.tray_icon = QtWidgets.QSystemTrayIcon(self)
        
        # Criar ícone padrão se não tiver um personalizado
        icon = QtGui.QIcon()
        pixmap = QtGui.QPixmap(16, 16)
        pixmap.fill(QtGui.QColor(0, 120, 215))
        icon.addPixmap(pixmap)
        self.tray_icon.setIcon(icon)
        
        # Menu
        tray_menu = QtWidgets.QMenu()
        
        open_config_action = tray_menu.addAction("Configurações")
        open_config_action.triggered.connect(self.open_config_dialog)
        
        toggle_visibility = tray_menu.addAction("Mostrar/Ocultar")
        toggle_visibility.triggered.connect(self.toggle_visibility)
        
        reload_action = tray_menu.addAction("Recarregar Chat")
        reload_action.triggered.connect(self.reload_chat)
        
        exit_action = tray_menu.addAction("Sair")
        exit_action.triggered.connect(self.close_application)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.setToolTip("Chat Overlay")
        self.tray_icon.show()
    
    def toggle_visibility(self):
        """Alterna a visibilidade da janela"""
        if self.isVisible():
            self.hide()
        else:
            self.show()
            self.activateWindow()
    
    def reload_chat(self):
        """Recarrega o chat"""
        self.load_embedded_html()
    
    def close_application(self):
        """Fecha a aplicação completamente"""
        # Salvar posição atual
        self.config.set("position_x", self.x())
        self.config.set("position_y", self.y())
        self.config.save_config()
        
        # Fechar a aplicação
        QtWidgets.QApplication.quit()
    
    def open_config_dialog(self):
        """Abre o diálogo de configuração"""
        dialog = ConfigDialog(self.config, self)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            # Recarregar configurações
            self.url = self.config.get("url")
            self.width = self.config.get("width")
            self.height = self.config.get("height")
            self.opacity = self.config.get("opacity") / 100
            self.enable_sound = self.config.get("enable_sound")
            self.sound_url = self.config.get("sound_url")
            self.hotkey = self.config.get("hotkey")
            
            # Aplicar mudanças
            self.resize(self.width, self.height)
            self.setWindowOpacity(self.opacity)
            self.reload_chat()
    
    def set_window_extras(self):
        """Aplica propriedades avançadas da janela"""
        hwnd = self.winId().__int__()
        
        ex_style = GetWindowLong(hwnd, GWL_EXSTYLE)
        
        ex_style |= WS_EX_LAYERED | WS_EX_TRANSPARENT | WS_EX_TOOLWINDOW | WS_EX_NOACTIVATE
        SetWindowLong(hwnd, GWL_EXSTYLE, ex_style)
        
        # Aplicar opacidade
        SetLayeredWindowAttributes(hwnd, 0, int(255 * self.opacity), 0x02)

    def load_embedded_html(self):
        """Carrega o HTML com o iframe do chat incorporado"""
        
        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Streamlabs Chat</title>
            <style>
                body, html {{
                    margin: 0;
                    padding: 0;
                    background: transparent;
                    overflow: hidden;
                    height: 100%;
                    width: 100%;
                }}
                iframe {{
                    border: none;
                    height: 100%;
                    width: 100%;
                    background: transparent;
                }}
            </style>
        </head>
        <body>
            <iframe
                src="{self.url}"
                id="chatFrame">
            </iframe>
        </body>
        </html>
        """
        self.browser.setHtml(html, QtCore.QUrl(""))

    def switch_to_edit_mode(self):
        """Ativa o modo de edição, permitindo interação com a janela"""
        if self.edit_mode:
            return  

        self.edit_mode = True

        # Permitir interação com o mouse
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, False)

        # Mudar flags da janela
        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.Window |  
            QtCore.Qt.Tool
        )

        # Aumentar a opacidade para melhor visualização
        self.setWindowOpacity(1.0)

        # Manter fundo transparente
        self.setStyleSheet("background-color: transparent;")

        # Reexibir com as novas configurações
        self.show()

    def switch_to_overlay_mode(self):
        """Retorna ao modo overlay, com transparência e sem interação com o mouse"""
        if not self.edit_mode:
            return  

        self.edit_mode = False

        # Desabilitar interação com o mouse
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, True)

        # Restaurar flags da janela
        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.Tool
        )

        # Restaurar opacidade configurada
        self.setWindowOpacity(self.opacity)

        # Reexibir com as novas configurações
        self.show()

    def check_hotkey(self):
        """
        Verifica se a tecla configurada está pressionada e alterna entre o modo de edição
        e o modo overlay.
        """
        is_key_pressed = bool(GetAsyncKeyState(self.hotkey) & 0x8000)
        if is_key_pressed and not self.edit_mode:
            self.switch_to_edit_mode()
        elif not is_key_pressed and self.edit_mode:
            self.switch_to_overlay_mode()

    def on_load_finished(self):
        """Executado quando o carregamento do HTML é concluído"""
        
        # Só adiciona o som se estiver habilitado
        if not self.enable_sound:
            return
        
        js = f"""
        (function() {{
            // Aguardar o iframe carregar
            var iframe = document.getElementById('chatFrame');
            if (!iframe) return;

            iframe.onload = function() {{
                try {{
                    var iframeDoc = iframe.contentDocument || iframe.contentWindow.document;

                    // Adicionar elemento de áudio
                    var audio = iframeDoc.createElement('audio');
                    audio.src = '{self.sound_url}';
                    audio.id = 'notificationSound';
                    iframeDoc.body.appendChild(audio);

                    // Configurar MutationObserver
                    var observer = new MutationObserver(function(mutations) {{
                        mutations.forEach(function(mutation) {{
                            if (mutation.addedNodes.length) {{
                                var sound = iframeDoc.getElementById('notificationSound');
                                if (sound) {{
                                    sound.play();
                                }}
                            }}
                        }});
                    }});

                    // Observar mudanças no contêiner de mensagens
                    var target = iframeDoc.getElementById('log');
                    if (target) {{
                        observer.observe(target, {{ childList: true }});
                    }}
                }} catch (e) {{
                    console.log('Erro ao acessar o conteúdo do iframe:', e);
                }}
            }};
        }})();
        """
        self.browser.page().runJavaScript(js)

    def mousePressEvent(self, event):
        if not self.edit_mode:
            return
        if event.button() == QtCore.Qt.LeftButton:
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if not self.edit_mode:
            return
        if self.offset is not None and event.buttons() & QtCore.Qt.LeftButton:
            self.move(self.pos() + event.pos() - self.offset)

    def mouseReleaseEvent(self, event):
        if not self.edit_mode:
            return
        self.offset = None
        
        # Salvar a nova posição
        self.config.set("position_x", self.x())
        self.config.set("position_y", self.y())
        self.config.save_config()

    def closeEvent(self, event):
        """Intercepta o evento de fechamento para minimizar para a bandeja do sistema"""
        # Ignora o fechamento e apenas oculta a janela
        event.ignore()
        self.hide()
        
        # Mostra uma notificação na primeira vez
        if not hasattr(self, 'close_notification_shown'):
            self.tray_icon.showMessage(
                "Chat Overlay",
                "O aplicativo continuará rodando na bandeja do sistema. "
                "Clique com o botão direito no ícone para mais opções.",
                QtWidgets.QSystemTrayIcon.Information,
                3000
            )
            self.close_notification_shown = True


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)  # Permite que o app continue rodando com janelas fechadas
    
    # Carregar configurações
    config_manager = ConfigManager()
    
    # Verificar se é a primeira execução
    if not os.path.exists(config_manager.config_file):
        # Exibir diálogo de configuração
        dialog = ConfigDialog(config_manager)
        if dialog.exec_() != QtWidgets.QDialog.Accepted:
            sys.exit("Configuração cancelada. Encerrando o programa.")
    
    # Criar e exibir o overlay
    overlay = ChatOverlay(config_manager)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()