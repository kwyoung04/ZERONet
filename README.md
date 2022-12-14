# 실험 데이터셋

| Data | Frame |
| --- | --- |
| train | 4167 |
| val | 465 |

| Pedestrian | Person | Car | Bus | Truck | Cyclist | Motorcyclist | Misc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Pedestrian | Unknown | Car | Bus | Truck | BicycleRider | MotorcyleRider | Misc |
| 74595 | 1755 | 219 | 0 | 1586 | 82 | 152 | 229 |

# 테스트 결과

1. SECOND (KITTI)
    
    ![Untitled](image/Untitled.png)
    
2. SECOND
    1. 0.0116 sec
    2. 57.307 AP

![Untitled](image/Untitled%201.png)

1. voxel rcnn
    1. 0.0186 sec
    2. 69.031 AP

![Untitled](image/Untitled%202.png)

1. pointpliar
    1. 0.0309 sec
    2. 64.862
    
    ![Untitled](image/Untitled%203.png)
    
2. pv rcnn
    1. 0.1209 sec
    2. 71.220 AP
    
    ![Untitled](image/Untitled%204.png)
    
3. pv rcnn++
    1. 0.0750 sec
    2. 74.210 AP
    
    ![Untitled](image/Untitled%205.png)
    
4. center point
    1. 0.0095 sec
    2. 63.534 AP
    
    ![Untitled](image/Untitled%206.png)
    

table

|  | Pedestrain 3D AP | sec per frame |
| --- | --- | --- |
| SECOND | 57.307 | 0.0116 |
| Voxel RCNN | 69.031 | 0.0186 |
| PointPliar | 64.862 | 0.0309 |
| PV RCNN | 71.220 | 0.1209 |
| PV RCNN++ | 74.210 | 0.0750 |
| Center Point | 63.534 | 0.0095 |

|  | Pedestrain 3D AP | sec per frame |
| --- | --- | --- |
| PV RCNN | 71.220 | 0.1209 |
| PV RCNN ++ | 74.210 | 0.0750 |
| Deformable PV RCNN | 74.111 | 0.1209 + c |

![center_ped-min.gif](image/center_ped-min.gif)