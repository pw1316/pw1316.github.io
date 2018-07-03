---
layout: page
title: Foudations of Machine Learning
showbar: false
---

## Cross-Validation

将整个数据集平均分成n份，每份m个数据，经验误差

$$ \hat{R}_{CV}(\theta)=\frac{1}{n}\sum_{i=1}^n{\frac{1}{m_i}}\sum_{j=1}^{m_i}L(h_i(x_{ij}),y_{ij}) $$

