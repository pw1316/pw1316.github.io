---
layout: page
title: NvCloth
date: 2024-09-13 14:40:38 +0800
mdate: 2024-09-13 14:40:38 +0800
---

# Cook

NvCloth provides an default cooker that generates cloth data from an simple mesh

## Mesh Description

- point: vertex array
- stiffness: stiffness for each point (optional)
- invMass: inverse mass (A.K.A. 1/m) for each point
- indexArray: triangle/quad

## Cook from Mesh Description

### Constraints

Basically NvCloth has 4 types of constraint:

- stretch(horizontal/vertical depending on the direction of gravity)
- bend
- shear

Each constraint represents a spring that contains following properties:

- vertex indices of the 2 end points
- rest length of the spring
- stiffness of the spring (stiffness = log_2(1-min(stiffnessA, stiffnessB)))

### Phases

Phases are sets of constraints that follow those rules:

- constraints in the same sets have a same type
- adjacent constraints are not in the same set

This makes us to solve constraints in different phases independently

### Tether

Tether means there are some points which can not move freely. We mark those point by set invMass to 0



## Fabric

### ClothMeshDesc


## Cloth

- gravity: we use its direction to distinguish between horizontal stretch and vertical stretch
- triangles: combine indexArray in FabricMesh
- edges: stretch/shear/bend
- constraints: valid edges (remove edges that does not have any constraint)
  - constraint types: bending/shearing/horizontal/vertical (depending on gravity's direction)
- 
  valency 不去重的边，valency[i] -> 编号0~i的所有顶点连接的边数 这里同时给边编号了 0号顶点的边编号0~valency[0] - 1，1号顶点的边编号valency[0]~valency[1]-1，这里AB和BA算两条边
  adjacencies 记录每条边的目标顶点(起始点已经由valency的key确定了)