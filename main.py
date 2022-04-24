#Inporta as bibliotecas
import PySimpleGUI as sg
from datetime import datetime, timezone, timedelta
from pyfirmata import Arduino
import time
import schedule

# variaveis
#atmega = Arduino('COM3')

#pino 2 responde ao avanço do pistão principal
#pino 4 responde ao retorno do pistão principal
#pino 6 responde ao avanço do pistão do funil
#pino 8 responde ao retorno do pistão do funil

# movimentar o pistão principal
def avancarpp():
    atmega.digital[2].write(1) #define o arduino e sua porta e seu estado
    atmega.digital[4].write(0)
    print('pistão pricipal avançado')
    time.sleep(2)



def retornarpp():
    atmega.digital[2].write(0) #define o arduino e sua porta e seu estado
    atmega.digital[4].write(1)
    print('pistão pricipal retornado')
    time.sleep(2)

# movimentar pistão do funil
def avancarpfunil():
    atmega.digital[6].write(1) #define o arduino e sua porta e seu estado
    atmega.digital[8].write(0)
    print('pistão funi avançado')
    time.sleep(1)

def retornarpfunil():
    atmega.digital[6].write(0) #define o arduino e sua porta e seu estado
    atmega.digital[8].write(1)
    print('pistão funil retornado')
    time.sleep(2)

#realizar os movimentos para alimentar os dois campos
def colocar_comida():

    avancarpfunil()
    retornarpfunil()
    time.sleep(2)
    avancarpp()
    time.sleep(5)
    avancarpfunil()
    retornarpfunil()
    time.sleep(2)
    retornarpp()
    print('fim do ciclo')
    #importa as bibliotecas que serão utilizadas
    buscar_hora()

#função que salva o horario no momento em que é chamada
def buscar_hora():
    difference = timedelta(hours=-3)
    datehournow = datetime.now()
    timez = timezone(difference)

    localdate = datehournow.astimezone(timez)
    textlocaldate = localdate.strftime('%d/%m/%Y - %H:%M')

    print(textlocaldate)

#cria a interface grafica
sg.theme('DarkPurple1')

layout = [
    [sg.Text('Insira as informações em formato HH:MM')],
    [sg.Text('Seu Nome'), sg.InputText(key='usuario', size=(20, 1)),],
    [sg.Text('Primeiro Horario'), sg.InputText(key='ifirst', size=(2, 1)),
    sg.Text(':'),sg.InputText(key='ifirstmin', size=(2, 1))],
    [sg.Text('Ultimo Horario  '), sg.InputText(key='ilast', size=(2, 1)),
     sg.Text(':'),sg.InputText(key='ilastmin', size=(2, 1))],
    [sg.Text('Horario intermediario'), sg.InputText(key='ibreak', size=(2, 1)),
     sg.Text(':'),sg.InputText(key='ibreakmin', size=(2, 1))],
    [sg.Button('COMPUTAR'), sg.Button('ENVIAR')],
    [sg.Button('CANCELAR')]
]

layoutfunc = [
    [sg.Text('Sistema em fincionamento')],
    [sg.Button('PARAR'), sg.Button('Gerar Telatorio')]
]

#cria a janela a ser mostrada
window = sg.Window('Alimentação Automatica', layout)
#evento do loop para o processo de input

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'CANCELAR':
        break
        #verifica as regras de negocio relacionados aos horarios
    if event == 'COMPUTAR':
        primeiro = int(values['ifirst'])
        ultimo = int(values['ilast'])
        intervalo = int(values['ibreak'])
        contintervalo = ultimo - primeiro
        if primeiro< 25:
            if ultimo > primeiro and ultimo < 25:
                if intervalo < contintervalo:
                    sg.popup('As informações são validas \n'
                             'Para salvar clique em ENVIAR')
                else:
                    sg.popup('As informações não são validas! \n'
                             'O intervalo é maior que o primeiro e segundo horario! \n'
                             'Favor volte e coloque um horario valido')
            else:
                sg.popup('As informações não são validas! \n'
                         'O ultimo horario é maior que 24 horas ou é menor que o primeiro! \n'
                         'Favor volte e coloque um horario valido')
        else:
            sg.popup('As informações não são validas \n'
                     'O primeiro horario é maior que 24 horas \n'
                     'Favor volte e coloque um horario valido')
    if event == 'ENVIAR':
        sg.popup('O sistema entrará em funcionamento \n'
                 'Clique em OK para iniciar \n'
                 'Clique em cancelar para parar')
        varfirst = values['ifirst'] + ':' + values['ifirstmin']
        varlast = values['ilast'] + ':' + values['ilastmin']
        varbreak = values['ibreak'] + ':' + values['ibreakmin']

        #printa os horarios inseridos
        print(varfirst, varlast, varbreak)

        #informa os horarios em que as tarefas serão pendentes de execução
        schedule.every().day.at(varfirst).do(colocar_comida)
        schedule.every().day.at(varlast).do(colocar_comida)
        schedule.every().day.at(varbreak).do(colocar_comida)

        window.close()

        #verifica as tarefas pendentes de execulçao e executa
        while 1:
            schedule.run_pending()
            time.sleep(1)

window.close()