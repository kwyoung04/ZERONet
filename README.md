# Point Cloud

## 테스트 detection 알고리즘

1. ****SECOND: Sparsely Embedded Convolutional Detection (2018)****

![Untitled](Point%20Cloud%20fbbb273063f249e580adc26c2e51f72f/Untitled.png)

3D → 2D 관점에서 어떻게 데이터를 잘, 3D, 2D, 

1. ****PV-RCNN: Point-Voxel Feature Set Abstraction for 3D Object Detection**** (2019)

![Untitled](Point%20Cloud%20fbbb273063f249e580adc26c2e51f72f/Untitled%201.png)

1. ****Voxel R-CNN: Towards High Performance Voxel-based 3D Object Detection (2020)****

![Untitled](Point%20Cloud%20fbbb273063f249e580adc26c2e51f72f/Untitled%202.png)

결과 표 (waymo data, vanilla)

| Model | Inference Time [me] | Pedestrians       E |                                M | car (paper)                                   E |                                    M |
| --- | --- | --- | --- | --- | --- |
| SECONDE | 29 | 0.49 | 0.44 | 0.846 | 0.759 |
| PV-RCNN | 342 | 0.42 | 0.38 | 0.902 | 0.814 |
| Voxel R-CNN | 44 | 0.54 | 0.49 | 0.909 | 0.81 |
| Part A2 |  |  |  | 0.87 |  |

## 문제

1. 대부분의 알고리즘에서 차량 대비 보행자의 검출 성능이 높지 않다
2. 라이다 센서로 취득하는 포인트 클라우드의 숫자에 따라 성능 불균형이 심함
    1. 채널(vertical resolution)뿐 아니라 horizontal resolution의 영향도 크다
    2. 대부분 평가 기준을 오픈데이터(KITTI, waymo)를 기준으로 성능을 평가함
    3. 채널의 따라 가격이 천차만별
    
    ![Untitled](Point%20Cloud%20fbbb273063f249e580adc26c2e51f72f/Untitled%203.png)
    

## 해결 방안

문제 2에 초점으로 둠

1. data augmentation
    1. 랜덤 드롭등 데이터 밀도 및 갯수에 관련된 augmentaiton 기법들 사용

![Untitled](Point%20Cloud%20fbbb273063f249e580adc26c2e51f72f/Untitled%204.png)

1. 필터 크기 및 레이어 깊이
    1. 데이터가 적고, 포인트 클라우드의 밀도가 낮으니 데이터 컨볼루션 과정에서 손실 가능성이 크다
    2. Deformable Convolutional Networks
        
        [Deformable Convolutional Networks](https://www.notion.so/Deformable-Convolutional-Networks-38a98240c6204e61b574ff05fb3041c1)
        
        ![Untitled](Point%20Cloud%20fbbb273063f249e580adc26c2e51f72f/Untitled%205.png)
        
          ㄱ. Scale, Rotation invariant 
        
        객체의 GT와 인풋 데이터 차이 에 따른 로케이션 문제, 리얼 크기의 차이
        

               ㄴ. Receptive field

                → Conv 필터 크기, voxel size

1. HRDNet: High-resolution Detection Network for Small Objects (항공 카메라 디텍션 (스몰 오브젝트))
    
    [HRDNet: High-resolution Detection Network for Small Objects](https://www.notion.so/HRDNet-High-resolution-Detection-Network-for-Small-Objects-4bf7e8b989164cc1ab23db3f2b2254b0)
    

## 실험 (KITTI, ****Anchor-free****)

디텍션 알고리즘은 Voxel-RCNN 통일

데이터는 64ch, 6도, 16ch, 1도같은 적은 데이터가 목표이지만 가공 이전이라 KITTI 데이터로 결과 확인

1. 3D Convs 필터 크기

| 크기 | Pedestrians
E | 
M | Car
E | 
M |
| --- | --- | --- | --- | --- |
| 3X3 (ref) | 0.646 | 0.571 | 0.892 | 0.790 |
| 5X5 | 0.644 | 0.58 | 0.886 | 0.786 |
| 7X7 | 0.606 | 0.534 | 0.892 | 0.780 |
1. 레이어 깊이

![Untitled](Point%20Cloud%20fbbb273063f249e580adc26c2e51f72f/Untitled%206.png)

| 깊이 | Pedestrians
E | 
M | Car
E | 
M |
| --- | --- | --- | --- | --- |
| 5 |  |  |  |  |
| 3 |  |  |  |  |
| 2 |  |  |  |  |
|  |  |  |  |  |
1. Submanifold convolution의 비율

![Untitled](Point%20Cloud%20fbbb273063f249e580adc26c2e51f72f/Untitled%207.png)

![Untitled](Point%20Cloud%20fbbb273063f249e580adc26c2e51f72f/Untitled%208.png)

- 크게 4 layer로 쌓고 내부에 sparse convolution과 submanifold convolution으로 empty voxel을 줄여나감
- submanifold convolution의 비율을 줄여 적은 포인트에서 손실되는 데이터의 비율을 줄인다

| 깊이 | Pedestrians
E | 
M | Car
E | 
M |
| --- | --- | --- | --- | --- |
| 1:2 |  |  |  |  |
| 1:1 | 62.68 | 56.88 | 89.02 | 78.95 |

1. Focals Conv

|  | Pedestrians
E | 
M | Car
E | 
M |
| --- | --- | --- | --- | --- |
|  | 64.27 | 58.04 | 89.48 | 79.40 |
| 5x5 | 59.12 | 52.54 | 88.67 | 78.71 |

1. Deformable Sparse Conv

![Untitled](Point%20Cloud%20fbbb273063f249e580adc26c2e51f72f/Untitled%209.png)

![Untitled](Point%20Cloud%20fbbb273063f249e580adc26c2e51f72f/Untitled%2010.png)

![Untitled](Point%20Cloud%20fbbb273063f249e580adc26c2e51f72f/Untitled%2011.png)

|  | Pedestrians
E | 
M | Car
E | 
M |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |
|  |  |  |  |  |

1. Attention

|  | Pedestrians
E | 
M | Car
E | 
M |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |
|  |  |  |  |  |

1. Focal Loss (RetinaNet)
- `Cross Entropy Loss`의 근본적인 문제가 Foreground 대비 Background의 객체가 굉장히 많이 나오는 class imbalance 문제에 해당하였습니다. 따라서 `Balanced Cross Entropy Loss`의 `weight` w 를 이용하면 w 에 대한 값의 조절을 통해 해결할 수 있을 것으로 보입니다. 즉, Forground의 weight는 크게 Background의 weight는 작게 적용하는 방향으로 개선하고자 하는 것입니다.
- 하지만 이와 같은 방법에는 문제점이 있습니다. 바로, **Easy/Hard example 구분을 할 수 없다는 점**입니다. **단순히 갯수가 많다고 Easy라고 판단하거나 Hard라고 판단하는 것에는 오차가 발생할 수 있습니다.**

|  | Pedestrians
E | 
M | Car
E | 
M |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |
|  |  |  |  |  |

### 추가

- CenterHead
    - free agnchor 방식으로 각 클래스마다 학습을 따로 하는 voxel based 방식의 학습 방식을 바꿈
    - 논문 리뷰 및 다른 알고리즘에도 적용
- 뷰어 코드 제작(SUSPoint, python 3D)
- 가공 툴 오픈, 가이드 문서 제작 완료

[디버그](https://www.notion.so/6f0d09854a684d6891cb94d808f1ec90)