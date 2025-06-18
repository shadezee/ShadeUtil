def get_initial_stylesheet(
  background='#121212',
  widgetBackground='#1E1E1E',
  text='#f5d5e0',
  textEditBackground='#252525',
  buttonBackground='#430d4b',
  buttonHover='#7b347e',
  buttonText='#FFFFFF',
  scrollAreaButtonText='#f5d5e0',
  border='#2E2E2E',
  lines='#f5d5e0',
  highlight='#430d4b',
  radioButtonClicked='#a449e4'
):
  return f'''
    QWidget {{
      background-color: {background};
      color: {text};
    }}

    QFrame[frameShape='4'] {{
      background-color: {lines};
      max-height: 1px;
      border: none;
    }}
    QFrame[frameShape='5'] {{
      background-color: {lines};
      max-width: 1px;
      border: none;
    }}

    QPushButton {{
      background-color: {buttonBackground};
      border: 1px solid {border};
      padding: 6px 12px;
      border-radius: 6px;
      color: {buttonText};
      font-weight: bold;
    }}
    QPushButton:hover {{
      background-color: {buttonHover};
    }}
    QPushButton:disabled {{
      background-color: {textEditBackground};
      color: {radioButtonClicked};
    }}

    QScrollArea {{
      border: 1px solid {border};
      border-radius: 4px;
    }}
    QScrollArea QWidget {{
      background-color: {widgetBackground};
      padding: 4px;
    }}
    QScrollArea QWidget QPushButton {{
      background-color: {buttonBackground};
      border: 1px solid {border};
      padding: 6px 12px;
      border-radius: 6px;
      color: {scrollAreaButtonText};
    }}

    QTextEdit, QPlainTextEdit, QLineEdit {{
      background-color: {textEditBackground};
      color: {text};
      border: 1px solid {border};
      padding: 6px;
      border-radius: 4px;
    }}

    QTabWidget::tab-bar {{
      background: {widgetBackground};
    }}
    QTabWidget::pane {{
      background-color: {widgetBackground};
      border: 1px solid {border};
    }}
    QTabBar::tab {{
      background: {textEditBackground};
      color: {text};
      padding: 6px 12px;
      border-top-left-radius: 4px;
      border-top-right-radius: 4px;
      margin-right: 2px;
    }}
    QTabBar::tab:selected {{
      background: {highlight};
      color: {buttonText};
    }}

    QRadioButton {{
      color: {text};
    }}
    QRadioButton::indicator:checked {{
      background-color: {radioButtonClicked};
      border-radius: 8px;
      border: 1px solid {border};
    }}
  '''
