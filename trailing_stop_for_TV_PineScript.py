
// скрипт Pine Script для создания торговой стратегии на платформе TradingView
// This Pine Script™ code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// Пример генерации Трейлинг Стопа
// ! Без цены активации
// ! В обе стороны


//@version=5

# Установка параметров стратегии: strategy() функция определяет основные параметры стратегии: название, 
# наложение на график, пирамидинг и т.д. Например, overlay=true указывает, что стратегия будет наложена на текущий график, 
# а default_qty_value=100 устанавливает количество позиции по умолчанию в 100% от доступного капитала.
strategy(
 "EMA_trailing_stop", 
 overlay=true, 
 pyramiding=0, 
 default_qty_type = strategy.percent_of_equity, 
 default_qty_value=100,
 initial_capital=100
 )


# Входные параметры: input.float() и input.int() используются для определения параметров, 
# которые пользователь может настраивать в интерфейсе Pine Script. Например, 
# trail_dist - это процентное расстояние для трейлинг-стопа, а fast_ema_period и slow_ema_period - периоды для скользящих средних.
trail_dist = input.float(5, "Trail Distance %", minval=1, step=0.5) / 100
fast_ema_period = input.int(20, "Fast MA Period", minval=5, step=5)
slow_ema_period = input.int(100, "Slow MA Period", minval=10, step=10)

# Вычисление скользящих средних: 
# ta.ema() функция используется для вычисления экспоненциального скользящего среднего (EMA) на основе цен закрытия.
fast_ema = ta.ema(close, fast_ema_period)
slow_ema = ta.ema(close, slow_ema_period)
plot(fast_ema, color = color.yellow)
plot(slow_ema, color = color.green)


# Условия входа в позицию: ta.crossover() и ta.crossunder() используются 
# для определения моментов пересечения скользящих средних
entry_long = ta.crossover(fast_ema, slow_ema)
entry_short = ta.crossunder(fast_ema, slow_ema)
var stop_price = 0.0


# Установка трейлинг-стопа: В зависимости от текущей позиции и условий рынка, устанавливается новая цена трейлинг-стопа. 
# Это позволяет автоматически обновлять стоп-заявку в соответствии с изменениями цены, защищая прибыль от потенциальных убытков.
if strategy.position_size == 0
    stop_price := na
    if entry_long
        strategy.entry("long", strategy.long)
    else if entry_short
        strategy.entry("short", strategy.short)
else if strategy.position_size > 0
    stop_new = high * (1 - trail_dist)
    // stop_new = close * (1 - trail_dist)
    stop_price := na(stop_price) ? stop_new : math.max(stop_new, stop_price)
else if strategy.position_size < 0
    stop_new = low * (1 + trail_dist)
    // stop_new = close * (1 - trail_dist)
    stop_price := na(stop_price) ? stop_new : math.min(stop_new, stop_price)

if not na(stop_price) and stop_price != 0.0
    strategy.exit("exit", stop=stop_price)

plot(stop_price != 0.0 ? stop_price : na, color = color.red, style = plot.style_steplinebr)
