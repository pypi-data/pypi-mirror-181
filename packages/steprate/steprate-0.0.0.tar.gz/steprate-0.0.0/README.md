# StepRate

Step Rate Compute

计算阶梯扣率或阶梯分成的一组方法

[Github地址](https://github.com/samjoeyang/steprate "Github")

> 为学习如何打包成pypi包编写的简易代码，仅供参考

## 参数

`amount` 待计算的金额
`rate` 阶梯扣率设定
`deduction` 扣除数

## 设定阶梯扣率的格式

数组的阶梯扣率，最后一个元素必须是包含有`-1`的`tuple`

```python
rate = [
        (10000,10),
        (20000,15),
        (30000,20),
        (40000,25),
        (50000,30),
        (-1,50),
    ]
```

## 计算类型

### 全量计算

`type=1`或者`type='full'`，返回值是一个数字

### 全量阶梯

`type=2`或者`type='stepfull'`，返回值是一个数字

### 溢出阶梯

`type=1`或者`type='stepover'`，返回值是一个数组，可以计算合计费用

### 设定计算类型的例子

```python
obj = steprate()
obj.type = 1
obj.type='full'
```

### 例子

```python
    rate = [
        (10000,10),
        (20000,15),
        (30000,20),
        (40000,25),
        (50000,30),
        (-1,50),
    ]
    
    obj = steprate()
    obj.compute(70001, rate, 10000,'stepover')
    rst = obj.result
    
    print(rst)
    
    # 计算结果 15000.5

    print(obj.results)

    # 计算结果 [1000.0, 1500.0, 2000.0, 2500.0, 3000.0, 5000.5]

```

