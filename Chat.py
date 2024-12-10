import sys
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets
import ctypes
from ctypes import wintypes
import os


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

class ChatOverlay(QtWidgets.QMainWindow):
    def __init__(self, url, width=300, height=600):
        super().__init__()
        
        
        self.edit_mode = False

        
        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.Tool
        )

        
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground, True)
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, True)

        
        self.resize(width, height)
        self.move(100, 100)  

        
        self.browser = QtWebEngineWidgets.QWebEngineView(self)
        self.browser.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.browser.setStyleSheet("background:transparent;")  
        self.browser.page().setBackgroundColor(QtCore.Qt.transparent)  

        self.setCentralWidget(self.browser)

        
        self.setWindowOpacity(0.4)

        
        self.setStyleSheet("background-color: transparent;")

        
        self.show()
        self.set_window_extras()

        
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.check_control_key)
        self.timer.start(100)  

        
        self.browser.page().loadFinished.connect(self.on_load_finished)

        
        self.offset = None

        
        self.load_embedded_html(url)

    def set_window_extras(self):
        hwnd = self.winId().__int__()
        
        ex_style = GetWindowLong(hwnd, GWL_EXSTYLE)
        
        ex_style |= WS_EX_LAYERED | WS_EX_TRANSPARENT | WS_EX_TOOLWINDOW | WS_EX_NOACTIVATE
        SetWindowLong(hwnd, GWL_EXSTYLE, ex_style)
        
        SetLayeredWindowAttributes(hwnd, 0, int(255 * 0.4), 0x02)  

    def load_embedded_html(self, url):
        
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
                src="{url}"
                allow="allow-same-origin allow-scripts"
                id="chatFrame">
            </iframe>
        </body>
        </html>
        """
        self.browser.setHtml(html, QtCore.QUrl(""))

    def switch_to_edit_mode(self):
        if self.edit_mode:
            return  

        self.edit_mode = True

        
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, False)

        
        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.Window |  
            QtCore.Qt.Tool
        )

        
        self.setWindowOpacity(1.0)

        
        self.setStyleSheet("background-color: transparent;")

        
        self.show()

    def switch_to_overlay_mode(self):
        if not self.edit_mode:
            return  

        self.edit_mode = False

        
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, True)

        
        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.Tool
        )

        
        self.setWindowOpacity(0.4)

        
        self.show()

    def check_control_key(self):
        
        is_control_pressed = bool(GetAsyncKeyState(VK_CONTROL) & 0x8000)

        if is_control_pressed and not self.edit_mode:
            self.switch_to_edit_mode()
        elif not is_control_pressed and self.edit_mode:
            self.switch_to_overlay_mode()

    def on_load_finished(self):
        
        
        js = """
        (function() {
            // Aguardar o iframe carregar
            var iframe = document.getElementById('chatFrame');
            if (!iframe) return;

            iframe.onload = function() {
                try {
                    var iframeDoc = iframe.contentDocument || iframe.contentWindow.document;

                    // Adicionar elemento de áudio
                    var audio = iframeDoc.createElement('audio');
                    audio.src = 'https://uploads.twitchalerts.com/000/186/728/273/%5BZELDA%5D%20NAVI%20-%20HEY%20LISTEN%20%21%20Sound%20Effect%20%5BFree%20Ringtones%20Download%5D.ogg';
                    audio.id = 'notificationSound';
                    iframeDoc.body.appendChild(audio);

                    // Configurar MutationObserver
                    var observer = new MutationObserver(function(mutations) {
                        mutations.forEach(function(mutation) {
                            if (mutation.addedNodes.length) {
                                var sound = iframeDoc.getElementById('notificationSound');
                                if (sound) {
                                    sound.play();
                                }
                            }
                        });
                    });

                    // Observar mudanças no contêiner de mensagens
                    var target = iframeDoc.getElementById('log');
                    if (target) {
                        observer.observe(target, { childList: true });
                    }
                } catch (e) {
                    console.log('Erro ao acessar o conteúdo do iframe:', e);
                }
            };
        })();
        """
        self.browser.page().runJavaScript(js)

    
    def mousePressEvent(self, event):
        if self.edit_mode:
            return
        if event.button() == QtCore.Qt.LeftButton:
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.edit_mode:
            return
        if self.offset is not None and event.buttons() & QtCore.Qt.LeftButton:
            self.move(self.pos() + event.pos() - self.offset)

    def mouseReleaseEvent(self, event):
        if self.edit_mode:
            return
        self.offset = None

def main():
    app = QtWidgets.QApplication(sys.argv)
    
    chat_url = "https://streamlabs.com/widgets/chat-box/v1/4485FA70F1938B583520"
    overlay = ChatOverlay(chat_url, width=300, height=600)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
