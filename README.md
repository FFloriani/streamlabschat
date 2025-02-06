# Overlay Chat for Streamlabs with PyQt5 (English Version)

A Python application that displays the Streamlabs chat in an overlay window using PyQt5 and QtWebEngine. This project allows for easy toggling between edit mode (for repositioning the window) and overlay mode, which is transparent and non-interactive with the mouse.

## Features

- **Transparent Overlay:** Window with 40% opacity that does not interfere with your stream.
- **Edit Mode:** Easily activated by holding the **Control** key, which enables window repositioning.
- **Sound Notifications:** Automatic audio playback for new chat messages.
- **Customizable:** Easy insertion of the Streamlabs Chat widget URL and customization of styles and behaviors.
- **Technologies Used:** Python, PyQt5, QtWebEngine, and Win32 APIs for Windows.

## SEO Keywords

Overlay Chat for Streamlabs, Chat Overlay, Overlay Window, PyQt5 Overlay, Streamlabs Chat, Edit Mode Overlay, Chat Overlay Tutorial, Chat Sound Notifications, Streaming Chat Overlay.

## Prerequisites

- **Python 3.7+**
- [PyQt5](https://pypi.org/project/PyQt5/)
- [PyQtWebEngine](https://pypi.org/project/PyQtWebEngine/)

> **Note:** This project has been developed and tested on Windows due to its use of Win32 API functions via ctypes.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/seu-usuario/FFloriani.git
   cd FFloriani
   ```

2. **Create a virtual environment (optional but recommended):**

   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Linux/MacOS:
   source venv/bin/activate
   ```

3. **Install the dependencies:**

   ```bash
   pip install PyQt5 PyQtWebEngine
   ```

## How to Use

1. **Run the main script:**

   ```bash
   python Chat.py
   ```

2. **Enter the Streamlabs Chat URL:**

   - Upon launch, a dialog will ask for the widget URL of Streamlabs Chat.
   - Enter the desired URL or use the default URL displayed.
   - Example URL:  
     `https://streamlabs.com/widgets/chat-box/v1/4485FA70F1938B583520`

3. **Window Interaction:**

   - **Overlay Mode (Default):**  
     The window is displayed with 40% opacity and does not respond to mouse clicks, avoiding interference with streaming.
   
   - **Edit Mode:**  
     To reposition the window, hold down the **Control** key. In this mode, the window becomes fully opaque and interactive, allowing you to drag it to the desired location.
   
   - **Return to Overlay Mode:**  
     Simply release the **Control** key for the window to revert to a transparent overlay.

4. **Sound Notifications:**

   - An audio element is automatically added to the chat content.
   - When new messages are detected, the defined sound is played, ensuring you do not miss important messages during the stream.

## Advanced Customizations

- **Adjusting Opacity:**  
  To change the overlay transparency, modify the values passed to the `setWindowOpacity` and `SetLayeredWindowAttributes` methods in the code.

- **Theme Modification:**  
  Customize the styles by altering the CSS in the `load_embedded_html` method to suit your visual identity.

- **Window Behavior:**  
  If you wish to modify how the window toggles between edit and overlay modes, adjust the `check_control_key` method and the related functions (`switch_to_edit_mode` and `switch_to_overlay_mode`).

## Known Issues

- **Compatibility:**  
  This script uses Windows-specific APIs. For usage on other operating systems, adaptation of the API calls or using a different approach for window handling is needed.

- **Debugging:**  
  If the window does not appear or there are issues with sound notifications, verify that all dependencies are installed correctly and that your operating system is compatible.

## Contribution

Contributions are welcome! If you wish to enhance the project, fix bugs, or add new features, feel free to open an _issue_ or submit a _pull request_.

## Contact

For questions or suggestions, please contact: [felipeffloriani@gmail.com]

---

# Overlay de Chat para Streamlabs com PyQt5 (Versão em Português)

Uma aplicação Python que exibe o chat do Streamlabs em uma janela de sobreposição (overlay) utilizando PyQt5 e QtWebEngine. Este projeto permite alternar facilmente entre o modo de edição para reposicionar a janela e o modo overlay, que é transparente e não interativa com o mouse.

## Características

- **Overlay Transparente:** Janela com 40% de opacidade que não interfere na sua transmissão.
- **Modo de Edição:** Ativação simples ao manter pressionada a tecla **Control**, permitindo o reposicionamento da janela.
- **Notificações Sonoras:** Reprodução automática de áudio para novas mensagens no chat.
- **Customizável:** Fácil inserção da URL do widget do Streamlabs Chat e personalização de estilos e comportamentos.
- **Tecnologias Utilizadas:** Python, PyQt5, QtWebEngine e APIs Win32 para Windows.

## Palavras-Chave (SEO)

Overlay de Chat para Streamlabs, Chat Overlay, Janela de Sobreposição, PyQt5 Overlay, Streamlabs Chat, Modo de Edição Overlay, Tutorial Overlay de Chat, Notificações Sonoras Chat, Streaming Overlay para Chat.

## Pré-requisitos

- **Python 3.7+**
- [PyQt5](https://pypi.org/project/PyQt5/)
- [PyQtWebEngine](https://pypi.org/project/PyQtWebEngine/)

> **Observação:** Este projeto foi desenvolvido e testado no ambiente Windows, devido ao uso das funções da API Win32 via ctypes.

## Instalação

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/seu-usuario/FFloriani.git
   cd FFloriani
   ```

2. **Crie um ambiente virtual (opcional, mas recomendado):**

   ```bash
   python -m venv venv
   # Ativação no Windows:
   venv\Scripts\activate
   # Ativação no Linux/MacOS:
   source venv/bin/activate
   ```

3. **Instale as dependências:**

   ```bash
   pip install PyQt5 PyQtWebEngine
   ```

## Como Usar

1. **Execute o script principal:**

   ```bash
   python Chat.py
   ```

2. **Insira a URL do Streamlabs Chat:**

   - Ao iniciar, uma janela de diálogo solicitará a URL do widget do Streamlabs Chat.
   - Digite a URL desejada ou utilize a URL padrão exibida.
   - Exemplo de URL:  
     `https://streamlabs.com/widgets/chat-box/v1/4485FA70F1938B583520`

3. **Interação com a Janela:**

   - **Modo Overlay (Padrão):**  
     A janela é exibida com 40% de opacidade e não responde aos cliques do mouse para evitar interferências na transmissão.
   
   - **Modo Edição:**  
     Para reposicionar a janela, mantenha pressionada a tecla **Control**. Nesse modo, a janela se torna totalmente opaca e interativa, permitindo arrastá-la para o local desejado.
   
   - **Retorno ao Modo Overlay:**  
     Simplesmente solte a tecla **Control** para que a janela volte a ser um overlay transparente.

4. **Notificações Sonoras:**

   - Um elemento de áudio é adicionado automaticamente ao conteúdo do chat.
   - Sempre que novas mensagens forem detectadas, o som definido será reproduzido, garantindo que você não perca nenhuma mensagem importante durante a transmissão.

## Customizações Avançadas

- **Ajuste da Opacidade:**  
  Para alterar a transparência do overlay, modifique os valores passados aos métodos `setWindowOpacity` e `SetLayeredWindowAttributes` no código.

- **Modificação do Tema:**  
  Personalize os estilos alterando o CSS presente no método `load_embedded_html` para adequar o visual à sua identidade visual.

- **Comportamento da Janela:**  
  Se desejar modificar a forma como a janela alterna entre os modos de edição e overlay, ajuste o método `check_control_key` e as funções relacionadas (`switch_to_edit_mode` e `switch_to_overlay_mode`).

## Problemas Conhecidos

- **Compatibilidade:**  
  Este script utiliza APIs específicas do Windows. Para rodá-lo em outros sistemas operacionais, será necessário adaptar as chamadas da API ou utilizar outra abordagem para manipulação de janelas.

- **Depuração:**  
  Caso a janela não apareça ou haja problemas com as notificações sonoras, verifique se todas as dependências estão instaladas corretamente e se o seu sistema operacional é compatível.

## Contribuição

Contribuições são bem-vindas! Se você deseja melhorar o projeto, corrigir bugs ou implementar novas funcionalidades, sinta-se à vontade para abrir uma _issue_ ou enviar um _pull request_.

## Contato

Dúvidas ou sugestões? Entre em contato através do email: [felipeffloriani@gmail.com]
