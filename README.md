# Livestream Chat Overlay

A Windows desktop application that provides a transparent overlay for your Streamlabs chat, allowing you to keep track of your stream chat while using other applications.

## Features

- **Transparent Overlay**: Places your Streamlabs chat as a transparent overlay on your screen
- **Configurable Appearance**: Customize size, position, and opacity
- **Notification Sound**: Optional sound alerts for new chat messages
- **Toggle Mode**: Quickly switch between "edit mode" and "overlay mode" with a configurable hotkey
- **System Tray Integration**: Minimize to system tray for easy access

## Installation

### Requirements
- Windows OS
- Python 3.6+ (for running from source)
- PyQt5 and QtWebEngine

### Download Binary
1. Download the latest release from the [Releases](https://github.com/FFloriani/livestreamchat/releases) page
2. Extract the ZIP file
3. Run `chat.exe`

### Run from Source
1. Clone this repository
   ```
   git clone https://github.com/FFloriani/livestreamchat.git
   cd livestreamchat
   ```
2. Install dependencies
   ```
   pip install PyQt5 PyQtWebEngine
   ```
3. Run the application
   ```
   python Chat.py
   ```

## Usage

1. When first launched, the application will show your chat in "edit mode"
2. Position the window where you want it on your screen
3. Press the hotkey (default: F1) to toggle to "overlay mode"
4. The window will become transparent and click-through
5. Press the hotkey again to return to "edit mode" for repositioning
6. Right-click the system tray icon for additional options

## Configuration

Configuration options are accessible via the system tray menu:

- **URL**: Your Streamlabs chat widget URL
- **Width/Height**: Size of the overlay window
- **Transparency**: Opacity level of the overlay
- **Notification Sound**: Enable/disable sound alerts and set custom sound URL
- **Hotkey**: Change the key used to toggle between edit and overlay modes

Settings are saved in `chat_overlay_config.json` in the application directory.

## Building from Source

The project includes a PyInstaller spec file for building a standalone executable:

```
pyinstaller Chat.spec
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with PyQt5 and QtWebEngine
- Uses Streamlabs chat widget technology
