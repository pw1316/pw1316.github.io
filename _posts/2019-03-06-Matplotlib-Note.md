---
layout: page
title: matplotlib笔记
date: 2019-03-06 12:11:58 +0800
mdate: 2019-03-06 12:11:58 +0800
showbar: false
---

## 2D坐标轴单位相同

```python
import matplotlib.pyplot as plt

# random scalar with different range
x = np.random.rand(100)
y = np.random.rand(100) * 2
z = np.random.rand(100) * 3

plt.axis('scaled')
plt.hist2d(x, y)
plt.show()
```

## 3D散点坐标轴单位相同

matplotlib(3.0.2)虽然可以让x轴和y轴的单位长度相等，但z轴依旧会自动缩放。为了让z轴也一致，可以人为添加8个点，这8个点是正方形包围盒的顶点。

```python
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# random scalar with different range
x = np.random.rand(100)
y = np.random.rand(100) * 2
z = np.random.rand(100) * 3

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.set_aspect('equal')
ax.scatter(rolls, pitches, yaws)

# Create cubic bounding box to simulate equal aspect ratio
max_range = np.array([x.max()-x.min(), y.max()-y.min(), z.max()-z.min()]).max()
Xb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][0].flatten() + 0.5*(x.max()+x.min())
Yb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][1].flatten() + 0.5*(y.max()+y.min())
Zb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][2].flatten() + 0.5*(z.max()+z.min())
for xb, yb, zb in zip(Xb, Yb, Zb):
   ax.plot([xb], [yb], [zb], 'w')
```
