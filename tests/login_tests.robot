*** Settings ***
Library    SeleniumLibrary
Suite Setup     Open Browser    http://localhost:${PORT}/login    Chrome
Suite Teardown  Close Browser

*** Variables ***
${PORT}    8080  # Valor padrão, será sobrescrito

*** Test Cases ***
Valid Login
    Input Text      username    teste@exemplo.com
    Input Password  password    senha123
    Click Button    Entrar
    Page Should Contain  Bem-vindo ao Sistema!

Invalid Login
    Go To    http://localhost:${PORT}/login
    Input Text      username    invalido@teste.com
    Input Password  password    errada
    Click Button    Entrar
    Page Should Contain  Credenciais inválidas!