import os

str = list("""`.-':_,^=;><+!rc*/z?sLTv)J7(|Fi{C}fI31tlu[neoZ5Yxjya]2ESwqkP6h9d4VpOGbUAKXHm8RD#$Bg0MNWQ%&@""")
print(''.join(str[::-1]))
dir = os.path.dirname(os.path.abspath(__file__))
os.mkdir(dir + '/frames')
