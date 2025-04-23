polygon = [
    [[15.1, 50.1], [15.2, 50.1], [15.3, 50.2], [15.2, 50.3], [15.1, 50.2], [15.1, 50.1]]
]

polygon_ctverec = [
    [[16.1, 50.1], [16.2, 50.1], [16.3, 50.2], [16.2, 50.3], [16.1, 50.1]]
]

polygon2 = [
    polygon,
    polygon_ctverec
]


druhy_vrchol = polygon2[1][0][1]
print(druhy_vrchol)  

slicing = polygon2[1][0][-3:]
print(slicing)  
