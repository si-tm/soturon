## 入力値
- [DNA配列](./seq_2022-10-18-032558.dat)
- [configulation file](./generated_2022-10-18-032558.conf)  
タイムステップ T, 箱の辺の長さ Lx, Ly, Lz, 全エネルギー, 位置エネルギー, 運動エネルギー Etot, U, K   
- [topology](./generated_2022-10-18-032558.top)  
鎖内の固定結合トポロジー（どのヌクレオチドがバックボーンリンクを共有しているか）
- [input](https://github.com/si-tm/oxDNA/blob/master/try_my_sample/input)
steps = 10
- [input_seq_dep](https://github.com/si-tm/oxDNA/blob/master/try_my_sample/input_seq_dep)
- [input_trap](https://github.com/si-tm/oxDNA/blob/master/try_my_sample/input_trap)  

## 出力結果
- [energy.dat](./energy.dat)  
 **[時間 (ステップ * dt)][ポテンシャルエネルギー][運動エネルギー][全エネルギー]**
- [hb_energy.dat](./hb_energy.dat)  
?? 
- [last_conf.dat](./last_conf.dat)  
this is the file where the last configuration is saved (when the program finishes or is killed). Set to last_conf.dat by default  
- [log_seq_dep.dat](./log_seq_dep.dat)  
- [log_trap.dat](./log_trap.dat)  
- [trajectory.dat](./trajectory.dat)  
In the configuration/trajectory files only the positions and orientations of the nucleotides are stored. If one wants to recover the positions of the individual interaction sites in the model, some maths need to be done.
