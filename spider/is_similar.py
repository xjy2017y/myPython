def is_similar(image1,image2,x,y):
    '''
    对比RGB值
    '''
    pass

    pixel1=image1.getpixel((x,y))
    pixel2=image2.getpixel((x,y))

    for i in range(0,3):
        if abs(pixel1[i]-pixel2[i])>=50:
            return False

    return True

def get_diff_location(image1,image2):
    '''
    计算缺口的位置
    '''

    i=0

    for i in range(0,260):
        for j in range(0,116):
            if is_similar(image1,image2,i,j)==False:
                return  i