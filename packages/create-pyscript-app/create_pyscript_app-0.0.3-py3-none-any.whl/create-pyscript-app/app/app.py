import matplotlib.pyplot as plt
import numpy as np

x = np.random.randn(100)
y = np.random.randn(100)
fig, ax = plt.subplots()
fig.patch.set_facecolor('#2D2E35')
ax.patch.set_facecolor('#2D2E35')
ax.scatter(x, y)    # TRY putting ax.step(x, y) in here instead.
ax.text(x=0, y=0, s="<py>", c="orange")
display(fig, target="app")
