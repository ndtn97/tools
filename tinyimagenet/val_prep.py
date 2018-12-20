#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import os
import shutil
import argparse

parser = argparse.ArgumentParser(description='Validation Prepare')
parser.add_argument('--dir',default=os.path.join(os.environ['HOME'],'dataset','tiny-imagenet-200','val'))
args = parser.parse_args()

# In[ ]:


DIR = args.dir
print(DIR)


# In[ ]:


data = pd.read_table(os.path.join(DIR,'val_annotations.txt'),header=None)


# In[ ]:


data.head()


# In[ ]:


class_ids = sorted(data[1].unique())


# In[ ]:


len(class_ids)


# In[ ]:


for class_id in class_ids:
    os.mkdir(os.path.join(DIR,class_id))
    os.mkdir(os.path.join(DIR,class_id,'images'))


# In[ ]:


files = data[0]
class_ids = data[1]


# In[ ]:


for i,file in enumerate(files):
    shutil.move(os.path.join(DIR,'images',file),os.path.join(DIR,class_ids[i],'images'))


# In[ ]:




