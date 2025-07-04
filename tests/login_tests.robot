*** Settings ***
Library    SeleniumLibrary

*** Variables ***
${PORT}    8080

*** Keywords ***
Open Headless Browser
    ${chrome_options}=    Evaluate    sys.modules['selenium.webdriver'].ChromeOptions()    sys
    Call Method    ${chrome_options}    add_argument    --headless
    Call Method    ${chrome_options}    add_argument    --no-sandbox
    Call Method    ${chrome_options}    add_argument    --disable-dev-shm-usage
    Create WebDriver    Chrome    options=${chrome_options}

*** Test Cases ***
Valid Login
    Open Headless Browser
    Go To    http://localhost:${PORT}/login
    Input Text      username    teste@exemplo.com
    Input Password  password    senha123
    Click Button    Entrar
    Page Should Contain  Bem-vindo ao Sistema!
    [Teardown]    Close Browser

Invalid Login
    Open Headless Browser
    Go To    http://localhost:${PORT}/login
    Input Text      username    invalido@teste.com
    Input Password  password    errada
    Click Button    Entrar
    Page Should Contain  Credenciais inválidas!
    [Teardown]    Close Browser