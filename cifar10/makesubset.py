import glob
import os
import random
import shutil

imgs_per_class = 10
cifar10_dir = 'cifar10'
savedir = 'cifar10_subset'
cates = os.listdir(os.path.join(cifar10_dir,'train'))

for c in cates:
    os.mkdir(os.path.join(savedir,'train',c))
    print(os.path.join(cifar10_dir,'train',c,'*.png'))
    imgs = glob.glob(os.path.join(cifar10_dir,'train',c,'*.png'))
    imgs = random.sample(imgs,imgs_per_class)

    for im in imgs:
        shutil.copyfile(im,os.path.join(savedir,'train',c,os.path.basename(im)))