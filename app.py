from flask import Flask, request, render_template
import logging

# Настройка логирования
logging.basicConfig(filename='calculator.log', level=logging.INFO, format='%(asctime)s:%(message)s')

app = Flask(__name__)

calculator = {
    'displayValue': '0',
    'firstOperand': None,
    'waitingForSecondOperand': False,
    'operator': None,
}

def inputDigit(digit):
    if calculator['waitingForSecondOperand']:
        calculator['displayValue'] = digit
        calculator['waitingForSecondOperand'] = False
    else:
        calculator['displayValue'] = digit if calculator['displayValue'] == '0' else calculator['displayValue'] + digit

# функция для добавления точки
def inputDecimal(dot):
    if dot not in calculator['displayValue']:
        calculator['displayValue'] += dot

# логика ввода калькулятора
def handleOperator(nextOperator):
    inputValue = float(calculator['displayValue'])

    if calculator['operator'] and calculator['waitingForSecondOperand']:
        calculator['operator'] = nextOperator
        return

    if calculator['firstOperand'] is None:
        calculator['firstOperand'] = inputValue
    else:
        currentValue = calculator['firstOperand'] or 0
        result = performCalculation[calculator['operator']](currentValue, inputValue)

        # перезагрузка калькулятора при делении на ноль
        if result == 'Ошибка: деление на ноль':
            logging.info(result)
            resetCalculator()
            return result

        calculator['displayValue'] = str(result)
        calculator['firstOperand'] = result

        # Логирование результатов вычислений
        logging.info(f'Выполнена операция: {currentValue} {calculator["operator"]} {inputValue}, результат: {result}')

    calculator['waitingForSecondOperand'] = True
    calculator['operator'] = nextOperator

# осуществление вычислений
performCalculation = {
    '/': lambda firstOperand, secondOperand: firstOperand / secondOperand if secondOperand != 0 else 'Ошибка: деление на ноль',
    '*': lambda firstOperand, secondOperand: firstOperand * secondOperand,
    '+': lambda firstOperand, secondOperand: firstOperand + secondOperand,
    '-': lambda firstOperand, secondOperand: firstOperand - secondOperand,
    '=': lambda firstOperand, secondOperand: secondOperand
}

# функция для сброса калькулятора
def resetCalculator():
    calculator['displayValue'] = '0'
    calculator['firstOperand'] = None
    calculator['waitingForSecondOperand'] = False
    calculator['operator'] = None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        button = request.form.get('button')
        if button == 'all-clear':
            resetCalculator()
        elif button in performCalculation:
            handleOperator(button)
        elif button == '.':
            inputDecimal(button)
        else:
            inputDigit(button)

    return render_template('index.html', display=calculator['displayValue'])

if __name__ == '__main__':
    app.run(debug=True)
