# UPDATE
## 2026.1.21
### v0.0.3
目前的域随机化是：
1. 动、静摩擦力范围(0.3,0.8),(0.3,1.0),弹性系数(0,0.5)
2. 负重(-1.0,3.0)
3. 关节质量系数缩放(0.9,1.1)
4. 质心x,y,z各偏移5cm
5. KP控制都是(0.9,1.1)
6. 速度偏移x,y (-0.4,0.4),(-0.4,0.4),角速度偏航(-0.6,0.6)
7. 控制延迟(0,4)仿真步(200Hz)

电机从原来的ImplicitActuatorCfg换成DelayedPDActuatorCfg

### v0.0.2
修改了unitree.py中的机器人模型路径，可以成功部署跑起来

## 2026.1.7
### v0.0.1
1. `source/unitree_rl_lab/unitree_rl_lab/tasks/locomotion/robots/g1/29dof/velocity_env_cfg.py` 改了速度指令最大值 Xmin: -0.5 -> -1.0, Ymin: +-0.3 -> 0.5, Zmin: +-0.2 -> 1.0
