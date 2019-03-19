from matplotlib.pyplot import imsave
import scipy.io as sio
import numpy as np


def load_array(path):
    array = sio.loadmat(path)['section']
    return array

def decide_boundary(sum_vec):
    length = len(sum_vec)
    lower_boundary = 0
    upper_boundary = length
    if np.min(sum_vec) != 0:
        return lower_boundary,upper_boundary
    for i in range(length-1):
        if sum_vec[i] == 0:
            if sum_vec[i+1] > 0 and i<length/2:
                lower_boundary = i+1
            elif sum_vec[i-1] > 0 and i>length/2:
                upper_boundary = i-1
    return lower_boundary,upper_boundary

def give_up_padding(imgArray):
    imgArray = np.array(imgArray)
    x_sum = np.sum(imgArray,axis=0)
    y_sum = np.sum(imgArray,axis=1)
    x1,x2 = decide_boundary(x_sum)
    y1,y2 = decide_boundary(y_sum)
    print(x1,x2,y1,y2)
    imgArray = imgArray[y1:y2,x1:x2]
    return imgArray

def save_image_to(imgArray, name):
    imgArray = imgArray.astype(float)
    try:
        imsave(name, imgArray, cmap='gray', vmin=np.min(imgArray), vmax=np.max(imgArray))
    except Exception as e:
        print(e)
        print('save failed')
        return False
    else:
        print('image saved to: ' + name)
        return True

def rotate_slice(mat_path,rotate_angle=(0,0,0)):

    def gen_mid_saggital_plane(xs,ys,zs):
        saggital_pos = zs/2
        saggital_plane = np.zeros((ys,xs,3))
        for x in range(xs):
            for y in range(ys):
                saggital_plane[y,x,:] = [x-xs/2, y-ys/2, 0]
        return saggital_plane

    mat_path = mat_path
    imgArray = load_array(mat_path)
    # print(np.shape(imgArray))
    # save_image_to(imgArray[:,128,:],img_path)
    rax = np.pi*rotate_angle[0]/180
    ray = np.pi*rotate_angle[1]/180
    raz = np.pi*rotate_angle[2]/180
    zs,ys,xs = np.shape(imgArray)
    init_array = np.zeros((ys,xs))
    img_origin = (xs/2,ys/2,zs/2)
    
    #rotation matrix
    x_axis_matrix = np.array([[1,0,0],[0,np.cos(rax),-np.sin(rax)],[0,np.sin(rax),np.cos(rax)]])
    y_axis_matrix = np.array([[np.cos(ray),0,np.sin(ray)],[0,1,0],[-np.sin(ray),0,np.cos(ray)]])
    z_axis_matrix = np.array([[np.cos(raz),-np.sin(raz),0],[np.sin(raz),np.cos(raz),0],[0,0,1]])

    saggital_plane = gen_mid_saggital_plane(xs,ys,zs)
    rotated_sag_plane = np.zeros((ys,xs,3))

    for x in range(xs):
        for y in range(ys):
            vec = np.reshape(saggital_plane[y,x,:],(3,1))
            if rotate_angle[0] != 0:
                vec = np.dot(x_axis_matrix,vec)
            if rotate_angle[1] != 0:
                vec = np.dot(y_axis_matrix,vec)
            if rotate_angle[2] != 0:
                vec = np.dot(z_axis_matrix,vec)
            vec = np.reshape(vec,(3,))
            rotated_sag_plane[y,x,:] = np.round(vec)

    for x in range(xs):
        for y in range(ys):
                vec = rotated_sag_plane[y,x,:]
                xt,yt,zt = vec + img_origin
                xt,yt,zt = [int(xt),int(yt),int(zt)]
                # print(x,y,xt,yt,zt)
                if zt>0 and zt<zs and xt>0 and xt<xs and yt>0 and yt<ys:
                    value = imgArray[zt,yt,xt]
                    init_array[y,x] = value
    return init_array

if __name__ == '__main__':
    mat_path = '2710.mat'
    for i in range(90):
        save_path = 'result'+str(i)+'.png'
        new_image = rotate_slice(mat_path,rotate_angle=(0,i,0))
        new_image = give_up_padding(new_image)
        save_image_to(new_image,save_path)
    # save_path = 'result.png'
    # new_image = rotate_slice(mat_path,rotate_angle=(0,0,0))
    # new_image = give_up_padding(new_image)
    # save_image_to(new_image,save_path)