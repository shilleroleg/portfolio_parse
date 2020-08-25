from MorningStar_wrapper import Wrapper

isin = 'RU000A0JPVK8'
w = Wrapper(isin)
print(w.getTicker())